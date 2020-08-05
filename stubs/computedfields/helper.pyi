from typing import Any, Iterable, List, Optional, Sequence, Tuple, Type, TypeVar

from django.db.models import Model

E1 = TypeVar("E1")
E2 = TypeVar("E2")
E3 = TypeVar("E3")

def pairwise(iterable: Iterable[E1]) -> Iterable[Tuple[E1, E1]]: ...
def modelname(model: Type[Model]) -> str: ...
def is_sublist(
    needle: Optional[Sequence[E2]], haystack: Optional[Iterable[E2]]
) -> bool: ...
def parent_to_inherited_path(
    parent: Type[Model], inherited: Type[Model]
) -> List[str]: ...
def skip_equal_segments(ps: Iterable[Optional[E3]], rs: E3) -> List[E3]: ...
