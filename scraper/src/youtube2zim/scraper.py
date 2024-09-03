#!/usr/bin/env python3
# vim: ai ts=4 sts=4 et sw=4 nu

"""
    create project on Google Developer console
    Add Youtube Data API v3 to it
    Create credentials (Other non-UI, Public Data)
"""

import concurrent.futures
import datetime
import functools
import json
import re
import shutil
import subprocess
import tempfile
from collections.abc import Callable
from gettext import gettext as _
from pathlib import Path
from typing import Any

import yt_dlp
from kiwixstorage import KiwixStorage
from pif import get_public_ip
from schedule import every, run_pending
from zimscraperlib.download import stream_file
from zimscraperlib.i18n import NotFoundError, get_language_details
from zimscraperlib.image.conversion import convert_image
from zimscraperlib.image.presets import WebpHigh
from zimscraperlib.image.probing import get_colors, is_hex_color
from zimscraperlib.image.transformation import resize_image
from zimscraperlib.inputs import compute_descriptions
from zimscraperlib.video.presets import VideoMp4Low, VideoWebmLow
from zimscraperlib.zim import Creator
from zimscraperlib.zim.filesystem import validate_zimfile_creatable
from zimscraperlib.zim.indexing import IndexData
from zimscraperlib.zim.metadata import (
    validate_description,
    validate_longdescription,
    validate_tags,
    validate_title,
)

from youtube2zim.constants import (
    CHANNEL,
    PLAYLIST,
    ROOT_DIR,
    SCRAPER,
    USER,
    YOUTUBE,
    YOUTUBE_LANG_MAP,
    logger,
)
from youtube2zim.processing import post_process_video, process_thumbnail
from youtube2zim.schemas import (
    Author,
    Channel,
    Config,
    Playlist,
    PlaylistPreview,
    Playlists,
    Subtitle,
    Subtitles,
    Video,
    VideoPreview,
)
from youtube2zim.utils import (
    clean_text,
    delete_callback,
    get_slug,
    load_json,
    load_mandatory_json,
    save_json,
)
from youtube2zim.youtube import (
    credentials_ok,
    extract_playlists_details_from,
    get_channel_json,
    get_videos_authors_info,
    get_videos_json,
    save_channel_branding,
    skip_deleted_videos,
    skip_outofrange_videos,
)

