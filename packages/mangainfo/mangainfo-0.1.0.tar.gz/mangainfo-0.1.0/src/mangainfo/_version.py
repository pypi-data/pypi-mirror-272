from __future__ import annotations

import sys

from typing_extensions import NamedTuple

if sys.version_info >= (3, 10):
    from importlib import metadata
else:
    import importlib_metadata as metadata


class Version(NamedTuple):
    """Version tuple based on SemVer"""

    major: int
    """Major version number"""
    minor: int
    """Minor version number"""
    patch: int
    """Patch version number"""


def _get_version() -> str:
    """
    Get the version of archivefile
    """
    try:
        return metadata.version("archivefile")

    except metadata.PackageNotFoundError:
        return "0.0.0"
