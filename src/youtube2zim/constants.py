#!/usr/bin/env python3
# vim: ai ts=4 sts=4 et sw=4 nu

import logging
from pathlib import Path

from zimscraperlib.logging import getLogger

from youtube2zim.__about__ import __version__

ROOT_DIR = Path(__file__).parent
NAME = ROOT_DIR.name

SCRAPER = f"{NAME} {__version__}"

CHANNEL = "channel"
PLAYLIST = "playlist"
USER = "user"

# Youtube uses some non-standard language codes
YOUTUBE_LANG_MAP = {
    "iw": "he",  # Hebrew
    "es-419": "es",  # Spanish
    "zh-Hans-CN": "zh-cn",  # Chinese
    "zh-Hant-TW": "zh-tw",  # Chinese
    "zh-Hant-HK": "zh-hk",  # Chinese
    "zh-Hans-SG": "zh-sg",  # Chinese
    "mo": "ro",  # Romanian
    "sh": "srp",  # Serbian
}

logger = getLogger(NAME, level=logging.DEBUG)


class Youtube:
    build_dir: Path
    cache_dir: Path
    api_key: str


YOUTUBE = Youtube()
