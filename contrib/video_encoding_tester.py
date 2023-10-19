#!/usr/bin/env python3
# vim: ai ts=4 sts=4 et sw=4 nu
# ruff: noqa: T201, T203, DTZ003

"""
    video encoding comparator

    tests a set of videos accross different ffmpeg settings
"""


import collections
import datetime
import json
import pathlib
import subprocess
import sys

import humanfriendly
import jinja2

video_codecs = {"mp4": "h264", "webm": "libvpx"}
audio_codecs = {"mp4": "aac", "webm": "libvorbis"}
params = {"mp4": ["-movflags", "+faststart"], "webm": []}


def preset_240p(video_format):
    return [
        "-codec:v",
        video_codecs[video_format],
        # keep good quality image
        "-qmin",
        "16",
        "-qmax",
        "26",
        # best compression
        "-quality",
        "best",
        # set constant rate
        "-minrate",
        "128k",
        "-maxrate",
        "128k",
        "-b:v",
        "128k",
        # scale to 240p 4:3, adding bars if necessary
        "-vf",
        "scale=426:240:force_original_aspect_ratio=decrease,"
        "pad=426:240:(ow-iw)/2:(oh-ih)/2",
        "-codec:a",
        audio_codecs[video_format],
        # constant bitrate
        "-b:a",
        "48k",
    ]


def preset_360p(video_format):
    return [
        "-codec:v",
        video_codecs[video_format],
        # keep good quality image
        "-qmin",
        "16",
        "-qmax",
        "26",
        # best compression
        "-quality",
        "best",
        # set constant rate
        "-minrate",
        "384k",
        "-maxrate",
        "384k",
        "-b:v",
        "384k",
        # scale to 360p 4:3, adding bars if necessary
        "-vf",
        "scale=640:360:force_original_aspect_ratio=decrease,"
        "pad=640:360:(ow-iw)/2:(oh-ih)/2",
        "-codec:a",
        audio_codecs[video_format],
        # constant bitrate
        "-b:a",
        "48k",
    ]


def preset_previous(video_format):
    return [
        # target video codec
        "-codec:v",
        video_codecs[video_format],
        # compression efficiency
        "-quality",
        "best",
        # increases encoding speed by degrading quality (0: don't speed-up)
        "-cpu-used",
        "0",
        # set output video average bitrate
        "-b:v",
        "300k",
        # quality range (min, max), the higher the worst quality
        # qmin 0 qmax 1 == best quality
        # qmin 50 qmax 51 == worst quality
        "-qmin",
        "30",
        "-qmax",
        "42",
        # constrain quality to not exceed this bitrate
        "-maxrate",
        "300k",
        # decoder buffer size, which determines the variability of the output bitrate
        "-bufsize",
        "1000k",
        # nb of threads to use
        "-threads",
        "8",
        # change output video dimensions
        "-vf",
        "scale='480:trunc(ow/a/2)*2'",
        # target audio codec
        "-codec:a",
        audio_codecs[video_format],
        # set output audio average bitrate
        "-b:a",
        "128k",
    ]


TEST_VIDEOS = collections.OrderedDict(
    [
        ("BupG57U82NI", "mali"),
        ("vIdStMTgNl0", "TEDED"),
        ("h--n1rnifT8", "thaki"),
        ("I7cajVnzm8k", "passorcier"),
        ("pLlv2o6UfTU", "crashcourse"),
        ("VJNt1AQ8p2A", "dirtybiology"),
        ("PFjX5tgu0iQ", "hygienementale"),
        ("ldH4_QwekuM", "fondamentaux"),
        ("N01db5Y-3B8", "notabene"),
    ]
)
PRESETS = collections.OrderedDict(
    [("previous", preset_previous), ("240p", preset_240p), ("360p", preset_360p)]
)
VIDEO_FORMATS = ["webm", "mp4"]  # ["webm", "mp4"]
VIDEOS = TEST_VIDEOS.keys()


def download_original(output_dir, youtube_id, video_format):
    expected_path = output_dir.joinpath(f"{youtube_id}.orig.{video_format}")
    if expected_path.exists():
        return expected_path
    fpath = expected_path.parent.joinpath(expected_path.stem)
    audext, vidext = {"webm": ("webm", "webm"), "mp4": ("m4a", "mp4")}[video_format]
    subprocess.run(
        [
            "/usr/bin/env",
            "youtube-dl",
            "-o",
            f"{fpath}.%(ext)s",
            "-f",
            f"best[ext={vidext}]/bestvideo[ext={vidext}]+bestaudio[ext={audext}]/best",
            youtube_id,
        ],
        capture_output=True,
        text=True,
        check=True,
    )


def get_src_path(output_dir: pathlib.Path, youtube_id, video_format):
    video_format_path = output_dir.joinpath(f"{youtube_id}.orig.{video_format}")
    if video_format_path.exists():
        return video_format_path


def convert_video(output_dir, youtube_id, video_format, preset):
    if preset not in PRESETS:
        raise ValueError(f"invalid preset {preset}")

    src_path = get_src_path(output_dir, youtube_id, video_format)
    dst_path = output_dir.joinpath(f"{youtube_id}.{preset}.{video_format}")
    if dst_path.exists():
        return dst_path

    args = ["ffmpeg", "-y", "-i", f"file:{src_path}"]
    args += PRESETS[preset](video_format)
    args += params[video_format]
    args += ["-max_muxing_queue_size", "9999"]
    args += [f"file:{dst_path}"]

    subprocess.run(args, capture_output=True, text=True, check=True)

    return dst_path


