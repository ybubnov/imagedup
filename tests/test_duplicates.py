from pathlib import Path

import cv2
import numpy as np

from imagedup.duplicates import ImageDupFinder


def test_find_duplicates(tmp_path: Path):
    dp = ImageDupFinder(str(tmp_path), 100, 100)

    im1 = np.random.randint(255, size=(300, 300, 3), dtype=np.uint8)
    im2 = np.full((400, 400, 3), 0, dtype=np.uint8)
    im3 = np.full((400, 400, 3), 255, dtype=np.uint8)

    file_template = "cam0_2023_01_23__10_20_0%d.jpg"

    cv2.imwrite(str(tmp_path / (file_template % 0)), im1)
    cv2.imwrite(str(tmp_path / (file_template % 1)), im1)
    cv2.imwrite(str(tmp_path / (file_template % 2)), im2)
    cv2.imwrite(str(tmp_path / (file_template % 3)), im2)
    cv2.imwrite(str(tmp_path / (file_template % 4)), im2)
    cv2.imwrite(str(tmp_path / (file_template % 5)), im3)
    cv2.imwrite(str(tmp_path / (file_template % 6)), im3)

    dups = [Path(metadata.filepath).name for metadata in dp]
    assert dups == [(file_template % i) for i in (1, 3, 4, 6)]
