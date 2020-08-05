from typing import Optional

class Base:
    @property
    def format(self) -> str: ...
    @format.setter
    def format(self, format: str) -> None: ...
    @property
    def engine(self) -> str: ...
    @engine.setter
    def engine(self, engine: str) -> None: ...
    @property
    def encoding(self) -> str: ...
    @encoding.setter
    def encoding(self, encoding: str) -> None: ...
    def copy(self) -> "Base": ...

class File(Base):
    directory: str = ...
    filename: str = ...
    format: str = ...
    engine: str = ...
    encoding: str = ...
    def __init__(
        self,
        filename: Optional[str] = ...,
        directory: Optional[str] = ...,
        format: Optional[str] = ...,
        engine: Optional[str] = ...,
        encoding: str = ...,
    ) -> None: ...
    def pipe(
        self,
        format: Optional[str] = ...,
        renderer: Optional[str] = ...,
        formatter: Optional[str] = ...,
        quiet: bool = ...,
    ) -> bytes: ...
    @property
    def filepath(self) -> str: ...
    def save(
        self, filename: Optional[str] = ..., directory: Optional[str] = ...
    ) -> str: ...
    def render(
        self,
        filename: Optional[str] = ...,
        directory: Optional[str] = ...,
        view: bool = ...,
        cleanup: bool = ...,
        format: Optional[str] = ...,
        renderer: Optional[str] = ...,
        formatter: Optional[str] = ...,
        quiet: bool = ...,
        quiet_view: bool = ...,
    ) -> str: ...
    def view(
        self,
        filename: Optional[str] = ...,
        directory: Optional[str] = ...,
        cleanup: bool = ...,
        quiet: bool = ...,
        quiet_view: bool = ...,
    ) -> str: ...

class Source(File):
    @classmethod
    def from_file(
        cls,
        filename: str,
        directory: Optional[str] = ...,
        format: Optional[str] = ...,
        engine: Optional[str] = ...,
        encoding: str = ...,
    ) -> "Source": ...
    source: str = ...
    def __init__(
        self,
        source: str,
        filename: Optional[str] = ...,
        directory: Optional[str] = ...,
        format: Optional[str] = ...,
        engine: Optional[str] = ...,
        encoding: str = ...,
    ) -> None: ...
