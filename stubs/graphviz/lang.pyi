from typing import Callable, Dict, Match, Optional, Set

def quote(
    identifier: str,
    is_html_string: Callable[[str, Optional[int], Optional[int]], Match[str]] = ...,
    is_valid_id: Callable[[str, Optional[int], Optional[int]], Match[str]] = ...,
    dot_keywords: Set[str] = ...,
    escape_unescaped_quotes: Callable[[str, Optional[int]], str] = ...,
) -> str: ...
def quote_edge(identifier: str) -> str: ...
def a_list(
    label: str = ...,
    kwargs: Dict[str, str] = ...,
    attributes: Dict[str, str] = ...,
) -> str: ...
def attr_list(
    label: str = ...,
    kwargs: Dict[str, str] = ...,
    attributes: Dict[str, str] = ...,
) -> str: ...
def escape(s: str) -> str: ...

class NoHtml: ...

def nohtml(s: str) -> str: ...
