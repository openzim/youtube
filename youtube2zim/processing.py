#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from zimscraperlib.video.encoding import reencode
from zimscraperlib.image.optimization import optimize_image
from zimscraperlib.image.transformation import resize_image

from .constants import logger


def process_thumbnail(thumbnail_path, preset):
    # thumbnail might be WebP as .webp, JPEG as .jpg or WebP as .jpg
    tmp_thumbnail = thumbnail_path
    if not thumbnail_path.exists():
        logger.debug("We don't have video.webp, thumbnail is .jpg")
        tmp_thumbnail = thumbnail_path.with_suffix(".jpg")

    # resize thumbnail. we use max width:248x187px in listing
    # but our posters are 480x270px
    resize_image(
        tmp_thumbnail,
        width=480,
        height=270,
        method="cover",
        allow_upscaling=True,
    )
    optimize_image(tmp_thumbnail, thumbnail_path, delete_src=True, **preset.options)
    return True


def post_process_video(video_dir, video_id, preset, video_format, low_quality):
    """apply custom post-processing to downloaded video

    - resize thumbnail
    - recompress video if incorrect video_format or low_quality requested"""

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
            f"Multiple video file candidates for {video_id} in {video_dir}. Picking {files[0]} out of {files}"
        )
    src_path = files[0]

    # don't reencode if not requesting low-quality and received wanted format
    if not low_quality and src_path.suffix[1:] == video_format:
        return

    dst_path = src_path.with_name(f"video.{video_format}")
    reencode(
        src_path, dst_path, preset.to_ffmpeg_args(), delete_src=True, failsafe=False
    )
