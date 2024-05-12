from __future__ import annotations

from mangainfo._core import MangaParser
from mangainfo._models import MangaInfo, PageInfo, Resolution
from mangainfo._version import Version, _get_version

__version__ = _get_version()
__version_tuple__ = Version(*map(int, __version__.split(".")))

__all__ = ["MangaParser", "MangaInfo", "PageInfo", "Resolution"]
