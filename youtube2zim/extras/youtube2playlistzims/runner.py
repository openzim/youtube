#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

"""
    create project on Google Developer console
    Add Youtube Data API v3 to it
    Create credentials (Other non-UI, Public Data)
"""

import shutil
from pathlib import Path
import subprocess

from ...youtube import (
    get_channel_json,
    credentials_ok,
    Playlist,
    get_channel_playlists_json,
)

from ...constants import logger
from .constants import (
    CHANNELS,
    PLAYLISTS,
    USERS,
)


class Youtube2PlaylistZims(object):
    def __init__(
        self,
        collection_type,
        youtube_ids,
        api_key,
        video_format,
        low_quality,
        nb_videos_per_page,
        all_subtitles,
        autoplay,
        output_dir,
        fname,
        debug,
        keep_build_dir,
        max_concurrency,
        youtube_store,
        language,
        locale_name,
        tags,
        dateafter,
        use_any_optimized_version,
        s3_url_with_credentials,
        title=None,
        description=None,
        creator=None,
        publisher=None,
        name=None,
        profile_image=None,
        banner_image=None,
        main_color=None,
        secondary_color=None,
        only_test_branding=None,
    ):
        # data-retrieval info
        self.collection_type = collection_type
        self.youtube_ids = [yid.strip() for yid in youtube_ids.split(",")]
        self.api_key = api_key
        self.dateafter = dateafter

        # video-encoding info
        self.video_format = video_format
        self.low_quality = low_quality

        # options & zim params
        self.nb_videos_per_page = nb_videos_per_page
        self.all_subtitles = all_subtitles
        self.autoplay = autoplay
        self.fname = fname
        self.language = language
        self.tags = tags
        self.title = title
        self.description = description
        self.creator = creator
        self.publisher = publisher
        self.name = name
        self.profile_image = profile_image
        self.banner_image = banner_image
        self.main_color = main_color
        self.secondary_color = secondary_color
        self.locale_name = locale_name

        # process-related
        self.output_dir = Path(output_dir).expanduser().resolve()
        self.playlists = []
        self.max_concurrency = max_concurrency

        # debug/devel options
        self.debug = debug
        self.keep_build_dir = keep_build_dir

        # update youtube credentials store
        youtube_store.update(api_key=self.api_key, cache_dir=self.cache_dir)

        # Optimization-cache
        self.s3_url_with_credentials = s3_url_with_credentials
        self.use_any_optimized_version = use_any_optimized_version

    @property
    def cache_dir(self):
        return self.output_dir.joinpath("cache")

    @property
    def is_users(self):
        return self.collection_type == USERS

    @property
    def is_channels(self):
        return self.collection_type == CHANNELS

    @property
    def is_playlists(self):
        return self.collection_type == PLAYLISTS

    

    def extract_playlists(self):
        """ prepare a list of Playlist from user request

            USER: we fetch the hidden channel associate to it
            CHANNEL (and USER): we grab all playlists + `uploads` playlist
            PLAYLIST: we retrieve from the playlist Id(s) """

        playlist_ids = []
        if self.is_users or self.is_channels:
            for youtube_id in self.youtube_ids:
                if self.is_users:
                    # youtube_id is a Username, fetch actual channelId through channel
                    channel_json = get_channel_json(youtube_id, for_username=True)
                else:
                    # youtube_id is a channelId
                    channel_json = get_channel_json(youtube_id)

                # retrieve list of playlists for that channel
                playlist_ids += [
                    p["id"] for p in get_channel_playlists_json(self.main_channel_id)
                ]
        elif self.is_playlists:
            playlist_ids = self.youtube_ids
        else:
            raise NotImplementedError("unsupported collection_type")

        self.playlists = [
            Playlist.from_id(playlist_id) for playlist_id in list(set(playlist_ids))
        ]

    def run_youtube2zim(self):
        for playlist in self.playlists:
            param_map = [("optimization-cache", "s3_url_with_credentials"),
            ("use-any-optimized-version", "use_any_optimized_version"),
            ("dateafter", "dateafter"),
            ("concurrency", "max_concurrency"),
            ("keep", "keep_build_dir"),
            ("debug", "debug"),
            ("secondary-color", "secondary_color"),
            ("main-color", "main_color"),
            ("banner", "banner_image"),
            ("profile", "profile_image"),
            ("tags", "tags"),
            ("publisher", "publisher"),
            ("language", "language"),
            ("autoplay", "autoplay"),
            ("locale", "locale_name"),
            ("pagination", "nb_videos_per_page"),
            ("all-subtitles", "all_subtitles"),
            ("low-quality", "low_quality"),
            ("format", "video_format"),
            ("api-key", "api_key")
            ]
            args = ["youtube2zim"]

            # set directly passed arguments
            for key, attr in param_map:
                if key not in ["keep", "debug", "all-subtitles", "low-quality"]:
                    val = getattr(self, attr)
                    if val:
                        args += [f"--{key}={str(val)}"]
                else:
                    if getattr(self, attr):
                        args += [f"--{key}"]

            # set dynamically passed arguments
            playlist_output_dir = self.output_dir.joinpath(playlist.playlist_id)
            args += [f"--id={playlist.playlist_id}"]
            args += [f"--output={str(playlist_output_dir)}"]
            name = self.name + f"playlist_{playlist.playlist_id}"
            args += [f"--name=\"{name}\""]
            
            args += [f"--zim-file={playlist.playlist_id}"]
            args += [f"--title='{playlist.title}'"]
            args += [f"--description='{playlist.description}'"]
            args += [f"--creator='{playlist.creator_name}'"]
            args += [f"--type=playlist"]


            logger.debug(args)
            subprocess.run(args, check=True)
            logger.info(f"youtube2zim successfully created zim for playlist {playlist.playlist_id}")
            logger.debug(f"Moving ZIM to output directory")

            zim = playlist.title.replace(" ", "_")
            if self.fname:
                fname = self.fname + f"_{zim}"
            else:
                fname = zim
            shutil.move(playlist_output_dir.joinpath(f"{playlist.playlist_id}.zim"), self.output_dir.joinpath(f"{fname}.zim"))
            
            
            
            # shutil.move(playlist_output_dir.glob("*.zim"), )

    def run(self):
        """ execute the runner step by step """

        logger.info(
            f"starting youtube2playlistzims for {self.collection_type} - {self.youtube_ids}"
        )
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir, ignore_errors=True)
        self.cache_dir.mkdir(parents=True)

        logger.info("testing Youtube credentials")
        if not credentials_ok():
            raise ValueError("Unable to connect to Youtube API v3. check `API_KEY`.")

        logger.info("compute playlists list to retrieve")
        self.extract_playlists()

        logger.info(
            ".. {} playlists:\n   {}".format(
                len(self.playlists),
                "\n   ".join([p.playlist_id for p in self.playlists]),
            )
        )

        self.run_youtube2zim()
        shutil.rmtree(self.cache_dir, ignore_errors=True)
        logger.info("All done")

