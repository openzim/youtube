#!/usr/bin/env python3
# vim: ai ts=4 sts=4 et sw=4 nu

import argparse
import logging
import os
import sys

from youtube2zim.constants import CHANNEL, NAME, PLAYLIST, SCRAPER, USER, logger
from youtube2zim.scraper import Youtube2Zim


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
        "--output",
        help="Output folder for ZIM file",
        default="/output",
        dest="output_dir",
    )

    parser.add_argument(
        "--tmp-dir",
        help="Path to create temp folder in."
        "Used to temporarily store downloaded files before adding to ZIM",
    )

    parser.add_argument(
        "--zimui-dist",
        type=str,
        help=(
            "Directory containing Vite build output from the Zim UI Vue.JS application"
        ),
        default=os.getenv("YOUTUBE_ZIMUI_DIST", "../zimui/dist"),
    )

    parser.add_argument(
        "--zim-file",
        help="ZIM file name (based on --name if not provided). "
        "If used, {period} is replaced with date as of YYYY-MM",
        dest="fname",
    )

    parser.add_argument(
        "--language", help="ISO-639-3 (3 chars) language code of content", default="eng"
    )

    parser.add_argument(
        "--title",
        help="Custom title for your project and ZIM. "
        "Default to Channel name (of first video if playlists)",
    )

    parser.add_argument(
        "--description",
        help="Custom description for your project and ZIM. "
        "Default to Channel name (of first video if playlists)",
    )

    parser.add_argument(
        "--long-description",
        help="Custom long description for your ZIM.",
    )

    parser.add_argument(
        "--creator",
        help="Name of content creator. Defaults to Channel name or “Youtue Channels”",
    )

    parser.add_argument(
        "--publisher", help="Custom publisher name (ZIM metadata)", default="openZIM"
    )

    parser.add_argument(
        "--tags",
        help="List of comma-separated Tags for the ZIM file. "
        "_videos:yes added automatically",
        default="youtube",
    )

    parser.add_argument(
        "--profile",
        help="Custom profile image (path or URL). Squared. "
        "Will be resized to 100x100px",
        dest="profile_image",
    )

    parser.add_argument(
        "--banner",
        help="Custom banner image (path or URL). Will be resized to 1060x175px",
        dest="banner_image",
    )

    parser.add_argument(
        "--main-color",
        help="Custom color. Hex/HTML syntax (#DEDEDE). "
        "Default to main color of profile image.",
    )

    parser.add_argument(
        "--secondary-color",
        help="Custom secondary color. Hex/HTML syntax (#DEDEDE). "
        "Default to secondary color of profile image.",
    )

    parser.add_argument(
        "--debug", help="Enable verbose output", action="store_true", default=False
    )

    parser.add_argument(
        "--concurrency",
        help="Number of concurrent threads to use",
        type=int,
        dest="max_concurrency",
        default=1,
    )

    parser.add_argument(
        "--version",
        help="Display scraper version and exit",
        action="version",
        version=SCRAPER,
    )

    parser.add_argument(
        "--disable-metadata-checks",
        help="Disable validity checks of metadata according to openZIM conventions",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--dateafter",
        help="Custom filter to download videos uploaded on or after specified date. "
        "Format: YYYYMMDD or (now|today)[+-][0-9](day|week|month|year)(s)?",
    )

    parser.add_argument(
        "--optimization-cache",
        help="URL with credentials to S3 for using as optimization cache",
        dest="s3_url_with_credentials",
    )

    parser.add_argument(
        "--use-any-optimized-version",
        help="Use the cached files if present, whatever the version",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--stats-filename",
        help="Path to store the progress JSON file to.",
        dest="stats_filename",
    )

    args = parser.parse_args()
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)

    try:
        if args.max_concurrency < 1:
            raise ValueError(f"Invalid concurrency value: {args.max_concurrency}")
        scraper = Youtube2Zim(**dict(args._get_kwargs()))
        return scraper.run()
    except Exception as exc:
        logger.error(f"FAILED. An error occurred: {exc}")
        if args.debug:
            logger.exception(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
