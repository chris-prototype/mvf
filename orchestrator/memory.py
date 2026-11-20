"""

 - Utilities for managing a local ticket markdown file.
 - No synching with Linear in this file
 
"""

import threading
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path

from langsmith import traceable

from orchestrator.audit import audit_log
from orchestrator.config import MEMORY_DIR, TEMPLATE_PATH

_write_lock = threading.Lock()


def _get_memory_path(ticket_id: str) -> Path:
    """Return the Markdown file path for the given ticket ID."""
    return MEMORY_DIR / f"{ticket_id}.md"


def _render_template(ticket_id: str, title: str) -> str:
    """Load the memory template and replace ticket placeholders."""
    template = TEMPLATE_PATH.read_text()
    return template.replace("{{TICKET_ID}}", ticket_id).replace("{{TICKET_TITLE}}", title)


def _format_entry(content: str, timestamp: datetime | None = None) -> str:
    """Format content as a Markdown block prefixed with a UTC timestamp."""
    ts = (timestamp or datetime.now(timezone.utc)).isoformat()
    return f"_{ts}_\n\n{content}"


def _find_section_header(markdown: str, section: str, start: int = 0) -> int | None:
    """Return the start index of an exact ``## {section}`` header line, or None."""
    marker = f"## {section}"
    search_start = start

    while True:
        header_idx = markdown.find(marker, search_start)
        if header_idx == -1:
            return None

        at_line_start = header_idx == 0 or markdown[header_idx - 1] == "\n"
        after_marker = header_idx + len(marker)
        at_line_end = after_marker == len(markdown) or markdown[after_marker] == "\n"

        if at_line_start and at_line_end:
            return header_idx

        search_start = after_marker


def _find_section_bounds(markdown: str, section: str) -> tuple[int, int] | None:
    """Return the start and end character offsets for a second-level Markdown section body."""
    header_idx = _find_section_header(markdown, section)
    if header_idx is None:
        return None

    nl = markdown.find("\n", header_idx)
    body_start = len(markdown) if nl == -1 else nl + 1
    nxt = markdown.find("\n## ", body_start)
    body_end = len(markdown) if nxt == -1 else nxt
    return body_start, body_end


def _splice_section_body(markdown: str, section: str, block: str) -> str:
    """Insert or append a block under the target section in Markdown text."""
    bounds = _find_section_bounds(markdown, section)
    if bounds is None:
        prefix = "" if markdown.endswith("\n") else "\n"
        return f"{markdown}{prefix}\n## {section}\n{block}\n"

    body_start, body_end = bounds
    body = markdown[body_start:body_end]

    if body.strip() == "_pending_":
        new_body = f"{block}\n"
    else:
        new_body = f"{body.rstrip(chr(10))}\n\n{block}\n"

    return markdown[:body_start] + new_body + markdown[body_end:]


def _locked_transform(path: Path, transform: Callable[[str], str]) -> None:
    """Apply a text transformation to a file under the write lock."""
    with _write_lock:
        updated = transform(path.read_text())
        path.write_text(updated)


def _log_memory_init(ticket_id: str, path: Path) -> None:
    """Record an audit entry for memory file initialization."""
    audit_log(ticket_id, "memory_init", str(path))


def _log_memory_append(ticket_id: str, section: str, content: str) -> None:
    """Record an audit entry for a memory section append."""
    audit_log(ticket_id, f"memory_append:{section}", f"{len(content)} chars")


@traceable(run_type="tool", name="init_memory")
def init_memory(ticket_id: str, title: str) -> Path:
    """Create a ticket memory file from the template if it does not already exist."""
    path = _get_memory_path(ticket_id)
    if path.exists():
        return path

    MEMORY_DIR.mkdir(exist_ok=True)
    path.write_text(_render_template(ticket_id, title))
    _log_memory_init(ticket_id, path)
    return path


@traceable(run_type="tool", name="append_memory")
def append_memory(ticket_id: str, section: str, content: str) -> None:
    """Append a timestamped entry to a named section in the ticket memory file."""
    path = _get_memory_path(ticket_id)
    block = _format_entry(content)
    _locked_transform(path, lambda text: _splice_section_body(text, section, block))
    _log_memory_append(ticket_id, section, content)