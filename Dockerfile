FROM python:3.8

# add zimwriterfs
ENV ZIMWRITERFS_VERSION 1.3.10
RUN wget http://download.openzim.org/release/zimwriterfs/zimwriterfs_linux-x86_64-${ZIMWRITERFS_VERSION}.tar.gz
RUN tar -C /usr/bin --strip-components 1 -xf zimwriterfs_linux-x86_64-${ZIMWRITERFS_VERSION}.tar.gz
RUN rm -f zimwriterfs_linux-x86_64-${ZIMWRITERFS_VERSION}.tar.gz
RUN chmod +x /usr/bin/zimwriterfs
RUN zimwriterfs --version

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

CMD ["youtube2zim", "--help"]
