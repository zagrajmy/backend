from typing import Any

from django import template

register: Any

class IndentByNode(template.Node):
    nodelist: Any = ...
    indent_level: Any = ...
    if_statement: Any = ...
    def __init__(self, nodelist: Any, indent_level: Any, if_statement: Any) -> None: ...
    def render(self, context: Any): ...

def indentby(parser: Any, token: Any): ...