from __future__ import annotations

import re
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from uuid import uuid4

from archivefile import ArchiveFile
from pymediainfo import MediaInfo


def parse_page(file: Path, parent: Path) -> dict[str, Any]:
    nested: list[dict[str, str]] = MediaInfo.parse(file, full=False).to_data()["tracks"]
    denested = nested[0] | nested[1]

    complete_name = denested.get("complete_name")
    name = Path(complete_name).resolve().relative_to(parent) if complete_name else None
    size = Path(complete_name).stat().st_size if complete_name else None
    extension = Path(complete_name).suffix.strip(".") if complete_name else None
    width = re.sub(r"\D", "", denested["width"]) if denested.get("width") else None
    height = re.sub(r"\D", "", denested["height"]) if denested.get("height") else None
    bit_depth = denested.get("bit_depth").split()[0] if denested.get("bit_depth") else None  # type: ignore

    return dict(
        name=name,
        extension=extension,
        format=denested.get("format"),
        format_info=denested.get("format_info"),
        size=size,
        compression=denested.get("compression"),
        resolution=dict(width=width, height=height),
        color_space=denested.get("color_space"),
        chroma_subsampling=denested.get("chroma_subsampling"),
        bit_depth=bit_depth,
        compression_mode=denested.get("compression_mode"),
    )


def parse_volume(file: Path) -> dict[str, Any]:
    info = MediaInfo.parse(file, full=False).to_data()["tracks"][0]
    name = file.name
    extension = file.suffix.removeprefix(".")
    format = info["format"]
    size = file.stat().st_size

    with ArchiveFile(file) as archive:
        page_count = len(archive.get_names())

    return dict(name=name, extension=extension, format=format, size=size, page_count=page_count)


def parse_all_pages(volume: Path) -> tuple[dict[str, Any], ...]:
    pages = []
    with ArchiveFile(volume) as archive:
        tmp_dir = TemporaryDirectory()
        tmp_path = Path(tmp_dir.name).resolve() / uuid4().hex[:10]
        outdir = archive.extractall(destination=tmp_path).rglob("*.*")
        for file in outdir:
            if file.suffix.lower() in [".png", ".jpg", ".jpeg"]:
                pages.append(parse_page(file, parent=tmp_path))

        try:
            tmp_dir.cleanup()
        except:  # noqa: E722; # pragma: no cover
            pass

        return tuple(pages)
