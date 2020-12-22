FROM python:3.8
LABEL org.opencontainers.image.source https://github.com/openzim/youtube

# Install necessary packages
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends locales-all wget unzip ffmpeg aria2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY youtube2zim /src/youtube2zim
COPY get_js_deps.sh requirements.txt setup.py README.md LICENSE MANIFEST.in /src/
RUN pip3 install $(grep "zimscraperlib" /src/requirements.txt)
RUN cd /src/ && python3 ./setup.py install

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

RUN mkdir -p /output
WORKDIR /output
CMD ["youtube2zim", "--help"]
