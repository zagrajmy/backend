from typing import Any, Optional

def register(
    model: Any,
    app: Optional[Any] = ...,
    manager_name: str = ...,
    records_class: Optional[Any] = ...,
    table_name: Optional[Any] = ...,
    **records_config: Any,
) -> None: ...
