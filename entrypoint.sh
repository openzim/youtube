#!/bin/sh

echo "Attempting to update yt-dlp…"
pip3 install -U yt-dlp


exec "$@"
