Youtube2zim
=============

[![CodeFactor](https://www.codefactor.io/repository/github/openzim/youtube/badge)](https://www.codefactor.io/repository/github/openzim/youtube)
[![Docker Build Status](https://img.shields.io/docker/build/openzim/youtube)](https://hub.docker.com/r/openzim/youtube)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI version shields.io](https://img.shields.io/pypi/v/youtube2zim.svg)](https://pypi.org/project/youtube2zim/)

`youtube2zim` allows you to create a [ZIM file](https://openzim.org)
from a Youtube Channel/Username or one-or-more Playlists.

It downloads the video (`webm` or `mp4` extension – optionnaly
recompress them in lower-quality, smaller size), the thumbnails, the
subtitles and the authors' profile pictures ; then, it create a static
HTML files folder of it before creating a ZIM off of it.

Requirements
------------

* [`ffmpeg`](https://ffmpeg.org/) for video transcoding (only used with `--lower-quality`).
* [`zimwriterfs`](https://github.com/openzim/zimwriterfs) for ZIM file packaging. Use `--no-zim` to skip this step.
* `curl` and `unzip` to install Javascript dependencies. See `get_js_deps.sh` if you want to do it manually.

Installation
------------

Here comes a few different ways to install `youtube2zim`.

## Virtualenv

`youtube2zim` is a Python3 software. If you are not using the
[Docker](https://docker.com) image, you are advised to use it in a
[virtualenv](https://virtualenv.pypa.io) to avoid installing software
dependences on your system.

```bash
virtualenv -p python3 ./ # Create virtualenv
source bin/activate      # Activate the virtualenv
pip3 install youtube2zim # Install dependencies
youtube2zim --help       # Display youtube2zim help
```

At the end, call `deactivate` to quit the virtual environment.

See `requirements.txt` for the list of python dependencies.

## Docker

```bash
docker run -v my_dir:/output openzim/youtube youtube2zim --help
```

## Globally (on GNU/Linux)

```bash
sudo pip3 install -U youtube2zim
```

Usage
-----

`youtube2zim` uses Youtube API v3 to fetch data from Youtube. You thus need to provide an `API_KEY` to use the scraper.

To get an API:

1. Connect to [Google Developers Console](https://console.developers.google.com/apis)
2. Create a new _Project_ then Select it.
3. When asked, choose _Create Credentials_ and select the **API Key** type. ([Credentials page](https://console.developers.google.com/apis/credentials))

```bash
youtube2zim --api-key "<your-api-key>" --type user --id "Vsauce"
```

## Notes

* Your API_KEY is subject to usage quotas (10,000 requests/day) so use `--only_test_branding` when adjusting parameters and branding to not *waste your quota*.
* If you encounter issues reading ZIM files created using this scraper, please take a look at the [Compatibility Matrix](https://github.com/openzim/youtube/wiki/Compatibility) before opening a ticket.

youtube2zim-playlists
---------------------

`youtube2zim` produces a single ZIM file for a youtube request (`channel`, `user`, `playlists`.

`youtube2zim-playlists` allows you to **create one ZIM file per playlist** instead.

This script is a wrapper around `youtube2zim` and is bundled with the main package.

## Usage

`youtube2zim-playlists --help`

Sample usage:

```
youtube2zim-playlists --indiv-playlists --api-key XXX --type user --id Vsauce --playlists-name="vsauce_en_playlist-{playlist_id}"
```

Those are the required arguments for `youtube2zim-playlists` but **you can also pass any regular `youtube2zim` argument**. Those will be forwarded to `youtube2zim` (which will be run independently for each playlist).

**Specificities**:

- `--title` and `--description` are mutually exclusive with `--playlists-title` and `--playlists-description`.
- If using `--title` or `--description`, all your playlists ZIMs will have the same, static metadata. This is rarely wanted.
- `--playlists-title` and `--playlists-description` allows you to dynamically customize them via some playlist-related variables:
  - `{title}`: the playlist title
  - `{description}`: the playlist description
  - `{slug}`: slugified version of the playlist title
  - `{playlist_id}`: playlist ID on youtube
  - `{creator_id}`: playlist's owner channel/user ID.
  - `{creator_name}`: playlist's owner channel/user name.
- You can omit them and `youtube2zim` will auto-generate those.
- you **must specify `--playlists-name`** (supports variables listed above).
- `--playlists-name` is used to set the `Name` metadata of the ZIM (should be unique) and if not set separately, the output file name for the ZIM.
- `--metadata-from` allows to specify a path or URL to a JSON file specifying custom static metadata for individual playlists. Format:

``` json
{
    "<playlist-id>": {
        "name": "",
        "zim-file": "",
        "title": "",
        "description": "",
        "tags": "",
        "creator": "",
        "profile": "",
        "banner": ""
    }
}
```

All fields are optional and taken from command-line/default if not found. `<playlist-id>` represents the Youtube Playlist ID.

If you feel the need for setting additional details in this file, chances are you should run `youtube2zim` independently for that playlist (still possible!)

Development
-----------

Before contributing be sure to check out the
[CONTRIBUTING.md](CONTRIBUTING.md) guidelines.

License
-------

[GPLv3](https://www.gnu.org/licenses/gpl-3.0) or later, see
[LICENSE](LICENSE) for more details.
