

def _excerpt(text: str, max_lines: int = 30) -> str:
  lines = text.strip().splitlines()
  meaningful = [l for l in lines if l.strip() and not l.startswith("[STUB]")]
  if len(meaningful) <= max_lines:
      return "\n".join(meaningful)
  return "\n".join(meaningful[:max_lines]) + f"\n\n_(truncated — {len(meaningful)} lines total)_"


def _build_agent_prompt(
    state: FactoryState,
    skill_file: str,
    extra_prompt: str = "",
) -> str:
    """Assemble the full agent prompt from ticket context, memory, skill instructions, and optional extra guidance."""
    ticket_id = state["ticket_id"]
    memory_content = (MEMORY_DIR / f"{ticket_id}.md").read_text()
    skill_content = (SKILLS_DIR / skill_file).read_text()
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


async def _execute_claude_session(prompt: str, workspace_path: str, memory_section: str, ticket_id: str) -> str:
    """Run a Claude Code query with timeout, falling back to a stub if SDK is missing."""
    try:
        from claude_agent_sdk import query as claude_query, ClaudeAgentOptions

        options = ClaudeAgentOptions(
            cwd=workspace_path,
            permission_mode="bypassPermissions",
            allowed_tools=[
                "Read", "Write", "Edit", "Bash", "Glob", "Grep",
                "mcp__linear__*", "mcp__github__*",
                "mcp__vercel__*", "mcp__supabase__*", "mcp__slack__*",
            ],
        )

        async def _run_claude_query() -> list[str]:
            parts: list[str] = []
            async for message in claude_query(prompt=prompt, options=options):
                if hasattr(message, "content"):
                    for block in message.content:
                        if hasattr(block, "text"):
                            parts.append(block.text)
            return parts

        output_parts = await asyncio.wait_for(_run_claude_query(), timeout=AGENT_TIMEOUT)
        return "\n".join(output_parts)
    except ImportError:
        logger.warning("claude-agent-sdk not available, using stub")
        return f"[STUB] {memory_section} completed for {ticket_id}"


async def _post_linear_updates(
    ticket_id: str,
    memory_section: str,
    sub_issue_id: str,
    issue_info: dict | None,
    output: str,
) -> None:
    """Update Linear parent and child issues and update the audit log."""
    if issue_info:

        # update linear
        await comment_on_issue(
            issue_info["id"],
            f"🟢 **{memory_section}** — complete.\n\n{_excerpt(output)}",
        )
    if sub_issue_id:
        
        # update linear and audit log
        await update_stage_progress(
            ticket_id, memory_section, sub_issue_id,
            f"Agent finished. Output:\n\n{_excerpt(output, max_lines=50)}",
        )

        # update linear and audit log
        await complete_stage_sub_issue(ticket_id, memory_section, sub_issue_id)