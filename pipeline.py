import re
from datetime import datetime


def _slugify(title: str) -> str:
    """Turn a ticket title into a valid GitHub repo name."""
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    slug = slug[:60].strip("-")
    if not slug:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        slug = f"app-{timestamp}"
    return slug