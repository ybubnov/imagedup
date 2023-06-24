from datetime import datetime

from imagedup.kopernikus import ImageMetadata


def test_from_filepath_format1():
    filepath = "~/c20-1616783552981.jpg"
    result = ImageMetadata.from_filepath(filepath)
    assert result == ImageMetadata(
        filepath, "c20", datetime(2021, 3, 26, 19, 32, 32, 981000)
    )


def test_from_filepath_format2():
    filepath = "/tmp/imagedup/c20_2021_03_25__16_18_36.png"
    result = ImageMetadata.from_filepath(filepath)
    assert result == ImageMetadata(filepath, "c20", datetime(2021, 3, 25, 16, 18, 36))
