#!/usr/bin/env python3
# vim: ai ts=4 sts=4 et sw=4 nu

""" turn a regular build-folder into a low-quality one by re-encoding all videos.

    shortcut to call the FFMPEG youtube-dl hook we use in the scraper.
    videos are replaced.

    Usage: python youtube2zim/reencode_low_quality.py my/project/build/
"""

import json
import logging
import pathlib
import sys

from zimscraperlib.video.encoding import reencode
from zimscraperlib.video.presets import VideoMp4Low, VideoWebmLow

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main(build_path):
    build_dir = pathlib.Path(build_path)
    logger.info(f"about to re-encode video files in {build_dir}")

    if not build_dir.exists() or not build_dir.is_dir():
        logger.error(f"Build dir `{build_dir}` is not an existing folder.")
        sys.exit(1)

    # retrieve source video_format
    metadata = json.loads(build_dir.joinpath("metadata.json").read_bytes())
    video_format = metadata["video_format"]

    if video_format == "mp4":
        args = VideoMp4Low().to_ffmpeg_args()
    else:
        args = VideoWebmLow().to_ffmpeg_args()

    for video_id in build_dir.joinpath("videos").iterdir():
        if not video_id.is_dir():
            continue
        video_path = build_dir.joinpath("videos", video_id, f"video.{video_format}")
        logger.info(video_path)

        reencode(video_path, video_path, args, delete_src=True, failsafe=False)

    logger.info("all done.")


if __name__ == "__main__":
    if len(sys.argv) != 2:  # noqa: PLR2004
        logger.error("you must supply a path to a build folder")
        sys.exit(1)
    main(sys.argv[-1])
