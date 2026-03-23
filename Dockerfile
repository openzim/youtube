FROM node:24-alpine as zimui

WORKDIR /src
COPY . /src
RUN cd zimui && yarn install --frozen-lockfile
RUN cd zimui && yarn build

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

CMD ["youtube2zim", "--help"]
