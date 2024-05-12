from __future__ import annotations

import argparse
from pathlib import Path

from mangainfo._core import MangaParser


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="mangainfo", description="Generate mediainfo-esque text from a manga archive."
    )
    parser.add_argument("path", type=Path, help="Path to a manga archive.")
    parser.add_argument("--full", action="store_true", help="Scan every page. More accurate data but far slower.")

    args = parser.parse_args()

    path = args.path.expanduser().resolve()

    if args.full:
        print(MangaParser(path).full_scan().mediainfo())
    else:
        print(MangaParser(path).partial_scan().mediainfo())


if __name__ == "__main__":
    main()
