Youtube2zim
=============

[![CodeFactor](https://www.codefactor.io/repository/github/openzim/youtube/badge)](https://www.codefactor.io/repository/github/openzim/youtube)
[![Docker](https://ghcr-badge.egpl.dev/openzim/youtube/latest_tag?label=docker)](https://ghcr.io/openzim/youtube)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI version shields.io](https://img.shields.io/pypi/v/youtube2zim.svg)](https://pypi.org/project/youtube2zim/)

`youtube2zim` allows you to create a [ZIM file](https://openzim.org)
from a Youtube Channel/Username or one-or-more Playlists.

It downloads the videos (`webm` or `mp4` extension – optionally
recompress them in lower-quality, smaller size), the thumbnails, the
subtitles and the authors' profile pictures; It then produces JSON files containing content for the channel, playlists, and videos, which are used by the UI, which is a Vue.js application that needs to be compiled as a static website with Vite and is then embedded inside the ZIM.

`youtube2zim` adheres to openZIM's [Contribution Guidelines](https://github.com/openzim/overview/wiki/Contributing).

`youtube2zim` has implemented openZIM's [Python bootstrap, conventions and policies](https://github.com/openzim/_python-bootstrap/blob/main/docs/Policy.md) **v1.0.2**.

# Documentation

For more details / advanced usage than what is in this README, see the [Manual](https://github.com/openzim/youtube/wiki/Manual) and [FAQ/FEE](https://github.com/openzim/youtube/wiki/FAQ---FEE).

# Requirements

* [`ffmpeg`](https://ffmpeg.org/) for video transcoding.
* [`Yarn`](https://yarnpkg.com/getting-started/install) to install Javascript dependencies for the Vue.js UI.

# Installation

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

# Usage

`youtube2zim` uses Youtube API v3 to fetch data from Youtube. You thus need to provide an `API_KEY` to use the scraper.

To get an API Key:

1. Connect to [Google Developers Console](https://console.developers.google.com/apis)
2. Create a new _Project_ then Select it.
3. When asked, choose _Create Credentials_ and select the **API Key** type. ([Credentials page](https://console.developers.google.com/apis/credentials))

You can then create a ZIM from a singe channel / user / handle like `Vsauce`:

```bash
youtube2zim --api-key "<your-api-key>" --id "Vsauce" --name "tests_hi_avanti"
```

When scraping a channel, you must pass one single value in `--id` and it can be the handle, user, or even the corresponding technical ID (see [FAQ/FEE](https://github.com/openzim/youtube/wiki/FAQ---FEE) for more details).

Or you can create a ZIM from two playlists like `PL3rEvTTL-Jm8cBdskZoQaDTlDT4t7F6kp` and `PL3rEvTTL-Jm_OuyYpMfxtJW3Mcr9fFS2Z`:

```bash
youtube2zim --api-key "<your-api-key>" --id "PL3rEvTTL-Jm8cBdskZoQaDTlDT4t7F6kp,PL3rEvTTL-Jm_OuyYpMfxtJW3Mcr9fFS2Z" --name "tests_hi_avanti"
```

When scraping playlists, you can pass multiple playlist IDs separated by a comma in `--id`.

For more details / advanced usage, see the [Manual](https://github.com/openzim/youtube/wiki/Manual).

## Notes

* Your API_KEY is subject to usage quotas (10,000 requests/day by default). Be careful to not waste your quota, especially when scraping large channels.

# youtube2zim-playlists

`youtube2zim` produces a single ZIM file for a youtube request (`channel`, `user`, `handle`, `playlist`).

`youtube2zim-playlists` allows you to **automatically create one ZIM file per playlist** of a given channel or user instead.

This script is a wrapper around `youtube2zim` and is bundled with the main package.

## Usage

Sample usage:

```
youtube2zim-playlists --indiv-playlists --api-key XXX --id Vsauce --playlists-name="vsauce_en_playlist-{playlist_id}"
```

Those are the required arguments for `youtube2zim-playlists` but **you can also pass any regular `youtube2zim` argument**. Those will be forwarded to `youtube2zim` (which will be run independently for each playlist).

For more details / advanced usage, see the [Manual](https://github.com/openzim/youtube/wiki/Manual).

# Development

Before contributing be sure to check out the
[CONTRIBUTING.md](CONTRIBUTING.md) guidelines.

# License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0) or later, see
[LICENSE](LICENSE) for more details.
