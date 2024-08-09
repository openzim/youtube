#!/usr/bin/env python3
# vim: ai ts=4 sts=4 et sw=4 nu

import json
import os
from pathlib import Path

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


def delete_callback(fpath: str | Path):
    """callback to delete file"""
    if Path(fpath).exists():
        os.unlink(fpath)
