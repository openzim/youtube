#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

""" turn a regular build-folder into a low-quality one by re-encoding all videos.

    shortcut to call the FFMPEG youtube-dl hook we use in the scraper.
    videos are replaced.

    Usage: python youtube2zim/reencode_low_quality.py my/project/build/
"""

import sys
import json
import logging
import pathlib

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main(build_path):
    build_dir = pathlib.Path(build_path)
    logger.info(f"about to re-encode video files in {build_dir}")

    if not build_dir.exists() or not build_dir.is_dir():
        logger.error(f"Build dir `{build_dir}` is not an existing folder.")
        sys.exit(1)

    # import youtube2zim hook
    sys.path = [str(pathlib.Path(__file__).parent.parent.resolve())] + sys.path
    from youtube2zim.converter import recompress_video

    # retrieve source video_format
    with open(build_dir.joinpath("metadata.json"), "r") as fp:
        metadata = json.load(fp)
        video_format = metadata["video_format"]

    for video_id in build_dir.joinpath("videos").iterdir():
        if not video_id.is_dir():
            continue
        video_path = build_dir.joinpath("videos", video_id, f"video.{video_format}")
        logger.info(video_path)

        recompress_video(video_path, video_path, video_format)

    logger.info("all done.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("you must supply a path to a build folder")
        sys.exit(1)
    main(sys.argv[-1])
