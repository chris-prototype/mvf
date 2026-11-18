'''
Core agent runner that spawns and manages Claude Code sessions via the SDK, handles execution timeouts, 
logs progress, and synchronizes state with Linear and memory files.
'''

import asyncio
from state import FactoryState

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    TextBlock,
)
from claude_agent_sdk import (
    query as claude_query,
)

# modularizing code - _build_prompt - verify correctness
#
#
def _build_prompt(state: FactoryState, memory_content: str, skill_content: str, extra_prompt: str = "") -> str:
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


# modularizing code - _run_claude_session
#
#
async def _run_claude_session(prompt: str, workspace_path: str, timeout: float) -> str:
    options = ClaudeAgentOptions(
        cwd=workspace_path,
        permission_mode="bypassPermissions",
        allowed_tools=[
            "Read", "Write", "Edit", "Bash", "Glob", "Grep",
            "mcp__linear__*", "mcp__github__*", "mcp__vercel__*", "mcp__supabase__*", "mcp__slack__*",
        ],
    )
    # satisfy's the typechecker while validating sdk schema - isinstance
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







# if __name__ == "__main__":
#     result = asyncio.run(
#         _run_claude_session(
#             prompt="Hello, reply with a short test message.",
#             workspace_path=".",
#             timeout=30.0,
#         )
#     )
#     print(result)
