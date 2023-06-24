from torchdata.datapipes.iter import IterableWrapper

from imagedup.parallel_map import ParallelMapper


def pickleable_add(x):
    return x + x


def test_parallel_mapper():

    dp = IterableWrapper(range(100))
    dp = ParallelMapper(dp, fn=pickleable_add, chunksize=10)

    assert list(dp) == list(range(0, 200, 2))
