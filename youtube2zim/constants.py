#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import pathlib
import logging

from zimscraperlib.logging import getLogger

ROOT_DIR = pathlib.Path(__file__).parent
NAME = ROOT_DIR.name

with open(ROOT_DIR.joinpath("VERSION"), "r") as fh:
    VERSION = fh.read().strip()

SCRAPER = f"{NAME} {VERSION}"

CHANNEL = "channel"
PLAYLIST = "playlist"
USER = "user"

# Youtube uses some non-standard language codes
YOUTUBE_LANG_MAP = {"iw": "he", "es-419": "es"}

logger = getLogger(NAME, level=logging.DEBUG)


class Youtube(object):
    def __init__(self):
        self.build_dir = None
        self.cache_dir = None
        self.api_key = None

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


YOUTUBE = Youtube()
