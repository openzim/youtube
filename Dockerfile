FROM openzim/zimwriterfs:1.3.5

# Install necessary packages
RUN apt-get update -y && apt-get install -y %% \
    --no-install-recommends python3-pip ffmpeg aria2 && \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /src
RUN cd /src/ && python3 ./setup.py install

# Boot commands
CMD youtube2zim --help
