Youtube2zim
=============

[![CodeFactor](https://www.codefactor.io/repository/github/openzim/youtube/badge)](https://www.codefactor.io/repository/github/openzim/youtube)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI version shields.io](https://img.shields.io/pypi/v/youtube2zim.svg)](https://pypi.org/project/youtube2zim/)

`youtube2zim` allows you to create a [ZIM file](https://openzim.org) from a Youtube Channel/username or one-or-more Playlists.

It downloads the video (webm or mp4 format – optionnaly recompress them in lower-quality, smaller size), the thumbnails, the subtitles and the authors' profile pictures ; then, it create a static HTML files folder of it before creating a ZIM off of it.

# Requirements

* [`ffmpeg`](https://ffmpeg.org/) for video transcoding (only used with `--lower-quality`).
* [`zimwriterfs`](https://github.com/openzim/zimwriterfs) for ZIM file packaging. Use `--no-zim` to skip this step.
* `curl` and `unzip` to install JS dependencies. See `get_js_deps.sh` if you want to do it manually.

# Installation

`youtube2zim` is a python program. if you are not using the docker image, you are advised to use it in a virtualenv. See `requirements.txt` for the list of python dependencies.

## docker

```
docker run -v my_dir:/output openzim/youtube youtube2zim --help
```

## pip

```
pip install youtube2zim
youtube2zim --help
```

## source

```
python youtube2zim --help
```

# Usage

`youtube2zim` uses Youtube API v3 to fetch data from Youtube. You thus need to provide an `API_KEY` to use the scraper.

To get an API:

1. Connect to [Google Developers Console](https://console.developers.google.com/apis)
2. Create a new _Project_ then Select it.
3. When asked, choose _Create Credentials_ and select the **API Key** type. ([Credentials page](https://console.developers.google.com/apis/credentials))

```
youtube2zim --api-key "<your-api-key>" --type user --id "Vsauce"
```

## Notes

* Your API_KEY is subject to usage quotas (10,000 requests/day) so use `--keep --skip-download` when adjusting parameters and branding to not *waste your quota*.
* On macOS, the locale setting is buggy. You need to launch it with `LANGUAGE` environment variable (as ISO-639-1) for the translations to work.

```
LANGUAGE=fr youtube2zim --language fra
```

# Developers note

In order to support all platform, we default to `webm` video format. `mp4` one (h264), is not available in Webview on most platform due to patent restrictions.

On the other hand, `webm` is not supported in Safari (macOS, iOS).

We thus use `ogv.js`, to play webm videos on browsers that don't support it. Using `video.js`, we default to native playback if supported.

`ogv.js` is an emscripten-based JS decoder for webm and thus dynamically loads differents parts at run-time on platforms that needs them. It has two consequences:

* `file://` scheme doesn't work as the binary `.wasm` files are sent naively as `text/html` instead of `application/oct-stream`. If you want to use the HTML generated folder instead of ZIM, serve it through a web server and [configure the Content-Type response](https://emscripten.org/docs/compiling/WebAssembly.html#web-server-setup).
* [ZIM](https://wiki.openzim.org/wiki/ZIM_file_format) places JS files under the `/-/` namespace and binary ones under the `/I/` one. Dynamically loading of JS and WASM files within `ogv.js` requires us to tweak it to introduce some ZIM-specific logic. See `fix_ogvjs_dist.py`.

Because the pagination system is implemented in JS, we also need to generate links there. For that to work both in static HTML and in-ZIM, we detect it using a `<link id="favicon">` in HTML files. This link needs to be present and parsed before loading the help `zim_prefix.js` script.


## i18n

`youtube2zim` has very minimal non-content text but still uses gettext through [babel]() to internationalize.

To add a new locale (`fr` in this example, use only ISO-639-1):

1. init for your locale: `pybabel init -d locale -l fr`
2. make sure the POT is up to date `pybabel extract -o youtube2zim/locale/messages.pot youtube2zim`
3. update your locale's catalog `pybabel update -d youtube2zim/locale/ -l fr -i youtube2zim/locale/messages.pot`
3. translate the PO file ([poedit](https://poedit.net/) is your friend)
4. compile updated translation `pybabel compile -d youtube2zim/locale -l fr`
