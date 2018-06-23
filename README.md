Youtube2zim
=============

`youtube2zim` scrappes a Youtube channel, playlist or user videos to a ZIM file.

Requirements
------------

You will need `ffmpeg` or `avconv` installed for video transcoding.

You will need `zimwriterfs` for ZIM file packaging. `zimwriterfs` can be found at https://github.com/openzim/zimwriterfs.

Installation
--------

It's advised, that you have `virtualenv` installed. It is usually packaged, but if you have to install it manually

    sudo pip install virtualenv

Create your virtualenv

    virtualenv --no-site-packages venv 

Activate the virtual environment

    source venv/bin/activate

Then install youtube2zim

    pip install youtube2zim
    
Usage
-----

    youtube2zim YOUTUBE_URL ZIM_LANG PUBLISHER [OPTION]...

Start `youtube2zim` without any parameter to list all available options.
