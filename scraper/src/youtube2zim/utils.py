#!/usr/bin/env python3
# vim: ai ts=4 sts=4 et sw=4 nu

import json
import os
import re
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


def parse_extractor_args(values):
    """turn yt-dlp-style `IE_KEY:ARG=VALUES` strings into a `extractor_args` dict

    Values are parsed exactly like yt-dlp parses its own `--extractor-args`:
    extractor and argument names are lower-cased with dashes turned into
    underscores, each value is a comma-separated list, a backslash escapes a
    literal comma, and every value is stored as a list of strings since that is
    the only shape yt-dlp reads.

    One deliberate difference: passing the same extractor twice merges the
    arguments instead of replacing them. yt-dlp's command line keeps only the
    last one, which silently drops whatever was set before."""

    extractor_args: dict[str, dict[str, list[str]]] = {}
    for value in values or []:
        ie_key, _, args = value.partition(":")
        ie_key = ie_key.strip().lower()
        if not ie_key or not args.strip():
            raise ValueError(
                f"Invalid extractor argument `{value}`. "
                "Expected IE_KEY:ARG=VALUES, such as "
                "`youtubepot-bgutilhttp:base_url=http://127.0.0.1:4416`"
            )
        for arg in args.split(";"):
            if not arg.strip():
                continue
            name, separator, arg_values = arg.partition("=")
            name = name.strip().lower().replace("-", "_")
            if not separator or not name:
                raise ValueError(
                    f"Invalid extractor argument `{value}`. "
                    "Expected IE_KEY:ARG=VALUES, such as "
                    "`youtubepot-bgutilhttp:base_url=http://127.0.0.1:4416`"
                )
            extractor_args.setdefault(ie_key, {})[name] = [
                val.replace(r"\,", ",").strip()
                for val in re.split(r"(?<!\\),", arg_values)
            ]
    return extractor_args


def delete_callback(fpath: str | Path):
    """callback to delete file"""
    if Path(fpath).exists():
        os.unlink(fpath)
