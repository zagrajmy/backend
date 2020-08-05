import subprocess
from typing import Any, Dict, Iterable, Tuple, Type, TypeVar

PY2: bool
string_classes: Tuple[Type[str]]
text_type = str
K = TypeVar("K")
V = TypeVar("V")

def iteritems(d: Dict[K, V]) -> Iterable[Tuple[K, V]]: ...
def makedirs(name: str, mode: int = ..., exist_ok: bool = ...) -> None: ...
def stderr_write_bytes(data: str, flush: bool = ...) -> None: ...
def Popen_stderr_devnull(*args: Any, **kwargs: Any) -> subprocess.Popen[bytes]: ...

CalledProcessError = subprocess.CalledProcessError
