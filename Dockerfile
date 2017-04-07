FROM openzim/zimwriterfs:latest

# Install necessary packages
RUN apt-get install -y python-pip

# Install sotoki
RUN locale-gen "en_US.UTF-8"
RUN pip install youtube2zim

# Boot commands
CMD youtube2zim ; /bin/bash
