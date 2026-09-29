"""Single-line JSON logging helpers."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    """Return the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def log_event(event: str, level: str = "info", **fields: Any) -> str:
    """Print one structured event as a single JSON line and return it."""
    payload = {
        "event": event,
        "level": level.lower(),
        "timestamp": utc_now_iso(),
        **fields,
    }
    rendered = json.dumps(payload, ensure_ascii=False)
    print(rendered, flush=True)
    return rendered
