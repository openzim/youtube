#!/bin/sh

echo "Attempting to update yt-dlp…"
pip3 install -U yt-dlp

# The bundled PO token provider is started in the background, like the bundled
# redis of mwoffliner. yt-dlp finds it on 127.0.0.1:4416 without any flag, so
# the default needs no configuration, and --yt-dlp-extractor-arg still lets a
# caller point somewhere else. If the provider dies, yt-dlp logs a warning and
# falls back to running without a PO token.
if [ -x /usr/local/bin/bgutil-pot ]; then
  echo "starting bgutil-pot in the background…"
  nohup /usr/local/bin/bgutil-pot server --host 127.0.0.1 --port 4416 > /tmp/bgutil-pot.log 2>&1 &

  # allow the provider to bind before we continue, otherwise the first few
  # videos would be requested before it is listening
  python3 - <<'EOF'
import socket
import time

deadline = time.monotonic() + 30
while time.monotonic() < deadline:
    try:
        with socket.create_connection(("127.0.0.1", 4416), timeout=1):
            break
    except OSError:
        time.sleep(0.5)
else:
    print("warning: PO token provider did not start, see /tmp/bgutil-pot.log")
EOF
fi

exec "$@"