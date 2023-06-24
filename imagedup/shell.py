import argparse
import logging
import sys
from pathlib import Path

from imagedup.duplicates import ImageDupFinder

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="imagedup",
        description="A program to remove image duplicates.",
    )

    parser.add_argument("root", type=str, help="location of a directory with images")
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="do not print file names to the standard output",
    )
    parser.add_argument(
        "-r",
        "--rm",
        action="store_true",
        help="remove image duplicates, by default only prints names",
    )
    parser.add_argument(
        "-a",
        "--min-area",
        default=10000,
        type=float,
        help="a minimum area of an object in pixels within diff of two images",
    )
    parser.add_argument(
        "-s",
        "--min-score",
        default=30000,
        type=float,
        help="a minimum score in pixels used to distinguish a pair of images",
    )

    args = parser.parse_args()

    datapipe = ImageDupFinder(args.root, args.min_score, args.min_area)
    for metadata in datapipe:
        filepath = Path(metadata.filepath)
        if not args.quiet:
            logger.info("%s", filepath.name)
        if args.rm:
            filepath.unlink(missing_ok=True)

    sys.exit(0)


if __name__ == "__main__":
    main()