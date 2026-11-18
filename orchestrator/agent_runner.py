'''
Core agent runner that spawns and manages Claude Code sessions via the SDK, handles execution timeouts, 
logs progress, and synchronizes state with Linear and memory files.
'''

import asyncio

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    TextBlock,
)
from claude_agent_sdk import (
    query as claude_query,
)


async def _run_claude_session(prompt: str, workspace_path: str, timeout: float) -> str:
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
    