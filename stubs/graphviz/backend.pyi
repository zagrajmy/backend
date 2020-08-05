from typing import Any, Optional, Set, Tuple

from . import _compat

ENGINES: Set[str]
FORMATS: Set[str]
RENDERERS: Set[str]
FORMATTERS: Set[str]

class ExecutableNotFound(RuntimeError):
    def __init__(self, args: Tuple[Any]) -> None: ...

class RequiredArgumentError(Exception): ...
class CalledProcessError(_compat.CalledProcessError): ...

def render(
    engine: str,
    format: str,
    filepath: str,
    renderer: Optional[str] = ...,
    formatter: Optional[str] = ...,
    quiet: bool = ...,
) -> str: ...
def pipe(
    engine: str,
    format: str,
    data: bytes,
    renderer: Optional[str] = ...,
    formatter: Optional[str] = ...,
    quiet: bool = ...,
) -> str: ...
def version() -> Tuple[int, int, Optional[int]]: ...
def view(filepath: str, quiet: bool = ...) -> None: ...
