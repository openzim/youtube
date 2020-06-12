#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import logging
import argparse

from ..constants import NAME, SCRAPER, CHANNEL, PLAYLIST, USER, logger
from ..utils import has_argument


def check_passed_args(args, extra_args, parser):
    # prevent setting --title and --description
    for arg in ("name", "title", "description", "zim-file"):
        if args.playlists_mode and has_argument(arg, extra_args):
            parser.error(
                f"Can't use --{arg} in playlists mode. Use --playlists-{arg} to set format."
            )

    # playlists-name mandatory in playlist-mode
    if not args.metadata_from:
        if args.playlists_mode and not args.playlists_name:
            parser.error("--playlists-name is mandatory in playlists mode")

        variables_list = [
            "{title}",
            "{description}",
            "{playlist_id}",
            "{slug}",
            "{creator_id}",
            "{creator_name}",
        ]
        if args.playlists_name and not [
            identifier
            for identifier in variables_list
            if identifier in args.playlists_name
        ]:
            parser.error("--playlists-name must have a variable to ensure unique names")

        if args.playlists_build_dir and not [
            identifier
            for identifier in variables_list
            if identifier in args.playlists_build_dir
        ]:
            parser.error(
                "--playlists-build-dir must have a variable to ensure unique names for custom build directories"
            )


def main():
    parser = argparse.ArgumentParser(
        prog=f"{NAME}-playlists",
        description="Scraper to create ZIM file(s) from a Youtube Channel or Playlists",
        epilog="Playlists titles, descriptions and names can use the following variables: {title}, {description}, {playlist_id}, {slug} (from title), {creator_id}, {creator_name}.",
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
        "--indiv-playlists",
        help="Playlists mode: build one ZIM per playlist of the channel",
        action="store_true",
        dest="playlists_mode",
    )

    parser.add_argument(
        "--playlists-name",
        help="Format for building individual --name argument. Required in playlist mode.",
        required=True,
    )
    parser.add_argument(
        "--playlists-zim-file",
        help="Format for building individual --zim-file argument. Uses --playlists-name otherwise",
    )
    parser.add_argument(
        "--playlists-title", help="Custom title format for individual playlist ZIM",
    )
    parser.add_argument(
        "--playlists-description",
        help="Custom description format for individual playlist ZIM",
    )
    parser.add_argument(
        "--playlists-build-dir",
        help="Custom format for build directory names for individual ZIMs",
    )
    parser.add_argument(
        "--metadata-from",
        help="File path or URL to a JSON file holding custom metadata for individual playlists. Format in README",
    )
    parser.add_argument(
        "--debug", help="Enable verbose output", action="store_true", default=False
    )
    parser.add_argument(
        "--version",
        help="Display scraper version and exit",
        action="version",
        version=SCRAPER,
    )

    args, extra_args = parser.parse_known_args()

    check_passed_args(args, extra_args, parser)

    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)

    from .scraper import YoutubeHandler

    try:
        handler = YoutubeHandler(dict(args._get_kwargs()), extra_args=extra_args)
        handler.run()
    except Exception as exc:
        logger.error(f"FAILED. An error occurred: {exc}")
        if args.debug:
            logger.exception(exc)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
