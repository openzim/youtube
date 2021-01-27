#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

"""
    create project on Google Developer console
    Add Youtube Data API v3 to it
    Create credentials (Other non-UI, Public Data)
"""

import os
import json
import locale
import shutil
import tempfile
import subprocess
import datetime
import functools
from pathlib import Path
import concurrent.futures
from gettext import gettext as _

import jinja2
import youtube_dl
from pif import get_public_ip
from babel.dates import format_date
from dateutil import parser as dt_parser
from kiwixstorage import KiwixStorage
from zimscraperlib.download import stream_file
from zimscraperlib.zim import make_zim_file
from zimscraperlib.fix_ogvjs_dist import fix_source_dir
from zimscraperlib.image.presets import WebpHigh
from zimscraperlib.image.transformation import resize_image
from zimscraperlib.image.probing import get_colors, is_hex_color
from zimscraperlib.video.presets import VideoWebmLow, VideoMp4Low
from zimscraperlib.i18n import get_language_details, setlocale

from .youtube import (
    get_channel_json,
    credentials_ok,
    extract_playlists_details_from,
    get_videos_json,
    get_videos_authors_info,
    save_channel_branding,
    skip_deleted_videos,
    skip_outofrange_videos,
)
from .utils import clean_text, load_json, save_json, get_slug
from .processing import post_process_video, process_thumbnail
from .constants import (
    logger,
    ROOT_DIR,
    CHANNEL,
    PLAYLIST,
    USER,
    SCRAPER,
    YOUTUBE_LANG_MAP,
)


