"""
Append-only audit logging that writes timestamped,
ticket-scoped events to a daily UTC-dated log file
and mirrors them to the application logger.
"""

from datetime import datetime, timezone

from langsmith import traceable