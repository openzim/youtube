#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import sys
import pathlib


def main():
    # allows running it from source using python youtube2zim
    sys.path = [str(pathlib.Path(__file__).parent.parent.parent.resolve())] + sys.path

    from youtube2zim.playlists.entrypoint import main as entry

    entry()


if __name__ == "__main__":
    main()
