#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import pathlib
import subprocess
from setuptools import setup

root_dir = pathlib.Path(__file__).parent


def read(*names, **kwargs):
    with open(root_dir.joinpath(*names), "r") as fh:
        return fh.read()


print("Downloading and fixing JS dependencies...")
ps = subprocess.run([str(root_dir.joinpath("get_js_deps.sh").resolve())])
ps.check_returncode()


setup(
    name="youtube2zim",
    version=read("youtube2zim", "VERSION").strip(),
    description="Make ZIM file from a Youtube channel, user or playlist(s)",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="dattaz",
    author_email="taz@dattaz.fr",
    url="https://github.com/openzim/youtube",
    keywords="kiwix zim youtube offline",
    license="GPLv3+",
    packages=["youtube2zim"],
    install_requires=[
        line.strip()
        for line in read("requirements.txt").splitlines()
        if not line.strip().startswith("#")
    ],
    zip_safe=False,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "youtube2zim=youtube2zim.__main__:main",
            "youtube2zim-playlists=youtube2zim.playlists.__main__:main",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    python_requires=">=3.6",
)
