
import asyncio

from a_sync._typing import *
from a_sync.a_sync._flags import VIABLE_FLAGS

if TYPE_CHECKING:
    from a_sync import TaskMapping


class ASyncFlagException(ValueError):
    @property
    def viable_flags(self) -> Set[str]:
        
        return VIABLE_FLAGS

    def desc(self, target) -> str:
        if target == 'kwargs':
            return "flags present in 'kwargs'"
        else:
            return f'flag attributes defined on {target}'

class NoFlagsFound(ASyncFlagException):
    def __init__(self, target, kwargs_keys=None):
        err = f"There are no viable a_sync {self.desc(target)}:"
        err += f"\nViable flags: {self.viable_flags}"
        if kwargs_keys:
            err += f"\nkwargs keys: {kwargs_keys}"
        err += "\nThis is likely an issue with a custom subclass definition."
        super().__init__(err)

class TooManyFlags(ASyncFlagException):
    def __init__(self, target, present_flags):
        err = f"There are multiple a_sync {self.__get_desc(target)} and there should only be one.\n"
        err += f"Present flags: {present_flags}\n"
        err += "This is likely an issue with a custom subclass definition."
        super().__init__(err)

class InvalidFlag(ASyncFlagException):
    def __init__(self, flag: Optional[str]):
        err = f"'flag' must be one of: {self.viable_flags}. You passed {flag}."
        err += "\nThis code should not be reached and likely indicates an issue with a custom subclass definition."
        super().__init__(err)

class InvalidFlagValue(ASyncFlagException):
    def __init__(self, flag: str, flag_value: Any):
        super().__init__(f"'{flag}' should be boolean. You passed {flag_value}.")

class FlagNotDefined(ASyncFlagException):
    def __init__(self, obj: Type, flag: str):
        super().__init__(f"{obj} flag {flag} is not defined.")


class ImproperFunctionType(ValueError):
    pass

class FunctionNotAsync(ImproperFunctionType):
    def __init__(self, fn):
        super().__init__(f"`coro_fn` must be a coroutine function defined with `async def`. You passed {fn}.")

class FunctionNotSync(ImproperFunctionType):
    def __init__(self, fn):
        super().__init__(f"`func` must be a coroutine function defined with `def`. You passed {fn}.")

class KwargsUnsupportedError(ValueError):
    def __init__(self):
        super().__init__("`run_in_executor` does not support keyword arguments, pass them as positional args instead if you're able")
        
class ASyncRuntimeError(RuntimeError):
    def __init__(self, e: RuntimeError):
        super().__init__(str(e))

class SyncModeInAsyncContextError(ASyncRuntimeError):
    def __init__(self):
        err = f"The event loop is already running, which means you're trying to use an ASync function synchronously from within an async context.\n"
        err += f"Check your traceback to determine which, then try calling asynchronously instead with one of the following kwargs:\n"
        err += f"{VIABLE_FLAGS}"
        super().__init__(err)

class MappingError(Exception):
    _msg: str
    def __init__(self, mapping: "TaskMapping", msg: str = ''):
        msg = msg or self._msg + f":\n{mapping}"
        if mapping:
            msg += f"\n{dict(mapping)}"
        super().__init__(msg)
        self.mapping = mapping

class MappingIsEmptyError(MappingError):
    _msg = "TaskMapping does not contain anything to yield"

class MappingNotEmptyError(MappingError):
    _msg = "TaskMapping already contains some data. In order to use `map`, you need a fresh one"

class PersistedTaskException(Exception):
    def __init__(self, exc: E, task: asyncio.Task) -> None:
        super().__init__(f"{exc.__class__.__name__}: {exc}", task)
        self.exception = exc
        self.task = task

class EmptySequenceError(ValueError):
    ...