#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import re
import json
import locale
import gettext
import colorsys

import PIL
import iso639
import requests
import colorthief
from slugify import slugify
from resizeimage import resizeimage

from .constants import ROOT_DIR


def get_slug(text, js_safe=True):
    """ slug from text to build URL parts """
    if js_safe:
        return slugify(text, regex_pattern=r"[^-a-z0-9_]+").replace("-", "_")
    return slugify(text)


def clean_text(text):
    """ cleaned-down version of text as Youtube is very permissive with descriptions """
    return text.strip().replace("\n", " ").replace("\r", " ")


def save_json(cache_dir, key, data):
    """ save JSON collection to path """
    with open(cache_dir.joinpath(f"{key}.json"), "w") as fp:
        json.dump(data, fp, indent=4)


def load_json(cache_dir, key):
    """ load JSON collection from path or None """
    fname = cache_dir.joinpath(f"{key}.json")
    if not fname.exists():
        return None
    try:
        with open(fname, "r") as fp:
            return json.load(fp)
    except Exception:
        return None


def save_file(url, fpath):
    """ download a binary file from its URL """
    req = requests.get(url)
    req.raise_for_status()
    if not fpath.parent.exists():
        fpath.parent.mkdir(exist_ok=True)
    with open(fpath, "wb") as fp:
        fp.write(req.content)


def get_colors(image_path, use_palette=True):
    """ (main, secondary) HTML color codes from an image path """

    def rgb_to_hex(r, g, b):
        """ hexadecimal HTML-friendly color code for RGB tuple """
        return "#{}{}{}".format(*[str(hex(x)[2:]).zfill(2) for x in (r, g, b)]).upper()

    def solarize(r, g, b):
        # calculate solarized color for main
        h, l, s = colorsys.rgb_to_hls(float(r) / 256, float(g) / 256, float(b) / 256)
        r2, g2, b2 = [int(x * 256) for x in colorsys.hls_to_rgb(h, 0.95, s)]
        return r2, g2, b2

    ct = colorthief.ColorThief(image_path)

    if use_palette:
        # extract two main colors from palette, solarizing second as background
        palette = ct.get_palette(color_count=2, quality=1)

        # using the first two colors of the palette?
        mr, mg, mb = palette[0]
        sr, sg, sb = solarize(*palette[1])
    else:
        # extract main color from image and solarize it as background
        mr, mg, mb = ct.get_color(quality=1)
        sr, sg, sb = solarize(mr, mg, mb)

    return rgb_to_hex(mr, mg, mb), rgb_to_hex(sr, sg, sb)


def resize_image(fpath, width, height=None, to=None, method="width"):
    """ resize an image file (dimensions)

        methods: width, height, cover """
    with open(str(fpath), "rb") as fp:
        with PIL.Image.open(fp) as image:
            if method == "width":
                resized = resizeimage.resize(method, image, width)
            elif method == "height":
                resized = resizeimage.resize(method, image, height=height)
            else:
                resized = resizeimage.resize(method, image, [width, height])
    kwargs = {"JPEG": {"quality": 100}}
    resized.save(
        str(to) if to is not None else fpath, image.format, **kwargs.get(image.format)
    )


def is_hex_color(text):
    """ whether supplied text is a valid hex-formated color code """
    return re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", text)


def nicer_args_join(args):
    """ slightly better concateated list of subprocess args for display """
    nargs = args[0:1]
    for arg in args[1:]:
        nargs.append(arg if arg.startswith("-") else '"{}"'.format(arg))
    return " ".join(nargs)


def get_language_details(iso_639_3):
    """ dict container iso639-2, name and native name for an iso-639-3 code """
    non_iso_langs = {
        "zh-Hans": {
            "code": "zh-Hans",
            "iso-639-1": "zh",
            "english": "Simplified Chinese",
            "native": "简化字",
        },
        "zh-Hant": {
            "code": "zh-Hant",
            "iso-639-1": "zh",
            "english": "Traditional Chinese",
            "native": "正體字",
        },
        "iw": {"code": "iw", "iso-639-1": "he", "english": "Hebrew", "native": "עברית"},
        "es-419": {
            "code": "es-419",
            "iso-639-1": "es-419",
            "english": "Spanish",
            "native": "Español",
        },
        "multi": {
            "code": "mul",
            "iso-639-1": "en",
            "english": "Multiple Languages",
            "native": "Multiple Languages",
        },
    }

    try:
        return (
            non_iso_langs.get(iso_639_3)
            if iso_639_3 in non_iso_langs.keys()
            else {
                "code": iso_639_3,
                "iso-639-1": iso639.to_iso639_1(iso_639_3),
                "english": iso639.to_name(iso_639_3),
                "native": iso639.to_native(iso_639_3),
            }
        )
    except iso639.NonExistentLanguageError:
        return {
            "code": iso_639_3,
            "iso_639_3": iso_639_3,
            "english": iso_639_3,
            "native": iso_639_3,
        }


def setlocale(locale_name):
    computed = locale.setlocale(locale.LC_ALL, (locale_name.split(".")[0], "UTF-8"))
    gettext.bindtextdomain("messages", str(ROOT_DIR.joinpath("locale")))
    gettext.textdomain("messages")
    return computed
