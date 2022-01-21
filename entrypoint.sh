#!/bin/sh

echo "Attempting to update youtube-dl…"
# pip3 install -U youtube-dl
# TEMP: awaiting post 2021.12.17 which would include an important fix
pip3 install --force-reinstall -U git+https://github.com/ytdl-org/youtube-dl@905d1d281ddfa5d183fc445010d350cefc6a58ec


exec "$@"
