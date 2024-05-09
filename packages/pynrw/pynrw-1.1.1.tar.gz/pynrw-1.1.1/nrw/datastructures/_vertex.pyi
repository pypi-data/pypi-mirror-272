__all__: Final[tuple[str]] = ("Vertex",)

from typing import Final

class Vertex:

    __slots__: Final[tuple[str, str]] = ("_id", "_mark")
    __hash__ = None  # type: ignore[assignment]

    def __init__(self, id_: str) -> None: ...
    @property
    def id(self) -> str: ...
    @property
    def mark(self) -> bool: ...
    @mark.setter
    def mark(self, new_mark: bool) -> None: ...
    @property
    def is_marked(self) -> bool: ...
