from multiprocessing import cpu_count
from multiprocessing import Pool
from typing import Callable
from typing import Iterator
from typing import Optional
from typing import TypeVar

from torchdata.datapipes import functional_datapipe
from torchdata.datapipes.iter import IterDataPipe


T_co = TypeVar("T_co", covariant=True)


@functional_datapipe("parallel_map")
class ParallelMapper(IterDataPipe[T_co]):
    """Applies a function over each item from the source datapipe in parallel.

    Args:
        datapipe (DataPipe): Source iterable datapipe.
        fn (Callable): Function being called over each item.
        num_procs (int, optional): A number of processes to spawn for processing.
        chunksize (int): A number of items within a single unit of work.

    Example:
        >>> from torchdata.datapipes.iter import IterableWrapper
        >>> from imagedup.parallel_map import ParallelMapper
        >>>
        >>> def add_one(x):
        ...     return x + 1
        >>> dp = IterableWrapper(range(10000))
        >>> dp = ParallelMapper(dp, fn=add_one)
        >>> list(dp)
        [1, 2, 3, ..., 10001]
    """

    def __init__(
        self,
        datapipe: IterDataPipe,
        fn: Callable,
        num_procs: Optional[int] = None,
        chunksize: int = 100,
    ):
        super().__init__()
        self.datapipe = datapipe
        self.fn = fn

        self.chunksize = chunksize
        self.num_procs = num_procs or cpu_count()
        if self.num_procs < 1:
            raise ValueError("num_procs should be >=1")

    def __iter__(self) -> Iterator[T_co]:
        with Pool(self.num_procs) as pool:
            yield from pool.imap(self.fn, self.datapipe, chunksize=self.chunksize)
