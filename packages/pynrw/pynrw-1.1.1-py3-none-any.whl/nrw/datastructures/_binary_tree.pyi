__all__: Final[tuple[str]] = ("BinaryTree",)

from typing import Final, Generic, TypeVar, overload

_T = TypeVar("_T")

class BinaryTree(Generic[_T]):
    __slots__: Final[tuple[str]] = ("_node",)
    __hash__ = None  # type: ignore[assignment]

    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self,
        content: _T | None,
    ) -> None: ...
    @overload
    def __init__(
        self,
        content: _T | None,
        left_tree: BinaryTree[_T] | None,
        right_tree: BinaryTree[_T] | None,
    ) -> None: ...
    @property
    def is_empty(self) -> bool: ...
    @property
    def content(self) -> _T | None: ...
    @content.setter
    def content(self, new_content: _T | None) -> None: ...
    @property
    def left_tree(self) -> BinaryTree[_T] | None: ...
    @left_tree.setter
    def left_tree(self, new_tree: BinaryTree[_T] | None) -> None: ...
    @property
    def right_tree(self) -> BinaryTree[_T] | None: ...
    @right_tree.setter
    def right_tree(self, new_tree: BinaryTree[_T] | None) -> None: ...
