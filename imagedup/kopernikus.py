from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class ImageMetadata:
    """Image metadata with information about the photos from surveillance camera."""

    filepath: str
    camera_name: str
    timestamp: datetime

    @staticmethod
    def from_filepath(filepath: str) -> ImageMetadata:
        """Parse a filename (without extension) to a tuple of camera name and timestamp.

        Example:
            >>> from_kopernikus_format("c20-1616783552981")
            ('c20', datetime.datetime(2021, 3, 26, 19, 32, 32, 981000))
            >>>
            >>> from_kopernikus_format("c20_2021_03_25__16_18_36")
            ('c20', datetime.datetime(2021, 3, 25, 16, 18, 36))
        """
        name = Path(filepath).stem
        parts = name.split("-", maxsplit=1)

        # When there are two parts in the name that are separated with a dash, then
        # use the first part as a camera name and the second part as a timestamp in
        # microseconds.
        if len(parts) == 2:
            timestamp = int(parts[1])
            return ImageMetadata(
                filepath=filepath,
                camera_name=parts[0],
                timestamp=datetime.fromtimestamp(timestamp / 1000),
            )

        # Try another format, which considers split by an underscore symbol. In case
        # of a successful split, replace symbols to cast the value to ISO format:
        #
        # 2021_03_25__16_18_36 => 2021-03-25 16:18:36
        parts = name.split("_", maxsplit=1)
        if len(parts) == 2:
            timestamp = parts[1].replace("__", " ")
            timestamp = timestamp.replace("_", "-", 2)
            timestamp = timestamp.replace("_", ":", 2)
            return ImageMetadata(
                filepath=filepath,
                camera_name=parts[0],
                timestamp=datetime.fromisoformat(timestamp),
            )

        raise ValueError(f"{name} is in unsupported format")
