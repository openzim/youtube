FROM openzim/zimwriterfs:1.3.5

# Install necessary packages
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends locales-all python3-pip ffmpeg aria2 curl unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install setuptools

COPY . /src
RUN cd /src/ && python3 ./setup.py install

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
CMD youtube2zim --help
