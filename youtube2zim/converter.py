#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import pathlib
import subprocess

from zimscraperlib.logging import nicer_args_join
from zimscraperlib.imaging import resize_image

from .constants import logger


def hook_youtube_dl_ffmpeg(video_format, low_quality, data):
    """ youtube-dl hook to convert video at end of download

        - if low_quality was request
        - if received format is not requested one """

    if data.get("status") != "finished":
        return

    src_path = pathlib.Path(data["filename"])
    post_process_video(
        video_dir=src_path.parent,
        video_id=src_path.stem,
        video_format=video_format,
        low_quality=low_quality,
    )


def post_process_video(
    video_dir, video_id, video_format, low_quality, skip_recompress=False
):
    """ apply custom post-processing to downloaded video

        - resize thumbnail
        - recompress video if incorrect video_format or low_quality requested """

    # find downloaded video from video_dir
    files = [p for p in video_dir.iterdir() if p.stem == "video" and p.suffix != ".jpg"]
    if len(files) == 0:
        logger.error(f"Video file missing in {video_dir} for {video_id}")
        logger.debug(list(video_dir.iterdir()))
        raise FileNotFoundError(f"Missing video file in {video_dir}")
    if len(files) > 1:
        logger.warning(
            f"Multiple video file candidates for {video_id} in {video_dir}. Picking {files[0]} out of {files}"
        )
    src_path = files[0]

    # resize thumbnail. we use max width:248x187px in listing
    # but our posters are 480x270px
    resize_image(
        src_path.parent.joinpath("video.jpg"), width=480, height=270, method="cover"
    )

    # don't reencode if not requesting low-quality and received wanted format
    if skip_recompress or (not low_quality and src_path.suffix[1:] == video_format):
        return

    dst_path = src_path.parent.joinpath(f"video.{video_format}")
    recompress_video(src_path, dst_path, video_format)


def recompress_video(src_path, dst_path, video_format):
    """ re-encode in-place (via temp file) for format at lower quality """

    tmp_path = src_path.parent.joinpath(f"video.tmp.{video_format}")

    video_codecs = {"mp4": "h264", "webm": "libvpx"}
    audio_codecs = {"mp4": "aac", "webm": "libvorbis"}
    params = {"mp4": ["-movflags", "+faststart"], "webm": []}

    args = ["ffmpeg", "-y", "-i", f"file:{src_path}"]

    args += [
        "-codec:v",
        video_codecs[video_format],
        "-quality",
        "best",
        "-cpu-used",
        "0",
        "-b:v",
        "300k",
        "-qmin",
        "30",
        "-qmax",
        "42",
        "-maxrate",
        "300k",
        "-bufsize",
        "1000k",
        "-threads",
        "8",
        "-vf",
        "scale='480:trunc(ow/a/2)*2'",
        "-codec:a",
        audio_codecs[video_format],
        "-ar",
        "44100",
        "-b:a",
        "128k",
        "-max_muxing_queue_size",
        "9999",
    ]
    args += params[video_format]
    args += [f"file:{tmp_path}"]

    logger.info(f"recompress {src_path} -> {dst_path} {video_format=}")
    logger.debug(nicer_args_join(args))

    ffmpeg = subprocess.run(args)
    ffmpeg.check_returncode()

    # delete original
    src_path.unlink()
    # rename temp filename with final one
    tmp_path.replace(dst_path)
