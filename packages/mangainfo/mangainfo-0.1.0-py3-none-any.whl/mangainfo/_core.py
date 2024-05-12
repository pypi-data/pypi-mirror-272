from __future__ import annotations

from pathlib import Path

from mangainfo._models import MangaInfo
from mangainfo._utils import parse_all_pages, parse_page, parse_volume


class MangaParser:
    def __init__(self, volume: Path | str) -> None:
        """
        Initialize the MangaParser.

        Parameters
        ----------
        volume : Path | str
            The path to the manga volume file or directory.
        """
        self.volume = Path(volume).expanduser().resolve()

    def full_scan(self) -> MangaInfo:
        """
        Perform a full scan of the manga volume.

        Returns
        -------
        MangaInfo
            Information about the manga volume including all parsed pages.

        Notes
        -----
        Depending on your hardware, this may be slow (~1s) as this will parse every single page in the manga archive.
        """
        return MangaInfo(pages=parse_all_pages(self.volume), **parse_volume(self.volume))  # type: ignore

    def partial_scan(self) -> MangaInfo:
        """
        Perform a partial scan of the manga volume, extracting and parsing
        only the smallest, median, and largest pages.

        Returns
        -------
        MangaInfo
            Information about the manga volume including the parsed smallest,
            median, and largest pages.

        Notes
        -----
        This is roughly 3x faster than `full_scan()`.
        Some methods may return less accurate data because they don't have enough pages to work with.
        """
        from statistics import median_low
        from tempfile import TemporaryDirectory
        from uuid import uuid4

        from archivefile import ArchiveFile

        volume = parse_volume(self.volume)

        with ArchiveFile(self.volume) as archive:
            members = {
                member.size: member.name
                for member in archive.get_members()
                if member.name.lower().endswith((".png", ".jpg", ".jpeg"))
            }
            smallest_file = members[min(members)]
            median_file = members[median_low(members)]
            largest_file = members[max(members)]

            tmp_dir = TemporaryDirectory()
            tmp_path = Path(tmp_dir.name).resolve() / uuid4().hex[:10]

            archive.extractall(destination=tmp_path, members=(smallest_file, median_file, largest_file))

            pages = (
                parse_page(tmp_path / smallest_file, parent=tmp_path),
                parse_page(tmp_path / median_file, parent=tmp_path),
                parse_page(tmp_path / largest_file, parent=tmp_path),
            )

            try:
                tmp_dir.cleanup()
            except:  # noqa: E722; # pragma: no cover
                pass

            return MangaInfo(pages=pages, **volume)  # type: ignore
