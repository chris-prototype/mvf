"""Factory-wide configuration: env vars, paths, constants."""

import os
import logging
from pathlib import Path

# works with a local .env file or cloud based secrets
try:
    from dotenv import load_dotenv
    load_dotenv()  # No-op if no .env file is found
except ImportError:
    pass

# Directories
MEMORY_DIR = Path("memory")
AUDIT_DIR = Path("audit")
TEMPLATE_PATH = MEMORY_DIR / "_template.md"
SKILLS_DIR = Path(".claude/skills")
DB_PATH = "factory.db"

# API keys and secrets
LINEAR_API_KEY = os.getenv("LINEAR_API_KEY", "")
LINEAR_WEBHOOK_SECRET = os.getenv("LINEAR_WEBHOOK_SECRET", "")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

GITHUB_ORG = os.getenv("GITHUB_ORG", "ashtilawat")
WORKSPACE_DIR = Path("/app/workspace")

# Timeouts
AGENT_TIMEOUT = 1800  # 30 minutes
PIPELINE_TIMEOUT = 4 * 60 * 60  # 240 minutes

# Logging
logger = logging.getLogger("factory")
logging.basicConfig(level=logging.INFO)