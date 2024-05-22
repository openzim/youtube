FROM python:3.12-bookworm
LABEL org.opencontainers.image.source https://github.com/openzim/youtube

# Install necessary packages
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      locales-all \
      wget \
      unzip \
      ffmpeg \
      aria2 \
 && rm -rf /var/lib/apt/lists/* \
 && python -m pip install --no-cache-dir -U \
      pip

# Custom entrypoint
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
RUN mkdir -p /output
WORKDIR /output

# Copy pyproject.toml and its dependencies
COPY pyproject.toml README.md openzim.toml /src/
COPY src/youtube2zim/__about__.py /src/src/youtube2zim/__about__.py

# Install Python dependencies
RUN pip install --no-cache-dir /src

# Copy code + associated artifacts
COPY src /src/src
COPY *.md LICENSE CHANGELOG /src/

# Install + cleanup
RUN pip install --no-cache-dir /src \
 && rm -rf /src

CMD ["youtube2zim", "--help"]
