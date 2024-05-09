__all__: Final[tuple[str, ...]] = (
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    "merge_sort",
    "quick_sort",
)

from typing import Final

from nrw.datastructures._comparable_content import ComparableContentT
from nrw.datastructures._list import List

def bubble_sort(lst: List[ComparableContentT]) -> List[ComparableContentT]: ...
def selection_sort(lst: List[ComparableContentT]) -> List[ComparableContentT]: ...
def insertion_sort(lst: List[ComparableContentT]) -> List[ComparableContentT]: ...
def merge_sort(lst: List[ComparableContentT]) -> List[ComparableContentT]: ...
def quick_sort(lst: List[ComparableContentT]) -> List[ComparableContentT]: ...
