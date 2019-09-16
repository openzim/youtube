#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import pathlib
import subprocess

from .constants import logger
from .utils import nicer_args_join


def hook_youtube_dl_ffmpeg(video_format, data):
    """ youtube-dl hook to convert in lower quality at end of download """

    if data.get("status") != "finished":
        return

    src_path = pathlib.Path(data["filename"])
    tmp_path = src_path.parent.joinpath(
        "video.tmp.{fmt}".format(src=src_path.name, fmt=video_format)
    )
    dst_path = src_path.parent.joinpath("video.{fmt}".format(fmt=video_format))

    video_codecs = {"mp4": "h264", "webm": "libvpx"}
    audio_codecs = {"mp4": "aac", "webm": "libvorbis"}
    params = {"mp4": ["-movflags", "+faststart"], "webm": []}
    args = [
        "ffmpeg",
        "-y",
        "-i",
        "file:{}".format(str(src_path)),
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
        "-b:a",
        "128k",
    ]
    args += params[video_format]
    args += ["file:{}".format(str(tmp_path))]
    logger.info(
        "  converting {src} into {dst}".format(src=str(src_path), dst=str(dst_path))
    )
    logger.debug(nicer_args_join(args))

    ffmpeg = subprocess.run(args)
    ffmpeg.check_returncode()

    # delete original
    src_path.unlink()
    # rename temp filename with final one
    tmp_path.replace(dst_path)
