#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import subprocess

from .constants import SCRAPER, logger
from .utils import nicer_args_join


class ZimInfo(object):
    def __init__(
        self,
        language="eng",
        title="my title",
        description="my zim description",
        creator="youtube",
        publisher="kiwix",
        name="youtube-test",
        tags=[],
        homepage="home.html",
        favicon="favicon.jpg",
        scraper=SCRAPER,
    ):

        self.homepage = homepage
        self.favicon = favicon
        self.language = language
        self.title = title
        self.description = description
        self.creator = creator
        self.publisher = publisher
        self.name = name
        self.tags = tags
        self.scraper = scraper

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_zimwriterfs_args(self):
        return [
            "--welcome",
            self.homepage,
            "--favicon",
            self.favicon,
            "--language",
            self.language,
            "--title",
            self.title,
            "--description",
            self.description,
            "--creator",
            self.creator,
            "--publisher",
            self.publisher,
            "--name",
            self.name,
            "--tags",
            ";".join(self.tags),
            "--scraper",
            self.scraper,
        ]


def make_zim_file(build_dir, output_dir, zim_fname, zim_info):
    """ runs zimwriterfs """
    args = (
        ["zimwriterfs"]
        + zim_info.to_zimwriterfs_args()
        + ["--verbose", str(build_dir), str(output_dir.joinpath(zim_fname))]
    )

    logger.debug(nicer_args_join(args))
    zimwriterfs = subprocess.run(args)
    zimwriterfs.check_returncode()
