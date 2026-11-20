"""

 - logs to a daily local file
 - appends a timestamped entry for a ticket event to the daily log file.
 - schema - [<ts>] <ticket_id> | <event> | <detail>

"""

from datetime import datetime, timezone

from langsmith import traceable

from orchestrator.config import AUDIT_DIR, logger


@traceable(run_type="tool", name="audit_log")
def audit_log(ticket_id: str, event: str, detail: str = "") -> None:
    AUDIT_DIR.mkdir(exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ts = datetime.now(timezone.utc).isoformat()
    line = f"[{ts}] {ticket_id} | {event} | {detail}\n"
    with (AUDIT_DIR / f"{today}.log").open("a") as f:
        f.write(line)
    logger.info(line.strip())