__all__: Final[tuple[str]] = ("Queue",)

from typing import Final, Generic, TypeVar

_T = TypeVar("_T")

class Queue(Generic[_T]):
    __slots__: Final[tuple[str, str]] = ("_head", "_tail")
    __hash__ = None  # type: ignore[assignment]

    def __init__(self) -> None: ...
    @property
    def is_empty(self) -> bool: ...
    def enqueue(self, content: _T) -> None: ...
    def dequeue(self) -> None: ...
    @property
    def front(self) -> _T | None: ...
