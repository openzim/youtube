#!/bin/sh

echo "Attempting to update youtube-dl…"
pip3 install -U youtube-dl

exec "$@"