class Youtube2Zim:
    def __init__(
        self,
        collection_type,
        youtube_id,
        api_key,
        video_format,
        low_quality,
        nb_videos_per_page,
        all_subtitles,
        autoplay,
        output_dir,
        no_zim,
        fname,
        debug,
        tmp_dir,
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
    ):
        # data-retrieval info
        self.collection_type = collection_type
        self.youtube_id = youtube_id
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
        self.tags = [t.strip() for t in tags.split(",")]
        self.title = title
        self.description = description
        self.creator = creator
        self.publisher = publisher
        self.name = name
        self.profile_image = profile_image
        self.banner_image = banner_image
        self.main_color = main_color
        self.secondary_color = secondary_color

        # directory setup
        self.output_dir = Path(output_dir).expanduser().resolve()
        if tmp_dir:
            tmp_dir = Path(tmp_dir).expanduser().resolve()
            tmp_dir.mkdir(parents=True, exist_ok=True)
        self.build_dir = Path(tempfile.mkdtemp(dir=tmp_dir))

        # process-related
        self.playlists = []
        self.uploads_playlist_id = None
        self.videos_ids = []
        self.main_channel_id = None  # use for branding

        # debug/devel options
        self.no_zim = no_zim
        self.debug = debug
        self.keep_build_dir = keep_build_dir
        self.max_concurrency = max_concurrency

        # update youtube credentials store
        youtube_store.update(
            build_dir=self.build_dir, api_key=self.api_key, cache_dir=self.cache_dir
        )

        # Optimization-cache
        self.s3_url_with_credentials = s3_url_with_credentials
        self.use_any_optimized_version = use_any_optimized_version
        self.video_quality = "low" if self.low_quality else "high"
        self.s3_storage = None

        # set and record locale for translations
        locale_name = locale_name or get_language_details(self.language)["iso-639-1"]
        try:
            self.locale = setlocale(ROOT_DIR, locale_name)
        except locale.Error:
            logger.error(
                f"No locale for {locale_name}. Use --locale to specify it. defaulting to en_US"
            )
            self.locale = setlocale(ROOT_DIR, "en")

    @property
    def root_dir(self):
        return ROOT_DIR

    @property
    def templates_dir(self):
        return self.root_dir.joinpath("templates")

    @property
    def assets_src_dir(self):
        return self.templates_dir.joinpath("assets")

    @property
    def assets_dir(self):
        return self.build_dir.joinpath("assets")

    @property
    def channels_dir(self):
        return self.build_dir.joinpath("channels")

    @property
    def cache_dir(self):
        return self.build_dir.joinpath("cache")

    @property
    def videos_dir(self):
        return self.build_dir.joinpath("videos")

    @property
    def profile_path(self):
        return self.build_dir.joinpath("profile.jpg")

    @property
    def banner_path(self):
        return self.build_dir.joinpath("banner.jpg")

    @property
    def is_user(self):
        return self.collection_type == USER

    @property
    def is_channel(self):
        return self.collection_type == CHANNEL

    @property
    def is_playlist(self):
        return self.collection_type == PLAYLIST

    @property
    def is_single_channel(self):
        if self.is_channel or self.is_user:
            return True
        return len(list(set([pl.creator_id for pl in self.playlists]))) == 1

    @property
    def sorted_playlists(self):
        """ sorted list of playlists (by title) but with Uploads one at first if any """
        if len(self.playlists) < 2:
            return self.playlists

        sorted_playlists = sorted(self.playlists, key=lambda x: x.title)
        index = 0
        # make sure our Uploads, special playlist is first
        if self.uploads_playlist_id:
            try:
                index = [
                    index
                    for index, p in enumerate(sorted_playlists)
                    if p.playlist_id == self.uploads_playlist_id
                ][-1]
            except Exception:
                index = 0
        return (
            [sorted_playlists[index]]
            + sorted_playlists[0:index]
            + sorted_playlists[index + 1 :]
        )

    def run(self):
        """ execute the scraper step by step """

        self.validate_id()

        # validate dateafter input
        self.validate_dateafter_input()

        logger.info(
            f"starting youtube scraper for {self.collection_type}#{self.youtube_id}"
        )
        logger.info("preparing build folder at {}".format(self.build_dir.resolve()))
        self.prepare_build_folder()

        logger.info("testing Youtube credentials")
        if not credentials_ok():
            raise ValueError("Unable to connect to Youtube API v3. check `API_KEY`.")

        if self.s3_url_with_credentials and not self.s3_credentials_ok():
            raise ValueError("Unable to connect to Optimization Cache. Check its URL.")

        # fail early if supplied branding files are missing
        self.check_branding_values()

        logger.info("compute playlists list to retrieve")
        self.extract_playlists()

        logger.info(
            ".. {} playlists:\n   {}".format(
                len(self.playlists),
                "\n   ".join([p.playlist_id for p in self.playlists]),
            )
        )

        logger.info("compute list of videos")
        self.extract_videos_list()

        nb_videos_msg = f".. {len(self.videos_ids)} videos"
        if self.dateafter.start.year != 1:
            nb_videos_msg += (
                f" in date range: {self.dateafter.start} - {datetime.date.today()}"
            )
        logger.info(f"{nb_videos_msg}.")

        # download videos (and recompress)
        logger.info(
            f"downloading all videos, subtitles and thumbnails (concurrency={self.max_concurrency})"
        )
        logger.info(f"  format: {self.video_format}")
        logger.info(f"  quality: {self.video_quality}")
        logger.info(f"  generated-subtitles: {self.all_subtitles}")
        if self.s3_storage:
            logger.info(
                f"  using cache: {self.s3_storage.url.netloc} with bucket: {self.s3_storage.bucket_name}"
            )
        succeeded, failed = self.download_video_files(
            max_concurrency=self.max_concurrency
        )
        if failed:
            logger.error(f"{len(failed)} video(s) failed to download: {failed}")
            if len(failed) >= len(succeeded):
                logger.critical("More than half of videos failed. exiting")
                raise IOError("Too much videos failed to download")

        logger.info("retrieve channel-info for all videos (author details)")
        get_videos_authors_info(succeeded)

        logger.info("download all author's profile pictures")
        self.download_authors_branding()

        logger.info("update general metadata")
        self.update_metadata()

        logger.info("creating HTML files")
        self.make_html_files(succeeded)

        # make zim file
        os.makedirs(self.output_dir, exist_ok=True)
        if not self.no_zim:
            period = datetime.datetime.now().strftime("%Y-%m")
            self.fname = (
                self.fname.format(period=period)
                if self.fname
                else f"{self.name}_{period}.zim"
            )
            logger.info("building ZIM file")
            make_zim_file(
                build_dir=self.build_dir,
                fpath=self.output_dir / self.fname,
                name=self.name,
                main_page="home.html",
                favicon="favicon.jpg",
                title=self.title,
                description=self.description,
                language=self.language,
                creator=self.creator,
                publisher="Kiwix",
                tags=self.tags,
                scraper=SCRAPER,
            )

            if not self.keep_build_dir:
                logger.info("removing temp folder")
                shutil.rmtree(self.build_dir, ignore_errors=True)

        logger.info("all done!")

    def s3_credentials_ok(self):
        logger.info("testing S3 Optimization Cache credentials")
        self.s3_storage = KiwixStorage(self.s3_url_with_credentials)
        if not self.s3_storage.check_credentials(
            list_buckets=True, bucket=True, write=True, read=True, failsafe=True
        ):
            logger.error("S3 cache connection error testing permissions.")
            logger.error(f"  Server: {self.s3_storage.url.netloc}")
            logger.error(f"  Bucket: {self.s3_storage.bucket_name}")
            logger.error(f"  Key ID: {self.s3_storage.params.get('keyid')}")
            logger.error(f"  Public IP: {get_public_ip()}")
            return False
        return True

    def validate_dateafter_input(self):
        try:
            self.dateafter = youtube_dl.DateRange(self.dateafter)
        except Exception as exc:
            logger.error(
                f"Invalid dateafter input. Valid dateafter format: "
                f"YYYYMMDD or (now|today)[+-][0-9](day|week|month|year)(s)."
            )
            raise ValueError(f"Invalid dateafter input: {exc}")

    def validate_id(self):
        # space not allowed in youtube-ID
        self.youtube_id = self.youtube_id.replace(" ", "")
        if self.collection_type == "channel" and len(self.youtube_id) > 24:
            raise ValueError("Invalid ChannelId")
        if "," in self.youtube_id and self.collection_type != "playlist":
            raise ValueError("Invalid YoutubeId")

    def prepare_build_folder(self):
        """ prepare build folder before we start downloading data """

        # copy assets
        shutil.copytree(self.assets_src_dir, self.assets_dir)

        fix_source_dir(self.assets_dir, "assets")

        # cache folder to store youtube-api results
        self.cache_dir.mkdir(exist_ok=True)

        # make videos placeholder
        self.videos_dir.mkdir(exist_ok=True)

        # make channels placeholder (profile files)
        self.channels_dir.mkdir(exist_ok=True)

    def check_branding_values(self):
        """checks that user-supplied images and colors are valid (so to fail early)

        Images are checked for existence or downloaded then resized
        Colors are check for validity"""

        # skip this step if none of related values were supplied
        if not sum(
            [
                bool(x)
                for x in (
                    self.profile_image,
                    self.banner_image,
                    self.main_color,
                    self.secondary_color,
                )
            ]
        ):
            return
        logger.info("checking your branding files and values")
        if self.profile_image:
            if self.profile_image.startswith("http"):
                stream_file(self.profile_image, self.profile_path)
            else:
                if not self.profile_image.exists():
                    raise IOError(
                        f"--profile image could not be found: {self.profile_image}"
                    )
                shutil.move(self.profile_image, self.profile_path)
            resize_image(self.profile_path, width=100, height=100, method="thumbnail")
        if self.banner_image:
            if self.banner_image.startswith("http"):
                stream_file(self.banner_image, self.banner_path)
            else:
                if not self.banner_image.exists():
                    raise IOError(
                        f"--banner image could not be found: {self.banner_image}"
                    )
                shutil.move(self.banner_image, self.banner_path)
            resize_image(self.banner_path, width=1060, height=175, method="thumbnail")

        if self.main_color and not is_hex_color(self.main_color):
            raise ValueError(
                f"--main-color is not a valid hex color: {self.main_color}"
            )

        if self.secondary_color and not is_hex_color(self.secondary_color):
            raise ValueError(
                f"--secondary_color-color is not a valid hex color: {self.secondary_color}"
            )

    def extract_playlists(self):
        """prepare a list of Playlist from user request

        USER: we fetch the hidden channel associate to it
        CHANNEL (and USER): we grab all playlists + `uploads` playlist
        PLAYLIST: we retrieve from the playlist Id(s)"""

        (
            self.playlists,
            self.main_channel_id,
            self.uploads_playlist_id,
        ) = extract_playlists_details_from(self.collection_type, self.youtube_id)

    def extract_videos_list(self):
        all_videos = load_json(self.cache_dir, "videos")
        if all_videos is None:
            all_videos = {}

            # we only return video_ids that we'll use later on. per-playlist JSON stored
            for playlist in self.playlists:
                videos_json = get_videos_json(playlist.playlist_id)
                # filter in videos within date range and filter away deleted videos
                skip_outofrange = functools.partial(
                    skip_outofrange_videos, self.dateafter
                )
                filter_videos = filter(skip_outofrange, videos_json)
                filter_videos = filter(skip_deleted_videos, filter_videos)
                all_videos.update(
                    {v["contentDetails"]["videoId"]: v for v in filter_videos}
                )
            save_json(self.cache_dir, "videos", all_videos)
        self.videos_ids = [*all_videos.keys()]  # unpacking so it's subscriptable

    def download_video_files(self, max_concurrency):

        audext, vidext = {"webm": ("webm", "webm"), "mp4": ("m4a", "mp4")}[
            self.video_format
        ]

        # prepare options which are shared with every downloader
        options = {
            "cachedir": self.videos_dir,
            "writethumbnail": True,
            "write_all_thumbnails": False,
            "writesubtitles": True,
            "allsubtitles": True,
            "subtitlesformat": "vtt",
            "keepvideo": False,
            "ignoreerrors": False,
            "retries": 20,
            "fragment-retries": 50,
            "skip-unavailable-fragments": True,
            # "external_downloader": "aria2c",
            # "external_downloader_args": ["--max-tries=20", "--retry-wait=30"],
            "outtmpl": str(self.videos_dir.joinpath("%(id)s", "video.%(ext)s")),
            "preferredcodec": self.video_format,
            "format": f"best[ext={vidext}]/bestvideo[ext={vidext}]+bestaudio[ext={audext}]/best",
            "y2z_videos_dir": self.videos_dir,
        }
        if self.all_subtitles:
            options.update({"writeautomaticsub": True})

        # find number of actuall parallel workers
        nb_videos = len(self.videos_ids)
        concurrency = nb_videos if nb_videos < max_concurrency else max_concurrency

        # short-circuit concurency if we have only one thread (can help debug)
        if concurrency <= 1:
            return self.download_video_files_batch(options, self.videos_ids)

        # prepare out videos_ids batches
        def get_slot():
            n = 0
            while True:
                yield n
                n += 1
                if n >= concurrency:
                    n = 0

        batches = [[] for _ in range(0, concurrency)]
        slot = get_slot()
        for video_id in self.videos_ids:
            batches[next(slot)].append(video_id)

        overall_succeeded = []
        overall_failed = []
        # execute the batches concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            fs = [
                executor.submit(self.download_video_files_batch, options, videos_ids)
                for videos_ids in batches
            ]
            done, not_done = concurrent.futures.wait(
                fs, return_when=concurrent.futures.ALL_COMPLETED
            )

            # we have some `not_done` batches, indicating errors within
            if not_done:
                logger.critical(
                    "Not all video-processing batches completed. Cancelling…"
                )
                for future in not_done:
                    exc = future.exception()
                    if exc:
                        logger.exception(exc)
                        raise exc

            # retrieve our list of successful/failed video_ids
            for future in done:
                succeeded, failed = future.result()
                overall_succeeded += succeeded
                overall_failed += failed

        # remove left-over files for failed downloads
        logger.debug(f"removing left-over files of {len(overall_failed)} failed videos")
        for video_id in overall_failed:
            shutil.rmtree(self.videos_dir.joinpath(video_id), ignore_errors=True)

        return overall_succeeded, overall_failed

    def download_from_cache(self, key, video_path, encoder_version):
        """ whether it successfully downloaded from cache """
        if self.use_any_optimized_version:
            if not self.s3_storage.has_object(key, self.s3_storage.bucket_name):
                return False
        else:
            if not self.s3_storage.has_object_matching_meta(
                key, tag="encoder_version", value=f"v{encoder_version}"
            ):
                return False
        video_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.s3_storage.download_file(key, video_path)
        except Exception as exc:
            logger.error(f"{key} failed to download from cache: {exc}")
            return False
        logger.info(f"downloaded {video_path} from cache at {key}")
        return True

    def upload_to_cache(self, key, video_path, encoder_version):
        """ whether it successfully uploaded to cache """
        try:
            self.s3_storage.upload_file(
                video_path, key, meta={"encoder_version": f"v{encoder_version}"}
            )
        except Exception as exc:
            logger.error(f"{key} failed to upload to cache: {exc}")
            return False
        logger.info(f"uploaded {video_path} to cache at {key}")
        return True

    def download_video(self, video_id, options):
        """ download the video from cache/youtube and return True if successful """

        preset = {"mp4": VideoMp4Low}.get(self.video_format, VideoWebmLow)()
        options_copy = options.copy()
        video_location = options_copy["y2z_videos_dir"].joinpath(video_id)
        video_path = video_location.joinpath(f"video.{self.video_format}")

        if self.s3_storage:
            s3_key = f"{self.video_format}/{self.video_quality}/{video_id}"
            logger.debug(
                f"Attempting to download video file for {video_id} from cache..."
            )
            if self.download_from_cache(s3_key, video_path, preset.VERSION):
                return True

        try:
            # skip downloading the thumbnails
            options_copy.update(
                {
                    "writethumbnail": False,
                    "writesubtitles": False,
                    "allsubtitles": False,
                    "writeautomaticsub": False,
                }
            )
            with youtube_dl.YoutubeDL(options_copy) as ydl:
                ydl.download([video_id])
            post_process_video(
                video_location,
                video_id,
                preset,
                self.video_format,
                self.low_quality,
            )
        except (
            youtube_dl.utils.DownloadError,
            FileNotFoundError,
            subprocess.CalledProcessError,
        ) as exc:
            logger.error(f"Video file for {video_id} could not be downloaded")
            logger.debug(exc)
            return False
        else:  # upload to cache only if everything went well
            if self.s3_storage:
                logger.debug(f"Uploading video file for {video_id} to cache ...")
                self.upload_to_cache(s3_key, video_path, preset.VERSION)
            return True

    def download_thumbnail(self, video_id, options):
        """ download the thumbnail from cache/youtube and return True if successful """

        preset = WebpHigh()
        options_copy = options.copy()
        video_location = options_copy["y2z_videos_dir"].joinpath(video_id)
        thumbnail_path = video_location.joinpath("video.webp")

        if self.s3_storage:
            s3_key = f"thumbnails/high/{video_id}"
            logger.debug(
                f"Attempting to download thumbnail for {video_id} from cache..."
            )
            if self.download_from_cache(s3_key, thumbnail_path, preset.VERSION):
                return True

        try:
            # skip downloading the video
            options_copy.update(
                {
                    "skip_download": True,
                    "writesubtitles": False,
                    "allsubtitles": False,
                    "writeautomaticsub": False,
                }
            )
            with youtube_dl.YoutubeDL(options_copy) as ydl:
                ydl.download([video_id])
            process_thumbnail(thumbnail_path, preset)
        except (
            youtube_dl.utils.DownloadError,
            FileNotFoundError,
            subprocess.CalledProcessError,
        ) as exc:
            logger.error(f"Thumbnail for {video_id} could not be downloaded")
            logger.debug(exc)
            return False
        else:  # upload to cache only if everything went well
            if self.s3_storage:
                logger.debug(f"Uploading thumbnail for {video_id} to cache ...")
                self.upload_to_cache(s3_key, thumbnail_path, preset.VERSION)
            return True

    def download_subtitles(self, video_id, options):
        """ download subtitles for a video """

        options_copy = options.copy()
        options_copy.update({"skip_download": True, "writethumbnail": False})
        try:
            with youtube_dl.YoutubeDL(options_copy) as ydl:
                ydl.download([video_id])
        except Exception:
            logger.error(f"Could not download subtitles for {video_id}")

    def download_video_files_batch(self, options, videos_ids):
        """ download video file and thumbnail for all videos in batch and return succeeded and failed video ids """

        succeeded = []
        failed = []
        for video_id in videos_ids:
            if self.download_video(video_id, options) and self.download_thumbnail(
                video_id, options
            ):
                self.download_subtitles(video_id, options)
                succeeded.append(video_id)
            else:
                failed.append(video_id)
        return succeeded, failed

    def download_authors_branding(self):
        videos_channels_json = load_json(self.cache_dir, "videos_channels")
        uniq_channel_ids = list(
            set([chan["channelId"] for chan in videos_channels_json.values()])
        )
        for channel_id in uniq_channel_ids:
            save_channel_branding(self.channels_dir, channel_id, save_banner=False)
            self.copy_default_banner(channel_id)

    def copy_default_banner(self, channel_id):
        banner_path = self.channels_dir / channel_id / "banner.jpg"
        if not banner_path.exists():
            shutil.copy(
                self.templates_dir / "assets" / "banner.jpg",
                self.channels_dir / channel_id / "banner.jpg",
            )

    def update_metadata(self):
        # we use title, description, profile and banner of channel/user
        # or channel of first playlist
        try:
            main_channel_json = get_channel_json(self.main_channel_id)
        except KeyError:
            main_channel_json = {"snippet": {"title": "Unknown", "description": ""}}
        else:
            save_channel_branding(
                self.channels_dir, self.main_channel_id, save_banner=True
            )
        self.copy_default_banner(self.main_channel_id)

        # if a single playlist was requested, use if for names;
        # otherwise, use main_channel's details.
        auto_title = (
            self.playlists[0].title
            if self.is_playlist and len(self.playlists) == 1
            else main_channel_json["snippet"]["title"].strip()
        )
        auto_description = (
            clean_text(self.playlists[0].description)
            if self.is_playlist and len(self.playlists) == 1
            else clean_text(main_channel_json["snippet"]["description"])
        )
        self.title = self.title or auto_title or "-"
        self.description = self.description or auto_description or "-"

        if self.creator is None:
            if self.is_single_channel:
                self.creator = _("Youtube Channel “{title}”").format(
                    title=main_channel_json["snippet"]["title"]
                )
            else:
                self.creator = _("Youtube Channels")
        self.publisher = self.publisher or "Kiwix"

        self.tags = self.tags or ["youtube"]
        if "_videos:yes" not in self.tags:
            self.tags.append("_videos:yes")

        # copy our main_channel branding into /(profile|banner).jpg if not supplied
        if not self.profile_path.exists():
            shutil.copy(
                self.channels_dir.joinpath(self.main_channel_id, "profile.jpg"),
                self.profile_path,
            )
        if not self.banner_path.exists():
            shutil.copy(
                self.channels_dir.joinpath(self.main_channel_id, "banner.jpg"),
                self.banner_path,
            )

        # set colors from images if not supplied
        if self.main_color is None or self.secondary_color is None:
            profile_main, profile_secondary = get_colors(self.profile_path)
        self.main_color = self.main_color or profile_main
        self.secondary_color = self.secondary_color or profile_secondary

        resize_image(
            self.profile_path,
            width=48,
            height=48,
            method="thumbnail",
            dst=self.build_dir.joinpath("favicon.jpg"),
        )

    def make_html_files(self, actual_videos_ids):
        """make up HTML structure to read the content

        /home.html                                  Homepage

        for each video:
            - <slug-title>.html                     HTML article
            - videos/<videoId>/video.<ext>          video file
            - videos/<videoId>/video.<lang>.vtt     subtititle(s)
            - videos/<videoId>/video.webp            template
        """

        def remove_unused_videos(videos):
            video_ids = [video["contentDetails"]["videoId"] for video in videos]
            for path in self.videos_dir.iterdir():
                if path.is_dir() and path.name not in video_ids:
                    logger.debug(f"Removing unused video {path.name}")
                    shutil.rmtree(path, ignore_errors=True)

        def is_present(video):
            """ whether this video has actually been succeffuly downloaded """
            return video["contentDetails"]["videoId"] in actual_videos_ids

        def video_has_channel(videos_channels, video):
            return video["contentDetails"]["videoId"] in videos_channels

        def get_subtitles(video_id):
            video_dir = self.videos_dir.joinpath(video_id)
            languages = [
                x.stem.split(".")[1]
                for x in video_dir.iterdir()
                if x.is_file() and x.name.endswith(".vtt")
            ]

            def to_jinja_subtitle(lang):
                try:
                    subtitle = get_language_details(YOUTUBE_LANG_MAP.get(lang, lang))
                except Exception:
                    logger.error(f"Failed to get language details for {lang}")
                    raise
                return {
                    "code": lang,
                    # Youtube.com uses `English - code` format.
                    # Note: videojs displays it lowercased anyway
                    "name": f"{subtitle['english'].title()} - {subtitle['query']}",
                }

            # Youtube.com sorts subtitles by English name
            return sorted(map(to_jinja_subtitle, languages), key=lambda x: x["name"])

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.templates_dir)), autoescape=True
        )

        videos = load_json(self.cache_dir, "videos").values()
        # filter videos so we only include the ones we could retrieve
        videos = list(filter(is_present, videos))
        videos_channels = load_json(self.cache_dir, "videos_channels")
        has_channel = functools.partial(video_has_channel, videos_channels)
        # filter videos to exclude those for which we have no channel (#76)
        videos = list(filter(has_channel, videos))
        for video in videos:
            video_id = video["contentDetails"]["videoId"]
            title = video["snippet"]["title"]
            slug = get_slug(title)
            description = video["snippet"]["description"]
            publication_date = dt_parser.parse(
                video["contentDetails"]["videoPublishedAt"]
            )
            author = videos_channels[video_id]
            subtitles = get_subtitles(video_id)
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            html = env.get_template("article.html").render(
                video_id=video_id,
                video_format=self.video_format,
                author=author,
                title=title,
                description=description,
                date=format_date(publication_date, format="medium", locale=self.locale),
                subtitles=subtitles,
                url=video_url,
                channel_id=video["snippet"]["channelId"],
                color=self.main_color,
                background_color=self.secondary_color,
                autoplay=self.autoplay,
            )
            with open(
                self.build_dir.joinpath(f"{slug}.html"), "w", encoding="utf-8"
            ) as fp:
                fp.write(html)

        # build homepage
        html = env.get_template("home.html").render(
            playlists=self.playlists,
            video_format=self.video_format,
            title=self.title,
            description=self.description,
            color=self.main_color,
            background_color=self.secondary_color,
            page_label=_("Page {current}/{total}"),
            back_label=_("Back to top"),
        )
        with open(self.build_dir.joinpath("home.html"), "w", encoding="utf-8") as fp:
            fp.write(html)

        # rewrite app.js including `format`
        with open(self.assets_dir.joinpath("app.js"), "w", encoding="utf-8") as fp:
            fp.write(
                env.get_template("assets/app.js").render(video_format=self.video_format)
            )

        # rewrite app.js including `pagination`
        with open(self.assets_dir.joinpath("db.js"), "w", encoding="utf-8") as fp:
            fp.write(
                env.get_template("assets/db.js").render(
                    NB_VIDEOS_PER_PAGE=self.nb_videos_per_page
                )
            )

        # write list of videos in data.js
        def to_data_js(video):
            return {
                "id": video["contentDetails"]["videoId"],
                "title": video["snippet"]["title"],
                "slug": get_slug(video["snippet"]["title"]),
                "description": video["snippet"]["description"],
                "subtitles": get_subtitles(video["contentDetails"]["videoId"]),
                "thumbnail": str(
                    Path("videos").joinpath(
                        video["contentDetails"]["videoId"], "video.webp"
                    )
                ),
            }

        with open(self.assets_dir.joinpath("data.js"), "w", encoding="utf-8") as fp:
            # write all playlists as they are
            for playlist in self.playlists:
                # retrieve list of videos for PL
                playlist_videos = load_json(
                    self.cache_dir, f"playlist_{playlist.playlist_id}_videos"
                )
                # filtering-out missing ones (deleted or not downloaded)
                playlist_videos = list(filter(skip_deleted_videos, playlist_videos))
                playlist_videos = list(filter(is_present, playlist_videos))
                playlist_videos = list(filter(has_channel, playlist_videos))
                # sorting them based on playlist
                playlist_videos.sort(key=lambda v: v["snippet"]["position"])

                fp.write(
                    "var json_{slug} = {json_str};\n".format(
                        slug=playlist.slug,
                        json_str=json.dumps(
                            list(map(to_data_js, playlist_videos)), indent=4
                        ),
                    )
                )

        # write a metadata.json file with some content-related data
        with open(
            self.build_dir.joinpath("metadata.json"), "w", encoding="utf-8"
        ) as fp:
            json.dump({"video_format": self.video_format}, fp, indent=4)

        # clean videos left out in videos directory
        remove_unused_videos(videos)
