from typing import Any, List, Optional, TypeVar

from django.db.models import Manager, Model
from simple_history.exceptions import NotHistoricalModelError as NotHistoricalModelError
from simple_history.models import HistoricalRecords

M = TypeVar("M", bound=Model)

def update_change_reason(instance: Any, reason: Any) -> None: ...
def get_history_manager_for_model(model: M) -> Manager[M]: ...
def get_history_model_for_model(model: M) -> HistoricalRecords: ...
def bulk_create_with_history(
    objs: Any,
    model: M,
    batch_size: Optional[Any] = ...,
    default_user: Optional[Any] = ...,
    default_change_reason: Optional[Any] = ...,
) -> List[M]: ...
def bulk_update_with_history(
    objs: Any,
    model: M,
    fields: Any,
    batch_size: Optional[Any] = ...,
    default_user: Optional[Any] = ...,
    default_change_reason: Optional[Any] = ...,
) -> None: ...
def get_change_reason_from_object(obj: Any) -> None: ...
