from typing import Iterator
from typing import List
from typing import TypeVar

from torchdata.datapipes.iter import IterDataPipe


T = TypeVar("T")


class Ungrouper(IterDataPipe[T]):
    """A DataPipe that ungroups the stream of grouped elements."""

    def __init__(self, source_datapipe: IterDataPipe[List[T]]) -> None:
        self.source_datapipe = source_datapipe

    def __iter__(self) -> Iterator[T]:
        for group in self.source_datapipe:
            yield from group