def get_duration_for(output_dir, youtube_id):
    src_path = get_src_path(output_dir, youtube_id, "webm")
    args = [
        "ffprobe",
        "-i",
        f"file:{src_path}",
        "-show_entries",
        "format=duration",
        "-v",
        "quiet",
        "-of",
        "csv",
    ]
    print(" ".join(args))
    ffprobe = subprocess.run(args, capture_output=True, text=True, check=False)
    return int(ffprobe.stdout.strip().split(",", 1)[-1].split(".", 1)[0])


def write_html_report(output_dir, report):
    env = jinja2.Environment(autoescape=True)

    def hsize(value):
        return humanfriendly.format_size(value, binary=True)

    def hduration(value):
        return humanfriendly.format_timespan(value)

    def hsduration(value):
        if value >= 3600:  # noqa: PLR2004
            hours = value // 3600
            value = value % 3600
        else:
            hours = 0
        if value >= 60:  # noqa: PLR2004
            minutes = value // 60
            value = value % 60
        else:
            minutes = 0
        return f"{hours:02}:{minutes:02}:{value:02}"

    env.filters["hsize"] = hsize
    env.filters["hduration"] = hduration
    env.filters["hsduration"] = hsduration
    env.filters["mn"] = lambda x: x * 60
    env.filters["p1"] = lambda x: x + 1
    env.filters["vname"] = lambda x: TEST_VIDEOS[x]

    html_template = """<!doctype html><html>
<head>
<meta charset="utf-8">
<title>Comparison</title>
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<link rel="stylesheet"
    href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
</head>
<body>
<div class="container-fluid">
<table class="table table-stripped table-sm">
<thead>
<tr>
    <th rowspan="2">VideoID</th>
    <th rowspan="2">Duration</th>
    {% for video_format in video_formats %}
    <th colspan="{{presets|length|p1}}">{{video_format}}</th>
    {% endfor %}
</tr>
<tr>
    {% for video_format in video_formats %}
        <th>Size</th>
        {% for preset in presets %}
            <th>{{preset}}</th>
        {% endfor %}
    {% endfor %}
</tr>
</thead>
<tbody>
{% for youtube_id, video in report.items() %}
    <tr>
        <th><a target="_blank"
            href="https://youtube.com/watch?v={{youtube_id}}">{{youtube_id|vname}}</a></th>
        <td title="{{video.duration|hduration}}">{{video.duration|hsduration}}</td>
        {% for video_format in video_formats %}
            <td>
                {{video[video_format].size|hsize}}<br />
                {{video[video_format].bitrate|hsize}}/s<br />
                {{video[video_format].bitrate|mn|hsize}}/mn
            </td>
            {% for preset in presets %}
            <td>
                {{video[video_format][preset].size|hsize}}<br />
                {{video[video_format][preset].bitrate|hsize}}/s<br />
                <strong>{{video[video_format][preset].bitrate|mn|hsize}}/mn</strong>
                <br />
                <a target="_blank"
                    href="{{youtube_id}}.{{preset}}.{{video_format}}">{{preset}}.{{video_format}}</a>
            </td>
            {% endfor %}
        {% endfor %}
    </tr>
{% endfor %}
</tbody>
</table>
</div>
</body>
</html>

    """
    # page = jinja2.Template(html_template).render(report=report)
    page = env.from_string(html_template).render(
        report=report, video_formats=VIDEO_FORMATS, presets=PRESETS
    )
    with open(output_dir.joinpath("report.html"), "w") as fh:
        fh.write(page)


def main(output_dir: pathlib.Path):
    if not output_dir.exists() or not output_dir.is_dir():
        print(f"{output_dir} is not a valid directory.")
        return 1

    report = {}

    for youtube_id in VIDEOS:
        report[youtube_id] = {}
        for video_format in VIDEO_FORMATS:
            report[youtube_id][video_format] = {}
            print(f"downloading {youtube_id}/{video_format}")
            download_original(output_dir, youtube_id, video_format)

            if video_format == "webm":
                report[youtube_id]["duration"] = get_duration_for(
                    output_dir, youtube_id
                )
            src_path = get_src_path(output_dir, youtube_id, video_format)
            if not src_path:
                raise Exception(
                    f"src_path of {output_dir}, {youtube_id}, {video_format} is missing"
                )
            report[youtube_id][video_format]["size"] = src_path.stat().st_size

            report[youtube_id][video_format]["bitrate"] = (
                report[youtube_id][video_format]["size"]
                // report[youtube_id]["duration"]
            )

            for preset in PRESETS.keys():
                started_on = datetime.datetime.utcnow()
                print(f"converting {youtube_id}/{video_format}/{preset}")
                fpath = convert_video(output_dir, youtube_id, video_format, preset)
                encoding_duration = (
                    datetime.datetime.utcnow() - started_on
                ).total_seconds()
                size = fpath.stat().st_size
                report[youtube_id][video_format][preset] = {
                    "encoding_duration": encoding_duration,
                    "size": size,
                    "hsize": humanfriendly.format_size(size, binary=True),
                    "bitrate": size // report[youtube_id]["duration"],
                }

    with open(output_dir.joinpath("report.json"), "w") as fh:
        json.dump(report, fh, indent=4)
    from pprint import pprint as pp

    pp(report)
    write_html_report(output_dir, report)


if __name__ == "__main__":
    nb_expected_args = 2
    if len(sys.argv) != nb_expected_args:
        print("you must pass a target folder")
        sys.exit(1)
    sys.exit(main(pathlib.Path(sys.argv[1])))
