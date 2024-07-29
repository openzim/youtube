Youtube2zim
=============

[![CodeFactor](https://www.codefactor.io/repository/github/openzim/youtube/badge)](https://www.codefactor.io/repository/github/openzim/youtube)
[![Docker](https://ghcr-badge.deta.dev/openzim/youtube/latest_tag?label=docker)](https://ghcr.io/openzim/youtube)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI version shields.io](https://img.shields.io/pypi/v/youtube2zim.svg)](https://pypi.org/project/youtube2zim/)

`youtube2zim` allows you to create a [ZIM file](https://openzim.org)
from a Youtube Channel/Username or one-or-more Playlists.

It downloads the videos (`webm` or `mp4` extension – optionally
recompress them in lower-quality, smaller size), the thumbnails, the
subtitles and the authors' profile pictures; It then produces JSON files containing content for the channel, playlists, and videos, which are used by the UI, which is a Vue.js application that needs to be compiled as a static website with Vite and is then embedded inside the ZIM.

`youtube2zim` adheres to openZIM's [Contribution Guidelines](https://github.com/openzim/overview/wiki/Contributing).

`youtube2zim` has implemented openZIM's [Python bootstrap, conventions and policies](https://github.com/openzim/_python-bootstrap/blob/main/docs/Policy.md) **v1.0.2**.

Requirements
------------

* [`ffmpeg`](https://ffmpeg.org/) for video transcoding.
* [`Yarn`](https://yarnpkg.com/getting-started/install) to install Javascript dependencies for the Vue.js UI.

Installation
------------

Here comes a few different ways to install `youtube2zim`.

## Virtualenv

`youtube2zim` is a Python3 software. If you are not using the [Docker](https://docker.com) image,
you are advised to use it in a [virtualenv](https://virtualenv.pypa.io) to avoid installing software
dependencies on your system. [Hatch](https://hatch.pypa.io/) is the proper tool to create the
virtualenv and install the software locally. Ensure to use proper Python version as well (see
pyproject.toml).

If you do not already have it on your system, install hatch to build the software and manage virtual
environments (you might be interested by our detailed
[Developer Setup](https://github.com/openzim/_python-bootstrap/blob/main/docs/Developer-Setup.md) as well,
especially regarding how to configure hatch globally for proper detection of its virtual environments
by Visual Studio Code).

``` bash
pip3 install hatch
```

Start a hatch shell: this will install software including dependencies in an isolated virtual environment.

``` bash
cd scraper
hatch shell
```

```bash
youtube2zim --help       # Display youtube2zim help
```

## Docker

```bash
docker run -v my_dir:/output ghcr.io/openzim/youtube youtube2zim --help
```

Usage
-----

`youtube2zim` uses Youtube API v3 to fetch data from Youtube. You thus need to provide an `API_KEY` to use the scraper.

To get an API:

1. Connect to [Google Developers Console](https://console.developers.google.com/apis)
2. Create a new _Project_ then Select it.
3. When asked, choose _Create Credentials_ and select the **API Key** type. ([Credentials page](https://console.developers.google.com/apis/credentials))

```bash
youtube2zim --api-key "<your-api-key>" --type user --id "Vsauce" --name "vsauce"
```

## Notes

* Your API_KEY is subject to usage quotas (10,000 requests/day by default). Be careful to not waste your quota, especially when scraping large channels.

youtube2zim-playlists
---------------------

`youtube2zim` produces a single ZIM file for a youtube request (`channel`, `user`, `playlist`).

`youtube2zim-playlists` allows you to **automatically create one ZIM file per playlist** of a given channel or user instead.

This script is a wrapper around `youtube2zim` and is bundled with the main package.

The difference between a channel and a user is due to Youtube legacy. Some old users have to be searched as a user, while more recent ones have to be searched as a channel. Try your best bet, and if it fails try the other type.

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
