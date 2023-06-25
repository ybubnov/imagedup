from pathlib import Path
from typing import Iterator
from typing import List

import cv2
from torchdata.datapipes.iter import FileLister
from torchdata.datapipes.iter import Grouper
from torchdata.datapipes.iter import IterDataPipe
from torchdata.datapipes.iter import Mapper

from imagedup.kopernikus import ImageMetadata
from imagedup.parallel_map import ParallelMapper
from imagedup.similarity import compare_frames_change_detection
from imagedup.similarity import preprocess_image_change_detection
from imagedup.ungrouper import Ungrouper


class ImageDupFinder(IterDataPipe[str]):
    """A DataPipe to find images that are nearly duplicates.

    This pipeline uses parallel mapper to find duplicates for each camera.

    Args:
        root (str): A target directory to find duplicates.
        min_score (float): A minimum score that image comparison algorithm should
            reach to treat two images as distinct.
        min_area (float): A minimum size of a contour area to include into total score.
            Larger areas capture larger objects, while smaller areas include more noise.
        width (int): A width of the image that will be scaled to.
        height (int): A height of the image that will be scaled to.
    """

    def __init__(
        self,
        root: str,
        min_score: float,
        min_area: float,
        width: int = 2688,
        height: int = 1520,
    ) -> None:
        super().__init__()

        self.root = root
        self.shape = (height, width)
        self.min_score = min_score
        self.min_area = min_area
        self.image_masks = ["*.png", "*.jpg", "*.jpeg"]

    @staticmethod
    def group_by_camera(metadata: ImageMetadata) -> str:
        return metadata.camera_name

    def find_duplicates(
        self, metadata_list: List[ImageMetadata]
    ) -> List[ImageMetadata]:
        """Returns images that are duplicates for other images.

        The primary idea is that identical images are located only within close time
        locations. But we cannot compare only two neighbour images as there could be
        a case, when in 100 of inputs samples, only 2 are unique.

        To resolve this issue, the algorithm will keep a previous image and only
        update it when score exceeds a minimum
        """
        metadata_list = sorted(metadata_list, key=lambda metadata: metadata.timestamp)

        num_metadata = len(metadata_list)
        if not num_metadata:
            return []

        duplicates = []

        prev_frame = cv2.imread(metadata_list[0].filepath)
        prev_im = preprocess_image_change_detection(prev_frame)
        prev_im = cv2.resize(prev_im, self.shape[::-1])

        for i in range(1, num_metadata):
            next_frame = cv2.imread(metadata_list[i].filepath)

            # Skip damaged files. Do we need to add a parameter to control this
            # behavior?
            if next_frame is None:
                continue

            next_im = preprocess_image_change_detection(next_frame)
            if next_im.shape != self.shape:
                next_im = cv2.resize(next_im, self.shape[::-1])

            score, *_ = compare_frames_change_detection(prev_im, next_im, self.min_area)
            if score < self.min_score:
                duplicates.append(metadata_list[i])
                # We don't undate the previous image here. The reason is that the
                # difference between two pairs of nearby images might be small, but
                # longer we wait, the more differences we accumulate. Therefore always
                # compare the next image with the first one.
            else:
                prev_im = next_im
        return duplicates

    def __iter__(self) -> Iterator[Path]:
        # Read all files in the specifie directory, leave only those that
        # has an image extension.
        dp = FileLister(root=self.root, masks=self.image_masks, recursive=False)
        dp = Mapper(dp, ImageMetadata.from_filepath)
        dp = Grouper(dp, group_key_fn=self.group_by_camera)
        dp = ParallelMapper(dp, self.find_duplicates)
        dp = Ungrouper(dp)

        yield from dp
