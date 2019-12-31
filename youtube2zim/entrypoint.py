#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import logging
import argparse

from .constants import NAME, SCRAPER, CHANNEL, PLAYLIST, USER, logger, YOUTUBE
from .scraper import Youtube2Zim


def main():
    parser = argparse.ArgumentParser(
        prog=NAME,
        description="Scraper to create a ZIM file from a Youtube Channel or Playlists",
    )

    parser.add_argument(
        "--type",
        help="Type of collection",
        choices=[CHANNEL, PLAYLIST, USER],
        required=True,
        dest="collection_type",
    )
    parser.add_argument(
        "--id", help="Youtube ID of the collection", required=True, dest="youtube_id"
    )
    parser.add_argument("--api-key", help="Youtube API Token", required=True)
    parser.add_argument(
        "--name",
        help="ZIM name. Used as identifier and filename (date will be appended)",
        required=True,
    )

    parser.add_argument(
        "--format",
        help="Format to download/transcode video to. webm is smaller",
        choices=["mp4", "webm"],
        default="webm",
        dest="video_format",
    )
    parser.add_argument(
        "--low-quality",
        help="Re-encode video using stronger compression",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--all-subtitles",
        help="Include auto-generated subtitles",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--pagination",
        help="Number of videos per page",
        type=int,
        dest="nb_videos_per_page",
        default=40,
    )
    parser.add_argument(
        "--autoplay",
        help="Enable autoplay on video articles (home never have autoplay). Behavior differs on platforms/browsers.",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--output",
        help="Output folder for ZIM file or build folder",
        default="/output",
        dest="output_dir",
    )
    parser.add_argument(
        "--no-zim",
        help="Don't produce a ZIM file, create HTML folder only.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--zim-file",
        help="ZIM file name (based on --name if not provided)",
        dest="fname",
    )

    parser.add_argument(
        "--language", help="ISO-639-3 (3 chars) language code of content", default="eng"
    )
    parser.add_argument(
        "--locale",
        help="Locale name to use for translations (if avail) and time representations. Defaults to --language or English.",
        dest="locale_name",
    )
    parser.add_argument(
        "--title",
        help="Custom title for your project and ZIM. Default to Channel name (of first video if playlists)",
    )
    parser.add_argument(
        "--description",
        help="Custom description for your project and ZIM. Default to Channel name (of first video if playlists)",
    )
    parser.add_argument(
        "--creator",
        help="Name of content creator. Defaults to Channel name or “Youtue Channels”",
    )
    parser.add_argument(
        "--publisher", help="Custom publisher name (ZIM metadata)", default="Kiwix"
    )
    parser.add_argument(
        "--tags",
        help="List of comma-separated Tags for the ZIM file. _videos:yes added automatically",
        default="youtube",
    )
    parser.add_argument(
        "--profile",
        help="Custom profile image. Squared. Will be resized to 100x100px",
        dest="profile_image",
    )
    parser.add_argument(
        "--banner",
        help="Custom banner image. Will be resized to 1060x175px",
        dest="banner_image",
    )
    parser.add_argument(
        "--main-color",
        help="Custom color. Hex/HTML syntax (#DEDEDE). Default to main color of profile image.",
    )
    parser.add_argument(
        "--secondary-color",
        help="Custom secondary color. Hex/HTML syntax (#DEDEDE). Default to secondary color of profile image.",
    )

    parser.add_argument(
        "--debug", help="Enable verbose output", action="store_true", default=False
    )
    parser.add_argument(
        "--keep",
        help="Don't erase build folder on start (for debug/devel)",
        default=False,
        action="store_true",
        dest="keep_build_dir",
    )
    parser.add_argument(
        "--skip-download",
        help="Skip the download step (videos, thumbnails, subtitles)",
        default=False,
        action="store_true",
        dest="skip_download",
    )
    parser.add_argument(
        "--concurrency",
        help="Number of concurrent threads to use",
        type=int,
        dest="max_concurrency",
        default=1,
    )
    parser.add_argument(
        "--only_test_branding",
        help="Just generate a fake home.html to check branding (images and colors)",
        default=False,
        action="store_true",
        dest="only_test_branding",
    )
    parser.add_argument(
        "--version",
        help="Display scraper version and exit",
        action="version",
        version=SCRAPER,
    )

    args = parser.parse_args()
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)

    try:
        if args.max_concurrency < 1:
            raise ValueError(f"Invalid concurrency value: {args.max_concurrency}")
        scraper = Youtube2Zim(**dict(args._get_kwargs()), youtube_store=YOUTUBE)
        scraper.run()
    except Exception as exc:
        logger.error(f"FAILED. An error occured: {exc}")
        if args.debug:
            logger.exception(exc)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
