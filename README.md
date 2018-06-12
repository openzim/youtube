This script made a .zim file of video from youtube user or youtube playlist.

== Usage ==

    youtube2zim [your user url or playlist url] [lang of your zim archive] [publisher]


    You can use --lowquality option that will download the video in mp4 and re-encode aggressively in webm
== Building ==

It's advised, that you have `virtualenv` installed:

    sudo pip install virtualenv

Up next you have to create a virtual enviroment in the kiwix-other/TED/ directory for the TED Scraper:

    virtualenv --no-site-packages venv 

Activate the virtual enviroment:

    source venv/bin/activate

Then install youtube2zim

    pip install youtube2zim

You will aslo need ffmpeg or avconv to convert mp4 format to webm format

You also need zimwriterfs binary in this folder, zimwriterfs can be found at https://sourceforge.net/p/kiwix/other/ci/master/tree/zimwriterfs/

