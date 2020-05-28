#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

"""
    Youtube Playlists to individual ZIMs scraper

    Invokes youtube2zim scraper individally for each playlist
    Also forwards regular requests to youtube2zim (can be used as generic entrypoint)

    - Uploads playlist (all videos of the channel) is excluded
    - Only displays youtube2zim's output on failure
"""

import re
import sys
import shutil
import pathlib
import subprocess

from zimscraperlib.logging import nicer_args_join

from ..constants import logger, NAME, YOUTUBE, PLAYLIST
from ..youtube import extract_playlists_details_from, credentials_ok
from ..utils import make_build_folder


class YoutubeHandler(object):
    def __init__(
        self, options, extra_args,
    ):
        # save options as properties
        for key, value in options.items():
            setattr(self, key, value)
        self.extra_args = extra_args

        self.output_dir = pathlib.Path(self.output_dir).expanduser().resolve()
        self.build_dir = self.output_dir.joinpath("build")

        # update youtube credentials store
        YOUTUBE.update(
            build_dir=self.build_dir,
            api_key=self.api_key,
            cache_dir=self.build_dir.joinpath("cache"),
        )

    @property
    def youtube2zim_exe(self):
        """ youtube2zim executable """

        # handle either `python youtube2zim` and `youtube2zim`
        executable = pathlib.Path(sys.executable)
        if re.match(r"python[0-9]*", executable.name):
            return [str(executable), "youtube2zim"]
        return [str(executable)]

    def run(self):
        # drop directly to regular youtube2zim if not requesting indiv playlits zims
        if not self.playlists_mode:
            return self.handle_single_zim()

        logger.info(
            f"starting all-playlits {NAME} scraper for {self.collection_type}#{self.youtube_id}"
        )

        # prepare main build dir (only for cache playlists computation data)
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir, ignore_errors=True)
        make_build_folder(self.build_dir)

        logger.info("testing Youtube credentials")
        if not credentials_ok():
            raise ValueError("Unable to connect to Youtube API v3. check `API_KEY`.")

        logger.info("compute playlists list to retrieve")
        (
            playlists,
            main_channel_id,
            uploads_playlist_id,
        ) = extract_playlists_details_from(self.collection_type, self.youtube_id)

        logger.info(
            ".. {} playlists:\n   {}".format(
                len(playlists), "\n   ".join([p.playlist_id for p in playlists]),
            )
        )

        for playlist in playlists:
            if playlist.playlist_id == uploads_playlist_id:
                logger.info(f"Skipping playlist {playlist.playlist_id} (uploads one)")
                continue

            logger.info(f"Executing youtube2zim for playlist {playlist.playlist_id}")
            success, process = self.run_playlist_zim(playlist)
            if success:
                logger.info(".. OK")
            else:
                logger.error(".. ERROR. Printing scraper output and exiting.")
                logger.error(process.stdout)
                return process.returncode

    def run_playlist_zim(self, playlist):
        """ run youtube2zim for an individual playlist """

        playlist_id = playlist.playlist_id
        args = self.youtube2zim_exe + [
            "--type",
            PLAYLIST,
            "--id",
            playlist_id,
            "--api-key",
            self.api_key,
            "--output",
            str(self.output_dir.joinpath("playlists", playlist_id)),
            "--name",
            self.compute_format(playlist, self.playlists_name),
        ]

        if self.playlists_title:
            args += ["--title", self.compute_format(playlist, self.playlists_title)]

        if self.playlists_description:
            args += [
                "--description",
                self.compute_format(playlist, self.playlists_description),
            ]

        args += self.extra_args

        logger.debug(nicer_args_join(args))
        process = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        return process.returncode == 0, process

    def handle_single_zim(self):
        """ redirect request to standard youtube2zim """

        args = (
            self.youtube2zim_exe
            + [
                "--type",
                self.collection_type,
                "--id",
                self.youtube_id,
                "--api-key",
                self.api_key,
                "--output",
                self.output_dir,
            ]
            + self.extra_args
        )
        sys.exit(subprocess.run(args).returncode)

    @staticmethod
    def compute_format(playlist, fmt):
        return fmt.format(**playlist.__dict__())
