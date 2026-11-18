'''
This module creates one markdown (.md) file per ticket on disk from a template and appends a 
timestamped entry under a named ## section header in that file, replacing the _pending_ placeholder, 
with every action traced and audit-logged.
'''

from langsmith import traceable
from pathlib import Path

# `init_memory` creates a ticket's `.md` file from a template (unless it already exists), 
# logs it, and returns the file's path.

@traceable(run_type="tool")
def init_memory(ticket_id: str, title: str) -> Path:
    path = MEMORY_DIR / f"{ticket_id}.md"
    # complete here
    return path