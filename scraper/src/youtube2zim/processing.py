#!/usr/bin/env python3
# vim: ai ts=4 sts=4 et sw=4 nu

import pathlib

from zimscraperlib.image.conversion import convert_image
from zimscraperlib.image.optimization import OptimizeWebpOptions, optimize_webp
from zimscraperlib.image.probing import format_for
from zimscraperlib.image.transformation import resize_image
from zimscraperlib.video.encoding import reencode

from youtube2zim.constants import logger


def process_thumbnail(thumbnail_path: pathlib.Path, options: OptimizeWebpOptions):
    # thumbnail might be WebP as .webp, JPEG as .jpg or WebP as .jpg
    if not thumbnail_path.exists():
        logger.debug("We don't have video.webp, thumbnail is .jpg")
        raw_thumbnail_path = thumbnail_path.with_suffix(".jpg")
        src_format = format_for(raw_thumbnail_path, from_suffix=False)
        if src_format != "webp":
            convert_image(raw_thumbnail_path, thumbnail_path)

    # resize thumbnail. we use max width:248x187px in listing
    # but our posters are 480x270px
    resize_image(
        thumbnail_path,
        width=480,
        height=270,
        method="cover",
        allow_upscaling=True,
    )

    optimize_webp(thumbnail_path, thumbnail_path, options)


def post_process_video(video_dir, video_id, preset, video_format):
    """apply custom post-processing to downloaded video

    - resize thumbnail
    - recompress video"""

    # find downloaded video from video_dir
    files = [
        p
        for p in video_dir.iterdir()
        if p.stem == "video" and p.suffix not in (".jpg", ".webp")
    ]

    if len(files) == 0:
        logger.error(f"Video file missing in {video_dir} for {video_id}")
        logger.debug(list(video_dir.iterdir()))
        raise FileNotFoundError(f"Missing video file in {video_dir}")
    if len(files) > 1:
        logger.warning(
            f"Multiple video file candidates for {video_id} in {video_dir}. "
            f"Picking {files[0]} out of {files}"
        )
    src_path = files[0]

    dst_path = src_path.with_name(f"video.{video_format}")
    logger.info(f"Reencode video to {dst_path}")
    success, process = reencode(
        src_path,
        dst_path,
        preset.to_ffmpeg_args(),
        delete_src=True,
        failsafe=True,
    )  # pyright: ignore[reportGeneralTypeIssues]
    if not success:
        if process:
            logger.error(process.stdout)
        raise Exception(f"Exception while re-encoding {src_path} for {video_id}")
