#!/bin/sh

###
# download JS dependencies and place them in our templates/assets folder
# then launch our ogv.js script to fix dynamic loading links
###

if ! command -v curl > /dev/null; then
	echo "you need curl."
	exit 1
fi

if ! command -v unzip > /dev/null; then
	echo "you need unzip."
	exit 1
fi

# Absolute path this script is in.
SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
ASSETS_PATH="${SCRIPT_PATH}/youtube2zim/templates/assets"

echo "About to download JS assets to ${ASSETS_PATH}"

echo "getting video.js"
curl -L -O https://github.com/videojs/video.js/releases/download/v7.6.4/video-js-7.6.4.zip
rm -rf $ASSETS_PATH/videojs
mkdir -p $ASSETS_PATH/videojs
unzip -o -d $ASSETS_PATH/videojs video-js-7.6.4.zip
rm -rf $ASSETS_PATH/videojs/alt $ASSETS_PATH/videojs/examples
rm -f video-js-7.6.4.zip

echo "getting ogv.js"
curl -L -O https://github.com/brion/ogv.js/releases/download/1.6.1/ogvjs-1.6.1.zip
rm -rf $ASSETS_PATH/ogvjs
unzip -o ogvjs-1.6.1.zip
mv ogvjs-1.6.1 $ASSETS_PATH/ogvjs
rm -f ogvjs-1.6.1.zip

echo "getting chosen.jquery.js"
curl -L -O https://github.com/harvesthq/chosen/releases/download/v1.8.7/chosen_v1.8.7.zip
rm -rf $ASSETS_PATH/chosen
mkdir -p $ASSETS_PATH/chosen
unzip -o -d $ASSETS_PATH/chosen chosen_v1.8.7.zip
rm -rf $ASSETS_PATH/chosen/docsupport $ASSETS_PATH/chosen/chosen.proto.* $ASSETS_PATH/chosen/*.html $ASSETS_PATH/chosen/*.md
rm -f chosen_v1.8.7.zip

echo "getting videojs-ogvjs.js"
curl -L -O https://github.com/hartman/videojs-ogvjs/archive/v1.3.1.zip
rm -f $ASSETS_PATH/videojs-ogvjs.js
unzip -o v1.3.1.zip
mv videojs-ogvjs-1.3.1/dist/videojs-ogvjs.js $ASSETS_PATH/videojs-ogvjs.js
rm -rf videojs-ogvjs-1.3.1
rm -f v1.3.1.zip

echo "getting jquery.js"
curl -L -o $ASSETS_PATH/jquery.min.js https://code.jquery.com/jquery-1.12.4.min.js

echo "fixing JS files"
python3 $SCRIPT_PATH/youtube2zim/fix_ogvjs_dist.py
