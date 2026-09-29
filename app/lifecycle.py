"""Graceful process shutdown state and signal forwarding."""

from __future__ import annotations

import signal
from types import FrameType
from typing import Any


class Lifecycle:
    """Track whether the process is draining traffic."""

    def __init__(self) -> None:
        self.shutting_down = False
        self._previous: dict[int, Any] = {}

    def request_shutdown(
        self,
        signum: int | None = None,
        frame: FrameType | None = None,
    ) -> None:
        """Mark shutdown and forward the signal to the previous handler."""
        self.shutting_down = True
        previous = self._previous.get(signum)
        if callable(previous):
            previous(signum, frame)

    def install(self) -> None:
        """Install handlers while preserving the server's existing handlers."""
        for sig in (signal.SIGTERM, signal.SIGINT):
            self._previous[sig] = signal.getsignal(sig)
            signal.signal(sig, self.request_shutdown)


lifecycle = Lifecycle()
