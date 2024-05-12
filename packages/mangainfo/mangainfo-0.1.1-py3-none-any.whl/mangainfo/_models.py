from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, ByteSize, ValidationInfo, field_validator


class Resolution(BaseModel):
    """Resolution of the image in pixels"""

    width: int = 0
    height: int = 0

    def as_str(self) -> str:
        """Return a human-readable representation of the resolution in the format: `{width}x{height}`"""
        return f"{self.width}x{self.height}"

    def as_tuple(self) -> tuple[int, int]:
        """Return the resolution as a tuple of integers: `(width, height)`"""
        return (self.width, self.height)

    def is_portrait(self) -> bool:
        """Check if the resolution is portrait."""
        return self.height > self.width

    def is_landscape(self) -> bool:
        """Check if the resolution is landscape."""
        return self.width > self.height

    def __str__(self) -> str:
        return self.as_str()

    def __hash__(self) -> int:
        return hash(self.as_str())


class PageInfo(BaseModel):
    """
    Media information about the page,
    as returned by [pymediainfo.MediaInfo](https://pymediainfo.readthedocs.io/en/stable/pymediainfo.html#pymediainfo.MediaInfo).
    """

    name: Path
    """Name of the page."""

    extension: str
    """Extension of the page."""

    format: str
    """Format of the page."""

    format_info: str | None = None
    """Additional information about the format."""

    size: ByteSize = ByteSize(0)
    """Size of the page"""

    compression: str | None = None
    """Compression method used on the page."""

    resolution: Resolution = Resolution()
    """Resolution of the page."""

    color_space: str | None = None
    """Color space of the page."""

    chroma_subsampling: str | None = None
    """Chroma subsampling."""

    bit_depth: int
    """Bit depth."""

    compression_mode: str | None = None
    """Type of compression used on the page."""

    @field_validator("*", mode="before")
    @classmethod
    def _replace_none_with_default(cls, v: str, info: ValidationInfo) -> Any:
        if v is None:
            return cls.model_fields[info.field_name].default
        return v


class MangaInfo(BaseModel):
    """
    Media information about the manga archive,
    as returned by [pymediainfo.MediaInfo](https://pymediainfo.readthedocs.io/en/stable/pymediainfo.html#pymediainfo.MediaInfo).
    """

    name: Path
    """Name of the volume archive."""

    extension: str
    """Extension of the volume archive."""

    format: str
    """Format of the volume archive."""

    size: ByteSize = ByteSize(0)
    """Size of the volume archive."""

    page_count: int = 0
    """Number of pages in the volume archive."""

    pages: tuple[PageInfo, ...] = tuple()
    """
    A tuple of `PageInfo` objects representing the pages inside the volume archive.
    If `partial_scan()` was called, then this  will only have a maximum of 3 pages: smallest, median, and largest. 
    If `full_scan()` was called, then this will have have a `PageInfo` object for every page in the archive.
    """

    @field_validator("*", mode="before")
    @classmethod
    def _replace_none_with_default(cls, v: str, info: ValidationInfo) -> Any:
        if v is None:
            return cls.model_fields[info.field_name].default  # pragma: no cover
        return v

    def smallest_page(self) -> PageInfo:
        """
        Find the smallest page in the archive by size.

        Returns
        -------
        PageInfo
            The smallest page in the archive.
        """
        return min(self.pages, key=lambda page: page.size)

    def median_page(self) -> PageInfo:
        """
        Find the median page in the archive by size.

        Returns
        -------
        PageInfo
            The median page in the archive.
        """
        from statistics import median_low

        data = {page.size: page for page in self.pages}
        return data[median_low(data.keys())]

    def largest_page(self) -> PageInfo:
        """
        Find the largest page in the archive by size.

        Returns
        -------
        PageInfo
            The largest page in the archive.
        """
        return max(self.pages, key=lambda page: page.size)

    def average_page_size(self) -> ByteSize:
        """
        Calculate the average page size of the volume archive.

        Returns
        -------
        ByteSize
            The average page size of the volume archive.
        """

        data = [page.size for page in self.pages]
        return ByteSize(sum(data) / len(data))

    def unique_resolutions(self) -> tuple[tuple[Resolution, int], ...]:
        """
        Count the occurrences of unique resolutions in the archive.

        Returns
        -------
        tuple[tuple[Resolution, int], ...]
            A tuple of tuples containing unique resolutions and their counts,
            sorted by frequency in descending order.
        """
        from collections import Counter

        return tuple(Counter(page.resolution for page in self.pages).most_common())

    def mediainfo(self) -> str:
        """
        Generate a mediainfo-esque string describing the archive,
        including information about the smallest, median, and largest pages in the archive.

        Returns
        -------
        str
            A string formatted similarly to mediainfo output,
            providing information about the archive.
        """
        volume_info = "Volume\n"
        data = self.model_dump(exclude_defaults=True, exclude_none=True, exclude_unset=True)
        pages = data.pop("pages")

        for key, value in data.items():
            if key == "size":
                value = ByteSize(value).human_readable(separator=" ")

            key = key.replace("_", " ").title()
            volume_info += f"{key:<20}: {value}\n"

        volume_info += f"{'Average Page Size':<20}: {self.average_page_size().human_readable(separator=' ')}\n"

        if len(pages) > 3:
            page_info = ""
            volume_info += f"{'Unique Resolutions':<20}: {', '.join(f'{resolution}: {count}' for resolution, count in self.unique_resolutions())}"
            for index, page in enumerate((self.smallest_page(), self.median_page(), self.largest_page()), start=1):
                page_info += f"\n\nPage #{index}\n"
                for key, value in page.model_dump(exclude_defaults=True, exclude_none=True, exclude_unset=True).items():
                    if key == "size":
                        value = ByteSize(value).human_readable(separator=" ")
                    if key == "resolution":
                        value = Resolution(width=value["width"], height=value["height"]).as_str()

                    key = key.replace("_", " ").title()
                    page_info += f"{key:<20}: {value}\n"

        elif len(pages) >= 1 and len(pages) <= 3:
            page_info = ""
            for index, page in enumerate(self.pages, start=1):
                page_info += f"\n\nPage #{index}\n"
                for key, value in page.model_dump(exclude_defaults=True, exclude_none=True, exclude_unset=True).items():
                    if key == "size":
                        value = ByteSize(value).human_readable(separator=" ")
                    if key == "resolution":
                        value = Resolution(width=value["width"], height=value["height"]).as_str()

                    key = key.replace("_", " ").title()
                    page_info += f"{key:<20}: {value}\n"

        else:  # pragma: no cover
            page_info = ""

        return f"{volume_info}{page_info}".strip()
