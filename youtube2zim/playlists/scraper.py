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

import sys
import json
import shutil
import pathlib
import tempfile
import subprocess

import requests
from zimscraperlib.logging import nicer_args_join

from ..constants import logger, NAME, YOUTUBE, PLAYLIST
from ..youtube import extract_playlists_details_from, credentials_ok


class YoutubeHandler(object):
    def __init__(
        self,
        options,
        extra_args,
    ):
        # save options as properties
        for key, value in options.items():
            setattr(self, key, value)
        self.extra_args = extra_args

        self.build_dir = pathlib.Path(tempfile.mkdtemp())

        # metadata_from JSON file
        self.metadata_from = (
            pathlib.Path(self.metadata_from) if self.metadata_from else None
        )
        self.metadata = {}  # custom metadata holder

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
        cmd = "youtube2zim"
        dev_cmd = f"{cmd}/playlists"
        if sys.argv[0] == dev_cmd:
            return [sys.executable, cmd]
        return [sys.argv[0].replace(f"{cmd}-playlists", cmd)]

    def run(self):
        # drop directly to regular youtube2zim if not requesting indiv playlits zims
        if not self.playlists_mode:
            shutil.rmtree(self.build_dir, ignore_errors=True)  # not needed
            return self.handle_single_zim()

        logger.info(
            f"starting all-playlits {NAME} scraper for {self.collection_type}#{self.youtube_id}"
        )

        # create required sub folders
        for sub_folder in ("cache", "videos", "channels"):
            self.build_dir.joinpath(sub_folder).mkdir()

        logger.info("testing Youtube credentials")
        if not credentials_ok():
            raise ValueError("Unable to connect to Youtube API v3. check `API_KEY`.")

        self.fetch_metadata()

        logger.info("compute playlists list to retrieve")
        (
            playlists,
            main_channel_id,
            uploads_playlist_id,
        ) = extract_playlists_details_from(self.collection_type, self.youtube_id)

        logger.info(
            ".. {} playlists:\n   {}".format(
                len(playlists),
                "\n   ".join([p.playlist_id for p in playlists]),
            )
        )

        # no need for build_dir anymore
        shutil.rmtree(self.build_dir, ignore_errors=True)

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
        ]
        if self.debug:
            args.append("--debug")

        # set metadata args for playlist
        metadata = self.metadata.get(playlist_id, {})
        for key in (
            "name",
            "zim-file",
            "title",
            "description",
            "tags",
            "creator",
            "profile",
            "banner",
        ):
            # use value from metadata JSON if present else from command-line
            value = metadata.get(
                key, getattr(self, f"playlists_{key.replace('-', '_')}", None)
            )

            if value:  # only set arg if we have a value so it can be defaulted
                # format value using playlists' variables
                args += [f"--{key}", self.compute_format(playlist, str(value))]

        # append regular youtube2zim args
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
            ]
            + self.extra_args
        )
        if self.debug:
            args.append("--debug")
        sys.exit(subprocess.run(args).returncode)

    @staticmethod
    def compute_format(playlist, fmt):
        return fmt.format(**playlist.__dict__(), **{"period": "{period}"})

    def fetch_metadata(self):
        """ retrieves and loads metadata from --metadata-from """

        if not self.metadata_from:
            return

        logger.info(f"Retrieving custom metadata from {self.metadata_from}")
        # load JSON from source (URL or file)
        try:
            if str(self.metadata_from).startswith("http"):
                self.metadata = requests.get(str(self.metadata_from)).json()
            else:
                if not self.metadata_from.exists():
                    raise IOError(
                        f"--metadata-from file could not be found: {self.metadata_from}"
                    )
                with open(self.metadata_from, "r") as fh:
                    self.metadata = json.load(fh)
        except Exception as exc:
            logger.debug(exc)
            raise ValueError(
                f"--metadata-from could not be loaded as JSON: {self.metadata_from}"
            )

        # ensure the basic format is respected: dict of playlist ID to dict of meta
        if not isinstance(self.metadata, dict) or len(self.metadata) != sum(
            [
                1
                for k, v in self.metadata.items()
                if isinstance(k, str) and isinstance(v, dict)
            ]
        ):
            raise ValueError("--metadata-from JSON is of unexpected format")
