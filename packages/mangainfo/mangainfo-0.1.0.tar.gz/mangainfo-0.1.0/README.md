# mangainfo

<div align="center">

[![PyPI - Version](https://img.shields.io/pypi/v/mangainfo?link=https%3A%2F%2Fpypi.org%2Fproject%2Fmangainfo%2F)](https://pypi.org/project/mangainfo/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mangainfo)
![License](https://img.shields.io/github/license/Ravencentric/mangainfo)
![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Ravencentric/mangainfo/release.yml)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ravencentric/mangainfo/test.yml?label=tests)
[![codecov](https://codecov.io/gh/Ravencentric/mangainfo/graph/badge.svg?token=6W8R2NKWIQ)](https://codecov.io/gh/Ravencentric/mangainfo)

</div>

## Table Of Contents

* [About](#about)
* [Installation](#installation)
* [Docs](#docs)
* [License](#license)

## About

`mangainfo` is both a library and CLI tool to generate mediainfo for manga archives. This relies on [archivefile](https://ravencentric.github.io/archivefile/) for reading the archives and [pymediainfo](https://pymediainfo.readthedocs.io/en/stable/) for generating the mediainfo.

## Installation

`mangainfo` is available on [PyPI](https://pypi.org/project/mangainfo/), so you can simply use [pip](https://github.com/pypa/pip) to install it.

```sh
pip install mangainfo
```

## Usage

As a library:

```py
from mangainfo import MangaParser

archive = "~/Blue Box (Digital) (1r0n)/Blue Box v06 (2023) (Digital) (1r0n).cbz"

manga = MangaParser(archive).partial_scan()

for page in manga.pages:
    print(page.resolution)
```

As a CLI:

```sh
❯ mangainfo --help
usage: mangainfo [-h] [--full] path

Generate mediainfo-esque text from a manga archive.

positional arguments:
  path        Path to a manga archive.

options:
  -h, --help  show this help message and exit
  --full      Scan every page. More accurate data but far slower.
```

Refer to the [API reference](https://ravencentric.github.io/mangainfo/api-reference/mangaparser/) for more details.

## Docs

Checkout the complete documentation [here](https://ravencentric.github.io/mangainfo/).

## License

Distributed under the [Unlicense](https://choosealicense.com/licenses/unlicense/) License. See [UNLICENSE](https://github.com/Ravencentric/mangainfo/blob/main/UNLICENSE) for more information.
