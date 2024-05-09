__all__: Final[tuple[str, ...]] = (
    "preorder",
    "inorder",
    "reverse_inorder",
    "postorder",
    "levelorder",
)

from typing import Final, TypeVar, overload

from nrw.datastructures import BinarySearchTree, BinaryTree, ComparableContentT, List

_T = TypeVar("_T")

@overload
def preorder(tree: BinaryTree[_T]) -> List[_T]: ...
@overload
def preorder(
    tree: BinarySearchTree[ComparableContentT],
) -> List[ComparableContentT]: ...
@overload
def inorder(tree: BinaryTree[_T]) -> List[_T]: ...
@overload
def inorder(
    tree: BinarySearchTree[ComparableContentT],
) -> List[ComparableContentT]: ...
@overload
def reverse_inorder(tree: BinaryTree[_T]) -> List[_T]: ...
@overload
def reverse_inorder(
    tree: BinarySearchTree[ComparableContentT],
) -> List[ComparableContentT]: ...
@overload
def postorder(tree: BinaryTree[_T]) -> List[_T]: ...
@overload
def postorder(
    tree: BinarySearchTree[ComparableContentT],
) -> List[ComparableContentT]: ...
@overload
def levelorder(tree: BinaryTree[_T]) -> List[_T]: ...
@overload
def levelorder(
    tree: BinarySearchTree[ComparableContentT],
) -> List[ComparableContentT]: ...
