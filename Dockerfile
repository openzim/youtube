FROM node:20-alpine as zimui

WORKDIR /src
COPY zimui /src
RUN yarn install --frozen-lockfile
RUN yarn build

FROM python:3.13-bookworm
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

# Install Python dependencies
RUN pip install --no-cache-dir /src/scraper

# Copy code + associated artifacts
COPY scraper/src /src/scraper/src
COPY *.md LICENSE CHANGELOG.md /src/

# Install + cleanup
RUN pip install --no-cache-dir /src/scraper \
 && rm -rf /src/scraper

# Copy zimui build output
COPY --from=zimui /src/dist /src/zimui

ENV YOUTUBE_ZIMUI_DIST=/src/zimui

CMD ["youtube2zim", "--help"]
