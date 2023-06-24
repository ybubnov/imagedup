from torchdata.datapipes.iter import IterableWrapper

from imagedup.ungrouper import Ungrouper


def test_ungrouper():
    dp = IterableWrapper([[1, 2, 3], [4, 5, 6]])
    dp = Ungrouper(dp)

    assert list(dp) == [1, 2, 3, 4, 5, 6]
