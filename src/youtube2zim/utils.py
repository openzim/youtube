#!/usr/bin/env python3
# vim: ai ts=4 sts=4 et sw=4 nu

import json
from pathlib import Path
import multiprocessing
import youtube_dl
import re

import jinja2
from slugify import slugify


def get_slug(text, *, js_safe=True):
    """slug from text to build URL parts"""
    if js_safe:
        return slugify(text, regex_pattern=r"[^-a-z0-9_]+").replace("-", "_")
    return slugify(text)


def clean_text(text):
    """cleaned-down version of text as Youtube is very permissive with descriptions"""
    return text.strip().replace("\n", " ").replace("\r", " ")


def save_json(cache_dir: Path, key, data):
    """save JSON collection to path"""
    with open(cache_dir.joinpath(f"{key}.json"), "w") as fp:
        json.dump(data, fp, indent=4)


def load_json(cache_dir: Path, key):
    """load JSON collection from path or None"""
    fname = cache_dir.joinpath(f"{key}.json")
    if not fname.exists():
        return None
    try:
        return json.loads(fname.read_bytes())
    except Exception:
        return None


def load_mandatory_json(cache_dir: Path, key):
    """load mandatory JSON collection from path"""
    return json.loads(cache_dir.joinpath(f"{key}.json").read_bytes())


def has_argument(arg_name, all_args):
    """whether --arg_name is specified in all_args"""
    return list(filter(lambda x: x.startswith(f"--{arg_name}"), all_args))


def render_template(env: jinja2.Environment, template_name: str, **kwargs):
    """render a Jinja template and ensures that result is a string"""
    html = env.get_template(template_name).render(kwargs)
    if not isinstance(html, str):
        raise Exception("Jinja template did not return a string")
    return html


def generate_subtitles(video_id):
    # this will just generate the subtitles, can change for the speed
    options = {
        'writesubtitles': True,
        'subtitleslang': ['en'],
        'outtmpl':f'{video_id}.%(ext)s' #ext here is the extension, just to specify the output file name 
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([f'http://www.youtube.com/watch?v={video_id}'])
    


def generate_all_subtitles(video_ids):
    # using multiprocessing, generating all the video id's
    with multiprocessing.Pool() as pool:
        pool.map(generate_subtitles, video_ids)
        
def extract_video_id(url):
    match = re.match(r'^https?://(?:www\.)?youtube\.com/watch\?v=([^\s&]+)', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("This URL is invalid")
        


if __name__ == "__main__":
    
    video_ids = ["https://www.youtube.com/watch?v=4p2HsIAqitg"]
    video_ids = [extract_video_id(url) for url in video_ids]
    generate_all_subtitles(video_ids)
