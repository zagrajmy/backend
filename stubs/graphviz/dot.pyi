from types import TracebackType
from typing import Any, Dict, Generator, Iterable, List, Optional, Tuple, Type

from . import files

class Dot(files.File):
    name: str = ...
    comment: str = ...
    graph_attr: Dict[str, str] = ...
    node_attr: Dict[str, str] = ...
    edge_attr: Dict[str, str] = ...
    body: List[str] = ...
    strict: bool = ...
    def __init__(
        self,
        name: Optional[str] = ...,
        comment: Optional[str] = ...,
        filename: Optional[str] = ...,
        directory: Optional[str] = ...,
        format: Optional[str] = ...,
        engine: Optional[str] = ...,
        encoding: str = ...,
        graph_attr: Optional[Dict[str, str]] = ...,
        node_attr: Optional[Dict[str, str]] = ...,
        edge_attr: Optional[Dict[str, str]] = ...,
        body: Optional[List[str]] = ...,
        strict: bool = ...,
    ) -> None: ...
    def clear(self, keep_attrs: bool = ...) -> None: ...
    def __iter__(self, subgraph: bool = ...) -> Generator[str, None, None]: ...
    source: str = ...
    def node(
        self,
        name: str,
        label: Optional[str] = ...,
        _attributes: Optional[Dict[str, str]] = ...,
        **attrs: Dict[str, str],
    ) -> None: ...
    def edge(
        self,
        tail_name: str,
        head_name: str,
        label: Optional[str] = ...,
        _attributes: Optional[Dict[str, str]] = ...,
        **attrs: Dict[str, str],
    ) -> None: ...
    def edges(self, tail_head_iter: Iterable[Tuple[str, str]]) -> None: ...
    def attr(
        self,
        kw: Optional[str] = ...,
        _attributes: Optional[Dict[str, str]] = ...,
        **attrs: List[str],
    ) -> None: ...
    def subgraph(
        self,
        graph: Optional["Graph"] = ...,
        name: Optional[str] = ...,
        comment: Optional[str] = ...,
        graph_attr: Optional[Dict[str, str]] = ...,
        node_attr: Optional[Dict[str, str]] = ...,
        edge_attr: Optional[Dict[str, str]] = ...,
        body: Optional[List[str]] = ...,
    ) -> None: ...

class SubgraphContext:
    parent: Graph = ...
    graph: Graph = ...
    def __init__(self, parent: Graph, kwargs: Dict[str, Any]) -> None: ...
    def __enter__(self) -> Graph: ...
    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None: ...

class Graph(Dot):
    @property
    def directed(self) -> bool: ...

class Digraph(Dot):
    @property
    def directed(self) -> bool: ...
