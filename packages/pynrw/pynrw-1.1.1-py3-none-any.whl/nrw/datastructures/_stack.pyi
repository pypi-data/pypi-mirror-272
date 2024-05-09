__all__: Final[tuple[str]] = ("Stack",)

from typing import Final, Generic, TypeVar

_T = TypeVar("_T")

class Stack(Generic[_T]):
    __slots__: Final[tuple[str]] = ("_head",)
    __hash__ = None  # type: ignore[assignment]

    def __init__(self) -> None: ...
    @property
    def is_empty(self) -> bool: ...
    def push(self, content: _T) -> None: ...
    def pop(self) -> None: ...
    @property
    def top(self) -> _T | None: ...
