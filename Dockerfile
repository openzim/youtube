FROM node:24-alpine as zimui

WORKDIR /src
COPY . /src
RUN cd zimui && yarn install --frozen-lockfile
RUN cd zimui && yarn build

# PO token provider, bundled so the image works out of the box.
# GPL-3.0, compatible with this repository; source at
# https://github.com/jim60105/bgutil-ytdlp-pot-provider-rs
FROM ghcr.io/jim60105/bgutil-pot:v0.8.1 AS potprovider

FROM python:3.14-trixie
LABEL org.opencontainers.image.source https://github.com/openzim/youtube

# Install necessary packages
RUN apt-get update \
     && apt-get install -y --no-install-recommends \
     wget \
     unzip \
     ffmpeg \
     aria2 \
     && rm -rf /var/lib/apt/lists/* \
     && python -m pip install --no-cache-dir -U \
     pip

# Custom entrypoint
COPY scraper/entrypoint.sh /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
RUN mkdir -p /output
WORKDIR /output

# Copy pyproject.toml and its dependencies
COPY README.md /src/
COPY scraper/pyproject.toml /src/scraper/
COPY scraper/src/youtube2zim/__about__.py /src/scraper/src/youtube2zim/__about__.py

# Install deno (required by yt-dlp)
RUN curl -fsSL https://deno.land/install.sh | sh -s \
  && ln -s /root/.deno/bin/deno /usr/local/bin/deno

# Install Python dependencies
RUN pip install --no-cache-dir /src/scraper

# Copy code
COPY scraper/src /src/scraper/src

# Copy zimui build output
COPY --from=zimui /src/scraper/src/youtube2zim/zimui /src/scraper/src/youtube2zim/zimui

# Copy associated artifacts
COPY *.md LICENSE CHANGELOG.md /src/

# Install + cleanup
RUN pip install --no-cache-dir /src/scraper \
 && rm -rf /src/scraper

# The provider and the plugin yt-dlp needs to talk to it. The plugin is
# installed in yt-dlp's system plugin root (/etc/yt-dlp/plugins/<pkg>), which
# yt-dlp scans by default: no flag and no scraper code are involved.
COPY --from=potprovider /bgutil-pot /usr/local/bin/bgutil-pot
COPY --from=potprovider /client/yt_dlp_plugins /etc/yt-dlp/plugins/bgutil/yt_dlp_plugins
COPY --from=potprovider /licenses/LICENSE /licenses/bgutil-ytdlp-pot-provider-LICENSE

CMD ["youtube2zim", "--help"]
