#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import pathlib
import logging

NAME = pathlib.Path(__file__).parent.name
VERSION = "2.0.0"
SCRAPER = f"{NAME} {VERSION}"

CHANNEL = "channel"
PLAYLIST = "playlist"
USER = "user"
ROOT_DIR = pathlib.Path(__file__).parent

logging.basicConfig(format="%(levelname)s:%(message)s")
logger = logging.getLogger("youtube-scraper")


class Youtube(object):
    def __init__(self):
        self.build_dir = None
        self.cache_dir = None
        self.api_key = None

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


YOUTUBE = Youtube()
