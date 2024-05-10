
import asyncio
import sys

from a_sync._typing import *
from a_sync.primitives._debug import _DebugDaemonMixin


class Event(asyncio.Event, _DebugDaemonMixin):
    """asyncio.Event but with some additional debug logging to help detect deadlocks."""
    _value: bool
    _loop: asyncio.AbstractEventLoop
    _waiters: Deque["asyncio.Future[None]"]
    if sys.version_info >= (3, 10):
        __slots__ = "_value", "_waiters", "_debug_daemon_interval"
    else:
        __slots__ = "_value", "_loop", "_waiters", "_debug_daemon_interval"
    def __init__(self, name: str = "", debug_daemon_interval: int = 300, *, loop: Optional[asyncio.AbstractEventLoop] = None):
        if sys.version_info >= (3, 10):
            super().__init__()
        else:
            super().__init__(loop=loop)
        self._name = name
        # backwards compatability
        if hasattr(self, "_loop"):
            self._loop = self._loop or asyncio.get_event_loop()
        self._debug_daemon_interval = debug_daemon_interval
    def __repr__(self) -> str:
        label = f'name={self._name}' if self._name else 'object'
        status = 'set' if self._value else 'unset'
        if self._waiters:
            status += f', waiters:{len(self._waiters)}'
        return f"<{self.__class__.__module__}.{self.__class__.__name__} {label} at {hex(id(self))} [{status}]>"
    async def wait(self) -> Literal[True]:
        if self.is_set():
            return True
        self._ensure_debug_daemon()
        return await super().wait()
    async def _debug_daemon(self) -> None:
        while not self.is_set():
            await asyncio.sleep(self._debug_daemon_interval)
            if not self.is_set():
                self.logger.debug("Waiting for %s", self)
