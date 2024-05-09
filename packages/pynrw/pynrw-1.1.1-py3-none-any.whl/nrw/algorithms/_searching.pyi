__all__: Final[tuple[str, ...]] = (
    "linear_search",
    "depth_first_search",
    "breadth_first_search",
)

from typing import Final, TypeVar

from nrw.datastructures._graph import Graph
from nrw.datastructures._list import List
from nrw.datastructures._vertex import Vertex

_T = TypeVar("_T")

def linear_search(lst: List[_T], element: _T) -> int: ...
def depth_first_search(graph: Graph, vertex: Vertex) -> List[Vertex]: ...
def breadth_first_search(graph: Graph, vertex: Vertex) -> List[Vertex]: ...