MAXIMUM_YOUTUBEID_LENGTH = 24


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
        output_dir,
        zimui_dist,
        fname,
        debug,
        tmp_dir,
        max_concurrency,
        language,
        tags,
        dateafter,
        use_any_optimized_version,
        s3_url_with_credentials,
        publisher,
        disable_metadata_checks,
        stats_filename,
        title=None,
        description=None,
        long_description=None,
        creator=None,
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
        self.fname = fname
        self.language = language
        self.tags = [t.strip() for t in tags.split(",")]
        self.title = title
        self.description = description
        self.long_description = long_description
        self.creator = creator
        self.publisher = publisher
        self.name = name
        self.profile_image = profile_image
        self.banner_image = banner_image
        self.main_color = main_color
        self.secondary_color = secondary_color
        self.disable_metadata_checks = disable_metadata_checks

        if not self.disable_metadata_checks:
            # Validate ZIM metadata early so that we do not waste time doing operations
            # for a scraper which will fail anyway in the end
            validate_tags("Tags", self.tags)
            if self.title:
                validate_title("Title", self.title)
            if self.description:
                validate_description("Description", self.description)
            if self.long_description:
                validate_longdescription("LongDescription", self.long_description)

        # directory setup
        self.output_dir = Path(output_dir).expanduser().resolve()
        if tmp_dir:
            tmp_dir = Path(tmp_dir).expanduser().resolve()
            tmp_dir.mkdir(parents=True, exist_ok=True)
        self.build_dir = Path(tempfile.mkdtemp(dir=tmp_dir))
        self.zimui_dist = Path(zimui_dist)

        # process-related
        self.playlists = []
        self.uploads_playlist_id = None
        self.videos_ids = []
        self.video_ids_count = 0
        self.videos_processed = 0
        self.main_channel_id = None  # use for branding

        # debug/devel options
        self.debug = debug
        self.max_concurrency = max_concurrency

        # update youtube credentials store
        YOUTUBE.build_dir = self.build_dir
        YOUTUBE.api_key = self.api_key
        YOUTUBE.cache_dir = self.cache_dir

        # Optimization-cache
        self.s3_url_with_credentials = s3_url_with_credentials
        self.use_any_optimized_version = use_any_optimized_version
        self.video_quality = "low" if self.low_quality else "high"
        self.s3_storage = None

        # scraper progess
        self.stats_path = None
        if stats_filename:
            self.stats_path = Path(stats_filename).expanduser()
            self.stats_path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def root_dir(self):
        return ROOT_DIR

    @property
    def channels_dir(self):
        return self.build_dir.joinpath("channels")

    @property
    def cache_dir(self):
        return self.build_dir.joinpath("cache")

    @property
    def subtitles_cache_dir(self):
        return self.cache_dir.joinpath("subtitles")

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
        return len(list({pl.creator_id for pl in self.playlists})) == 1

    @property
    def sorted_playlists(self):
        """sorted list of playlists (by title) but with Uploads one at first if any"""
        if len(self.playlists) <= 1:
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
        """execute the scraper step by step"""

        try:
            # first report => creates a file with appropriate structure
            self.report_progress()

            self.validate_id()

            # validate dateafter input
            self.validate_dateafter_input()

            if not self.name:
                raise Exception("name is mandatory")
            period = datetime.date.today().strftime("%Y-%m")
            self.fname = (
                self.fname.format(period=period)
                if self.fname
                else f"{self.name}_{period}.zim"
            )

            # check that we can create a ZIM file in the output directory
            validate_zimfile_creatable(self.output_dir, self.fname)

            # check that build_dir is correct
            if not self.build_dir.exists() or not self.build_dir.is_dir():
                raise OSError(f"Incorrect build_dir: {self.build_dir}")

            logger.info(
                f"starting youtube scraper for {self.collection_type}#{self.youtube_id}"
            )
            logger.info(f"preparing build folder at {self.build_dir.resolve()}")
            self.prepare_build_folder()

            logger.info("testing Youtube credentials")
            if not credentials_ok():
                raise ValueError(
                    "Unable to connect to Youtube API v3. check `API_KEY`."
                )

            if self.s3_url_with_credentials and not self.s3_credentials_ok():
                raise ValueError(
                    "Unable to connect to Optimization Cache. Check its URL."
                )

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

            self.video_ids_count = len(self.videos_ids)
            nb_videos_msg = f".. {self.video_ids_count} videos"
            if self.dateafter.start.year != 1:
                nb_videos_msg += (
                    f" in date range: {self.dateafter.start} - {datetime.date.today()}"
                )
            logger.info(f"{nb_videos_msg}.")

            # set a timer to report progress only every 10 seconds
            every(10).seconds.do(self.report_progress)

            logger.info("update general metadata")
            self.update_metadata()

            if not self.title:
                raise Exception("title is mandatory")
            if not self.description:
                raise Exception("description is mandatory")
            if not self.creator:
                raise Exception("creator is mandatory")

            # check that illustration is correct
            illustration = "favicon.png"
            illustration_path = self.build_dir / illustration
            if not illustration_path.exists() or not illustration_path.is_file():
                raise OSError(
                    f"Incorrect illustration: {illustration} ({illustration_path})"
                )
            with open(illustration_path, "rb") as fh:
                illustration_data = fh.read()

            logger.info("building ZIM file")
            self.zim_file = Creator(
                filename=self.output_dir / self.fname,
                main_path="index.html",
                ignore_duplicates=True,
                disable_metadata_checks=self.disable_metadata_checks,
            )
            self.zim_file.config_metadata(
                Name=self.name,
                Language=self.language,
                Title=self.title,
                Description=self.description,
                LongDescription=self.long_description,
                Creator=self.creator,
                Publisher=self.publisher,
                tags=";".join(self.tags) if self.tags else "",
                scraper=SCRAPER,
                Date=datetime.date.today(),
                Illustration_48x48_at_1=illustration_data,
            )
            self.zim_file.start()

            logger.debug(f"Preparing zimfile at {self.zim_file.filename}")

            logger.info("add main channel branding to ZIM")
            self.add_main_channel_branding_to_zim()

            logger.debug(f"add zimui files from {self.zimui_dist}")
            self.add_zimui()

            # download videos (and recompress)
            logger.info(
                "downloading all videos, subtitles and thumbnails "
                f"(concurrency={self.max_concurrency})"
            )
            logger.info(f"  format: {self.video_format}")
            logger.info(f"  quality: {self.video_quality}")
            logger.info(f"  generated-subtitles: {self.all_subtitles}")
            if self.s3_storage:
                logger.info(
                    f"  using cache: {self.s3_storage.url.netloc} "
                    f"with bucket: {self.s3_storage.bucket_name}"
                )
            succeeded, failed = self.download_video_files(
                max_concurrency=self.max_concurrency
            )
            if failed:
                logger.error(f"{len(failed)} video(s) failed to download: {failed}")
                if len(failed) >= len(succeeded):
                    logger.critical("More than half of videos failed. exiting")
                    raise OSError("Too much videos failed to download")

            logger.info("retrieve channel-info for all videos (author details)")
            get_videos_authors_info(succeeded)

            logger.info("download all author's profile pictures")
            self.download_authors_branding()

            logger.info("creating JSON files")
            self.make_json_files(succeeded)
        except KeyboardInterrupt:
            logger.error("KeyboardInterrupt, exiting.")
            return 1
        except Exception as exc:
            logger.error(f"Interrupting process due to error: {exc}")
            logger.exception(exc)
            return 1
        else:
            logger.info("Finishing ZIM file…")
            self.zim_file.finish()
        finally:
            self.report_progress()
            logger.info("removing temp folder")
            shutil.rmtree(self.build_dir, ignore_errors=True)

        logger.info("all done!")

    def add_zimui(self):
        logger.info(f"Adding files in {self.zimui_dist}")
        for file in self.zimui_dist.rglob("*"):
            if file.is_dir():
                continue
            path = str(Path(file).relative_to(self.zimui_dist))
            logger.debug(f"Adding {path} to ZIM")
            if path == "index.html":  # Change index.html title and add to ZIM
                index_html_path = self.zimui_dist / path
                html_content = index_html_path.read_text(encoding="utf-8")
                new_html_content = re.sub(
                    r"(<title>)(.*?)(</title>)",
                    rf"\1{self.title}\3",
                    html_content,
                    flags=re.IGNORECASE,
                )
                self.zim_file.add_item_for(
                    path=path,
                    content=new_html_content,
                    mimetype="text/html",
                    is_front=True,
                )
            else:
                self.zim_file.add_item_for(
                    path,
                    fpath=file,
                    is_front=False,
                )

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
            self.dateafter = yt_dlp.DateRange(self.dateafter)
        except Exception as exc:
            logger.error(
                "Invalid dateafter input. Valid dateafter format: "
                "YYYYMMDD or (now|today)[+-][0-9](day|week|month|year)(s)."
            )
            raise ValueError(f"Invalid dateafter input: {exc}") from exc

    def validate_id(self):
        # space not allowed in youtube-ID
        self.youtube_id = self.youtube_id.replace(" ", "")
        if (
            self.collection_type == "channel"
            and len(self.youtube_id) > MAXIMUM_YOUTUBEID_LENGTH
        ):
            raise ValueError("Invalid ChannelId")
        if "," in self.youtube_id and self.collection_type != "playlist":
            raise ValueError("Invalid YoutubeId")

    def prepare_build_folder(self):
        """prepare build folder before we start downloading data"""

        # cache folder to store youtube-api results
        self.cache_dir.mkdir(exist_ok=True)
        self.subtitles_cache_dir.mkdir(exist_ok=True)

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
            if isinstance(self.profile_image, str) and self.profile_image.startswith(
                "http"
            ):
                stream_file(self.profile_image, self.profile_path)
            else:
                self.profile_image = Path(self.profile_image)
                if not self.profile_image.exists():
                    raise OSError(
                        f"--profile image could not be found: {self.profile_image}"
                    )
                shutil.copy(self.profile_image, self.profile_path)
            resize_image(self.profile_path, width=100, height=100, method="thumbnail")
        if self.banner_image:
            if isinstance(self.banner_image, str) and self.banner_image.startswith(
                "http"
            ):
                stream_file(self.banner_image, self.banner_path)
            else:
                self.banner_image = Path(self.banner_image)
                if not self.banner_image.exists():
                    raise OSError(
                        f"--banner image could not be found: {self.banner_image}"
                    )
                shutil.copy(self.banner_image, self.banner_path)
            resize_image(self.banner_path, width=1060, height=175, method="thumbnail")

        if self.main_color and not is_hex_color(self.main_color):
            raise ValueError(
                f"--main-color is not a valid hex color: {self.main_color}"
            )

        if self.secondary_color and not is_hex_color(self.secondary_color):
            raise ValueError(
                "--secondary_color-color is not "
                f"a valid hex color: {self.secondary_color}"
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
            "format": f"best[ext={vidext}]/"
            f"bestvideo[ext={vidext}]+bestaudio[ext={audext}]/best",
            "y2z_videos_dir": self.videos_dir,
        }
        if self.all_subtitles:
            options.update({"writeautomaticsub": True})

        # find number of actuall parallel workers
        nb_videos = self.video_ids_count
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
        """whether it successfully downloaded from cache"""
        if not self.s3_storage:
            raise Exception(
                "Cannot download from cache if s3_storage is not configured"
            )
        if self.use_any_optimized_version:
            if not self.s3_storage.has_object(key, self.s3_storage.bucket_name):
                return False
        elif not self.s3_storage.has_object_matching_meta(
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
        """whether it successfully uploaded to cache"""
        if not self.s3_storage:
            raise Exception("Cannot upload to cache if s3_storage is not configured")
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
        """download the video from cache/youtube and return True if successful"""

        preset = {"mp4": VideoMp4Low}.get(self.video_format, VideoWebmLow)()
        options_copy = options.copy()
        video_location = options_copy["y2z_videos_dir"].joinpath(video_id)
        video_path = video_location.joinpath(f"video.{self.video_format}")
        zim_path = f"videos/{video_id}/video.{self.video_format}"

        s3_key = None
        if self.s3_storage:
            s3_key = f"{self.video_format}/{self.video_quality}/{video_id}"
            logger.debug(
                f"Attempting to download video file for {video_id} from cache..."
            )
            if self.download_from_cache(s3_key, video_path, preset.VERSION):
                self.add_file_to_zim(
                    zim_path, video_path, callback=(delete_callback, video_path)
                )
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
            with yt_dlp.YoutubeDL(options_copy) as ydl:
                ydl.download([video_id])
            post_process_video(
                video_location,
                video_id,
                preset,
                self.video_format,
                self.low_quality,
            )
            self.add_file_to_zim(
                zim_path, video_path, callback=(delete_callback, video_path)
            )
        except (
            yt_dlp.utils.DownloadError,
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
        """download the thumbnail from cache/youtube and return True if successful"""

        preset = WebpHigh()
        options_copy = options.copy()
        video_location = options_copy["y2z_videos_dir"].joinpath(video_id)
        thumbnail_path = video_location.joinpath("video.webp")
        zim_path = f"videos/{video_id}/video.webp"

        s3_key = None
        if self.s3_storage:
            s3_key = f"thumbnails/high/{video_id}"
            logger.debug(
                f"Attempting to download thumbnail for {video_id} from cache..."
            )
            if self.download_from_cache(s3_key, thumbnail_path, preset.VERSION):
                self.add_file_to_zim(
                    zim_path, thumbnail_path, callback=(delete_callback, thumbnail_path)
                )
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
            with yt_dlp.YoutubeDL(options_copy) as ydl:
                ydl.download([video_id])
            process_thumbnail(thumbnail_path, preset)
            self.add_file_to_zim(
                zim_path, thumbnail_path, callback=(delete_callback, thumbnail_path)
            )
        except (
            yt_dlp.utils.DownloadError,
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

    def fetch_video_subtitles_list(self, video_id: str) -> Subtitles:
        """fetch list of subtitles for a video"""

        video_dir = self.videos_dir.joinpath(video_id)
        languages = [
            x.stem.split(".")[1]
            for x in video_dir.iterdir()
            if x.is_file() and x.name.endswith(".vtt")
        ]

        def to_subtitle_object(lang) -> Subtitle:
            try:
                try:
                    subtitle = get_language_details(YOUTUBE_LANG_MAP.get(lang, lang))
                except NotFoundError:
                    lang_simpl = re.sub(r"^([a-z]{2})-.+$", r"\1", lang)
                    subtitle = get_language_details(
                        YOUTUBE_LANG_MAP.get(lang_simpl, lang_simpl)
                    )
            except Exception:
                logger.error(f"Failed to get language details for {lang}")
                raise
            if not subtitle:
                logger.error(f"Empty language details retrieved for {lang}")
                raise Exception("Empty language details")
            return Subtitle(
                code=lang,
                name=f"{subtitle['english'].title()} - {subtitle['query']}",
            )

        # Youtube.com sorts subtitles by English name
        return Subtitles(
            subtitles=sorted(map(to_subtitle_object, languages), key=lambda x: x.name)
        )

    def add_video_subtitles_to_zim(self, video_id: str):
        """add subtitles files to zim file"""

        for file in self.videos_dir.joinpath(video_id).iterdir():
            if file.suffix == ".vtt":
                self.add_file_to_zim(
                    f"videos/{video_id}/{file.name}",
                    file,
                    callback=(delete_callback, file),
                )

    def download_subtitles(self, video_id, options):
        """download subtitles for a video"""

        options_copy = options.copy()
        options_copy.update({"skip_download": True, "writethumbnail": False})
        try:
            with yt_dlp.YoutubeDL(options_copy) as ydl:
                ydl.download([video_id])
            subtitles_list = self.fetch_video_subtitles_list(video_id)
            # save subtitles to cache for generating JSON files later
            save_json(
                self.subtitles_cache_dir,
                video_id,
                subtitles_list.dict(by_alias=True),
            )
            self.add_video_subtitles_to_zim(video_id)
        except Exception:
            logger.error(f"Could not download subtitles for {video_id}")

    def download_video_files_batch(self, options, videos_ids):
        """download video file and thumbnail for all videos in batch

        returning succeeded and failed video ids"""

        succeeded = []
        failed = []
        for video_id in videos_ids:
            run_pending()
            if self.download_video(video_id, options) and self.download_thumbnail(
                video_id, options
            ):
                self.download_subtitles(video_id, options)
                succeeded.append(video_id)
            else:
                failed.append(video_id)
            self.videos_processed += 1
        return succeeded, failed

    def download_authors_branding(self):
        videos_channels_json = load_mandatory_json(self.cache_dir, "videos_channels")
        uniq_channel_ids = list(
            {chan["channelId"] for chan in videos_channels_json.values()}
        )
        for channel_id in uniq_channel_ids:
            save_channel_branding(self.channels_dir, channel_id, save_banner=False)
            channel_profile_path = self.channels_dir / channel_id / "profile.jpg"
            self.add_file_to_zim(
                f"channels/{channel_id}/profile.jpg",
                channel_profile_path,
                callback=(delete_callback, channel_profile_path),
            )

    def add_main_channel_branding_to_zim(self):
        """add main channel branding to zim file"""
        branding_items = [
            ("profile.jpg", self.profile_path),
            ("banner.jpg", self.banner_path),
            ("favicon.png", self.build_dir / "favicon.png"),
        ]
        for filename, path in branding_items:
            if path.exists():
                self.add_file_to_zim(filename, path, callback=(delete_callback, path))

    def update_metadata(self):
        # we use title, description, profile and banner of channel/user
        # or channel of first playlist
        if not self.main_channel_id:
            raise Exception("main_channel_id is mandatory")
        try:
            main_channel_json = get_channel_json(self.main_channel_id)
        except KeyError:
            main_channel_json = {"snippet": {"title": "Unknown", "description": ""}}
        else:
            save_channel_branding(
                self.channels_dir, self.main_channel_id, save_banner=True
            )

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
        ) or "-"
        self.title = self.title or auto_title or "-"
        self.description, self.long_description = compute_descriptions(
            default_description=auto_description,
            user_description=self.description,
            user_long_description=self.long_description,
        )

        if self.creator is None:
            if self.is_single_channel:
                self.creator = _("Youtube Channel “{title}”").format(
                    title=main_channel_json["snippet"]["title"]
                )
            else:
                self.creator = _("Youtube Channels")

        self.tags = self.tags or ["youtube"]
        if "_videos:yes" not in self.tags:
            self.tags.append("_videos:yes")

        # copy our main_channel branding into /(profile|banner).jpg if not supplied
        if not self.profile_path.exists():
            shutil.copy(
                self.channels_dir.joinpath(self.main_channel_id, "profile.jpg"),
                self.profile_path,
            )

        # set colors from images if not supplied
        if self.main_color is None or self.secondary_color is None:
            profile_main, profile_secondary = get_colors(self.profile_path)
            self.main_color = self.main_color or profile_main
            self.secondary_color = self.secondary_color or profile_secondary

        # convert profile image to png for favicon
        png_profile_path = self.build_dir.joinpath("profile.png")
        convert_image(self.profile_path, png_profile_path)

        resize_image(
            png_profile_path,
            width=48,
            height=48,
            method="thumbnail",
            dst=self.build_dir.joinpath("favicon.png"),
        )
        png_profile_path.unlink()

    def make_json_files(self, actual_videos_ids):
        """Generate JSON files to be consumed by the frontend"""

        def remove_unused_videos(videos):
            video_ids = [video["contentDetails"]["videoId"] for video in videos]
            for path in self.videos_dir.iterdir():
                if path.is_dir() and path.name not in video_ids:
                    logger.debug(f"Removing unused video {path.name}")
                    shutil.rmtree(path, ignore_errors=True)

        def is_present(video):
            """whether this video has actually been succeffuly downloaded"""
            return video["contentDetails"]["videoId"] in actual_videos_ids

        def video_has_channel(videos_channels, video):
            return video["contentDetails"]["videoId"] in videos_channels

        def get_thumbnail_path(video_id):
            return f"videos/{video_id}/video.webp"

        def get_subtitles(video_id) -> list[Subtitle]:
            subtitles_list = load_json(self.subtitles_cache_dir, video_id)
            if subtitles_list is None:
                return []
            return subtitles_list["subtitles"]

        def get_videos_list(playlist):
            videos = load_mandatory_json(
                self.cache_dir, f"playlist_{playlist.playlist_id}_videos"
            )
            videos = list(filter(skip_deleted_videos, videos))
            videos = list(filter(is_present, videos))
            videos = list(filter(has_channel, videos))
            videos = sorted(videos, key=lambda v: v["snippet"]["position"])
            return videos

        def generate_video_object(video) -> Video:
            video_id = video["contentDetails"]["videoId"]
            author = videos_channels[video_id]
            subtitles_list = get_subtitles(video_id)
            channel_data = get_channel_json(author["channelId"])
            return Video(
                id=video_id,
                title=video["snippet"]["title"],
                description=video["snippet"]["description"],
                author=Author(
                    channel_id=author["channelId"],
                    channel_title=author["channelTitle"],
                    channel_description=channel_data["snippet"]["description"],
                    channel_joined_date=channel_data["snippet"]["publishedAt"],
                    profile_path=f"channels/{author['channelId']}/profile.jpg",
                    banner_path=f"channels/{author['channelId']}/banner.jpg",
                ),
                publication_date=video["contentDetails"]["videoPublishedAt"],
                video_path=f"videos/{video_id}/video.{self.video_format}",
                thumbnail_path=get_thumbnail_path(video_id),
                subtitle_path=f"videos/{video_id}" if len(subtitles_list) > 0 else None,
                subtitle_list=subtitles_list,
                duration=videos_channels[video_id]["duration"],
            )

        def generate_video_preview_object(video) -> VideoPreview:
            video_id = video["contentDetails"]["videoId"]
            return VideoPreview(
                slug=get_video_slug(video),
                id=video_id,
                title=video["snippet"]["title"],
                thumbnail_path=get_thumbnail_path(video_id),
                duration=videos_channels[video_id]["duration"],
            )

        def get_video_slug(video) -> str:
            title = video["snippet"]["title"]
            video_id = video["contentDetails"]["videoId"]
            return f"{get_slug(title)}-{video_id[:4]}"

        def generate_playlist_object(playlist) -> Playlist:
            channel_data = get_channel_json(playlist.creator_id)
            videos = get_videos_list(playlist)
            playlist_videos = [generate_video_preview_object(video) for video in videos]

            # add videos to ZIM index
            for idx, video_obj in enumerate(playlist_videos):
                self.add_custom_item_to_zim_index(
                    video_obj.title,
                    videos[idx]["snippet"]["description"],
                    video_obj.slug,
                    f"watch/{video_obj.slug}?list={get_playlist_slug(playlist)}",
                )

            return Playlist(
                id=playlist.playlist_id,
                title=playlist.title,
                description=playlist.description,
                videos=playlist_videos,
                publication_date=playlist.published_at,
                author=Author(
                    channel_id=playlist.creator_id,
                    channel_title=playlist.creator_name,
                    channel_description=channel_data["snippet"]["description"],
                    channel_joined_date=channel_data["snippet"]["publishedAt"],
                    profile_path=f"channels/{playlist.creator_id}/profile.jpg",
                    banner_path=f"channels/{playlist.creator_id}/banner.jpg",
                ),
                videos_count=len(videos),
                thumbnail_path=get_thumbnail_path(
                    videos[0]["contentDetails"]["videoId"]
                ),
            )

        def generate_playlist_preview_object(playlist) -> PlaylistPreview:
            videos = get_videos_list(playlist)
            return PlaylistPreview(
                slug=get_playlist_slug(playlist),
                id=playlist.playlist_id,
                title=playlist.title,
                thumbnail_path=get_thumbnail_path(
                    videos[0]["contentDetails"]["videoId"]
                ),
                videos_count=len(videos),
                main_video_slug=get_video_slug(videos[0]),
            )

        def get_playlist_slug(playlist) -> str:
            return f"{get_slug(playlist.title)}-{playlist.playlist_id[-4:]}"

        videos = load_mandatory_json(self.cache_dir, "videos").values()
        # filter videos so we only include the ones we could retrieve
        videos = list(filter(is_present, videos))
        videos_channels = load_mandatory_json(self.cache_dir, "videos_channels")
        has_channel = functools.partial(video_has_channel, videos_channels)
        # filter videos to exclude those for which we have no channel (#76)
        videos = list(filter(has_channel, videos))
        for video in videos:
            slug = get_video_slug(video)
            self.zim_file.add_item_for(
                path=f"videos/{slug}.json",
                title=slug,
                content=generate_video_object(video).model_dump_json(
                    by_alias=True, indent=2
                ),
                mimetype="application/json",
                is_front=False,
            )

        # write playlists JSON files
        playlist_list = []

        main_playlist_slug = None
        if len(self.playlists) > 0:
            main_playlist_slug = get_playlist_slug(
                self.playlists[0]
            )  # set first playlist as main playlist

        for playlist in self.playlists:
            playlist_slug = get_playlist_slug(playlist)
            playlist_path = f"playlists/{playlist_slug}.json"

            if playlist.playlist_id != self.uploads_playlist_id:
                playlist_list.append(generate_playlist_preview_object(playlist))
            else:
                main_playlist_slug = (
                    playlist_slug  # set uploads playlist as main playlist
                )

            playlist_obj = generate_playlist_object(playlist)
            self.zim_file.add_item_for(
                path=playlist_path,
                title=playlist.title,
                content=playlist_obj.model_dump_json(by_alias=True, indent=2),
                mimetype="application/json",
                is_front=False,
            )

            # add playlist to ZIM index
            self.add_custom_item_to_zim_index(
                playlist_obj.title,
                playlist_obj.description,
                playlist_slug,
                f"playlist/{playlist_slug}",
            )

        # write playlists.json file
        self.zim_file.add_item_for(
            path="playlists.json",
            title="Playlists",
            content=Playlists(playlists=playlist_list).model_dump_json(
                by_alias=True, indent=2
            ),
            mimetype="application/json",
            is_front=False,
        )

        # write channel.json file
        channel_data = get_channel_json(self.main_channel_id)
        self.zim_file.add_item_for(
            path="channel.json",
            title=self.title,
            content=Channel(
                id=str(self.main_channel_id),
                title=str(self.title),
                description=str(self.description),
                channel_name=channel_data["snippet"]["title"],
                channel_description=channel_data["snippet"]["description"],
                profile_path="profile.jpg",
                banner_path="banner.jpg",
                collection_type=self.collection_type,
                main_playlist=main_playlist_slug,
                playlist_count=len(self.playlists),
                joined_date=channel_data["snippet"]["publishedAt"],
            ).model_dump_json(by_alias=True, indent=2),
            mimetype="application/json",
            is_front=False,
        )

        # write config.json file
        self.zim_file.add_item_for(
            path="config.json",
            title="Config",
            content=Config(
                main_color=self.main_color, secondary_color=self.secondary_color
            ).model_dump_json(by_alias=True, indent=2),
            mimetype="application/json",
            is_front=False,
        )

        # clean videos left out in videos directory
        remove_unused_videos(videos)

    def add_file_to_zim(
        self,
        path: str,
        fpath: Path,
        callback: Callable | tuple[Callable, Any] | None = None,
    ):
        """add a file to a ZIM file"""

        if not fpath.exists():
            logger.error(f"File {fpath} does not exist")
            return
        logger.debug(f"Adding {path} to ZIM")
        self.zim_file.add_item_for(
            path,
            fpath=fpath,
            callback=callback,
        )

    def add_custom_item_to_zim_index(
        self, title: str, content: str, fname: str, zimui_redirect: str
    ):
        """add a custom item to the ZIM index"""

        redirect_url = f"../index.html#/{zimui_redirect}"
        html_content = (
            f"<html><head><title>{title}</title>"
            f'<meta http-equiv="refresh" content="0;URL=\'{redirect_url}\'" />'
            f"</head><body></body></html>"
        )

        logger.debug(f"Adding {fname} to ZIM index")
        self.zim_file.add_item_for(
            title=title,
            path="index/" + fname,
            content=bytes(html_content, "utf-8"),
            mimetype="text/html",
            index_data=IndexData(title=title, content=content),
        )

    def report_progress(self):
        """report progress to stats file"""

        if not self.stats_path:
            return
        progress = {
            "done": self.videos_processed,
            "total": self.video_ids_count,
        }
        self.stats_path.write_text(json.dumps(progress, indent=2))
