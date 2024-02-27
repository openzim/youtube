#!/usr/bin/env python3
# vim: ai ts=4 sts=4 et sw=4 nu

import sys

from youtube2zim.entrypoint import main
from youtube2zim.utils import generate_all_subtitles

if __name__ == "__main__":
    sys.exit(main())
    
if __name__ == "__main__":
    
    video_ids = ["v1", "v2", "v3"]
    generate_all_subtitles(video_ids)
