"""

Core agent runner that spawns and manages Claude Code sessions via the SDK, handles execution timeouts,
logs progress, and synchronizes state with Linear and memory files.

"""

import asyncio

from langsmith import traceable

from orchestrator.config import SKILLS_DIR, MEMORY_DIR, AGENT_TIMEOUT, logger
from orchestrator.state import FactoryState
from orchestrator.audit import audit_log
from orchestrator.memory import append_memory
from orchestrator.linear import (
    update_linear_state,
    complete_stage_sub_issue,
    update_stage_progress,
    get_issue_id,
    comment_on_issue,
)
from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, TextBlock
from claude_agent_sdk import query as claude_query


def _excerpt(text: str, max_lines: int = 30) -> str:
    """Extract a meaningful excerpt from agent output for Linear comments."""
    lines = text.strip().splitlines()
    meaningful = [l for l in lines if l.strip() and not l.startswith("[STUB]")]
    if len(meaningful) <= max_lines:
        return "\n".join(meaningful)
    return "\n".join(meaningful[:max_lines]) + f"\n\n_(truncated — {len(meaningful)} lines total)_"


def _load_stage_inputs(state: FactoryState, skill_file: str) -> tuple[str, str, str, str]:
    """Load ticket ID, workspace path, memory text, and skill instructions for a stage."""
    ticket_id = state["ticket_id"]
    workspace_path = state.get("workspace_path", "/app")
    memory_content = (MEMORY_DIR / f"{ticket_id}.md").read_text()
    skill_content = (SKILLS_DIR / skill_file).read_text()
    return ticket_id, workspace_path, memory_content, skill_content


def _build_prompt(state: FactoryState, memory_content: str, skill_content: str, extra_prompt: str = "") -> str:
    """Assemble a Markdown prompt for a ticket from factory state, memory, skill instructions, and optional extra text."""
    ticket_id = state["ticket_id"]
    repo_name = state.get("repo_name", "")
    workspace_path = state.get("workspace_path", "/app")

    prompt = (
        f"You are working on ticket {ticket_id}: {state['title']}\n\n"
        f"**Repo**: `{repo_name}`\n"
        f"**Workspace**: `{workspace_path}`\n\n"
        f"All code changes go in this workspace directory — it is the root of the app repo.\n\n"
        f"## Memory File\n\n{memory_content}\n\n"
        f"## Your Skill Instructions\n\n{skill_content}"
    )
    if extra_prompt:
        prompt += f"\n\n{extra_prompt}"
    return prompt


async def _resolve_linear_targets(state: FactoryState, memory_section: str, post_updates: bool) -> tuple[str, dict | None]:
    """Resolve the stage sub-issue ID and parent issue info when Linear updates are enabled."""
    if not post_updates:
        return "", None
    ticket_id = state["ticket_id"]
    sub_issue_id = state.get("stage_sub_issues", {}).get(memory_section, "")
    issue_info = await get_issue_id(ticket_id)
    return sub_issue_id, issue_info


async def _notify_stage_start(ticket_id: str, memory_section: str, sub_issue_id: str, issue_info: dict | None) -> None:
    """Post start updates to the stage sub-issue and parent issue."""
    if sub_issue_id:
        await update_stage_progress(ticket_id, memory_section, sub_issue_id, f"Agent starting: **{memory_section}**")
    if issue_info:
        await comment_on_issue(issue_info["id"], f"🟡 **{memory_section}** — agent started.")


async def _run_claude_session(prompt: str, workspace_path: str, timeout: float) -> str:
    """Run a Claude agent session in a workspace with a timeout and return joined assistant text blocks."""
    options = ClaudeAgentOptions(
        cwd=workspace_path,
        permission_mode="bypassPermissions",
        allowed_tools=[
            "Read", "Write", "Edit", "Bash", "Glob", "Grep",
            "mcp__linear__*", "mcp__github__*", "mcp__vercel__*", "mcp__supabase__*", "mcp__slack__*",
        ],
    )

    async def _collect() -> list[str]:
        parts: list[str] = []
        async for message in claude_query(prompt=prompt, options=options):
            if not isinstance(message, AssistantMessage):
                continue
            for block in message.content:
                if isinstance(block, TextBlock):
                    parts.append(block.text)
        return parts

    output_parts = await asyncio.wait_for(_collect(), timeout=timeout)
    return "\n".join(output_parts)


async def _execute_session_with_fallback(prompt: str, workspace_path: str, ticket_id: str, memory_section: str) -> str:
    """Run a Claude agent session for a stage, falling back to a stub if the SDK is unavailable."""
    try:
        return await _run_claude_session(prompt, workspace_path, AGENT_TIMEOUT)
    except ImportError:
        logger.warning("claude-agent-sdk not available, using stub")
        return f"[STUB] {memory_section} completed for {ticket_id}"


async def _advance_linear_state(ticket_id: str, next_linear_state: str | None) -> None:
    """Transition the Linear ticket to ``next_linear_state`` when specified."""
    if next_linear_state:
        await update_linear_state(ticket_id, next_linear_state)


async def _post_parent_completion(issue_info: dict | None, memory_section: str, output: str) -> None:
    """Post a completion summary for the stage to the parent Linear issue."""
    if not issue_info:
        return
    await comment_on_issue(issue_info["id"], f"🟢 **{memory_section}** — complete.\n\n{_excerpt(output)}")


async def _finish_stage_sub_issue(ticket_id: str, memory_section: str, sub_issue_id: str, output: str) -> None:
    """Append a bounded output excerpt to a Linear stage sub-issue and mark it done when a sub-issue ID is present."""
    if not sub_issue_id:
        return
    await update_stage_progress(ticket_id, memory_section, sub_issue_id, f"Agent finished. Output:\n\n{_excerpt(output, max_lines=50)}")
    await complete_stage_sub_issue(ticket_id, memory_section, sub_issue_id)


@traceable(run_type="chain", name="run_agent")
async def run_agent(state: FactoryState, skill_file: str, memory_section: str, next_linear_state: str | None = None, extra_prompt: str = "", post_updates: bool = True, result_state: str | None = None) -> FactoryState:

    ticket_id, workspace_path, memory_content, skill_content = _load_stage_inputs(state, skill_file)
    prompt = _build_prompt(state, memory_content, skill_content, extra_prompt)

    audit_log(ticket_id, f"agent_start:{memory_section}", skill_file)

    sub_issue_id, issue_info = await _resolve_linear_targets(state, memory_section, post_updates)
    await _notify_stage_start(ticket_id, memory_section, sub_issue_id, issue_info)

    output = await _execute_session_with_fallback(prompt, workspace_path, ticket_id, memory_section)
    append_memory(ticket_id, memory_section, output)

    await _advance_linear_state(ticket_id, next_linear_state)
    await _post_parent_completion(issue_info, memory_section, output)
    await _finish_stage_sub_issue(ticket_id, memory_section, sub_issue_id, output)

    audit_log(ticket_id, f"agent_done:{memory_section}", f"{len(output)} chars")
    return {**state, "current_state": result_state or memory_section}


    '''
     - audit_log writes resultes to a local log file
    '''