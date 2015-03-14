This script made a .zim file of video from youtube user or youtube playlist.

== Usage ==
python youtube2zim.py [your user url or playlist url] [lang of your zim archive] [publisher]

== Building ==

It's advised, that you have `pip` installed. 
Chose one of the following methods to do that:

    sudo apt-get install python-setuptools

    sudo easy_install pip

It's advised, that you have `virtualenv` installed:

    sudo pip install virtualenv

Up next you have to create a virtual enviroment in the kiwix-other/TED/ directory for the TED Scraper:

    virtualenv --no-site-packages venv 

Activiate the virtual enviroment:

    source venv/bin/activate

Requirements are in requirements.txt you just need to make :

    pip install -r requirements.txt

You will aslo need ffmpeg to convert mp4 format to webm format (maybe ffmpeg is remplace by avconv in your distribution so you have to modify script)

You also need zimwriterfs binary in this folder, zimwriterfs can be found at https://sourceforge.net/p/kiwix/other/ci/master/tree/zimwriterfs/

