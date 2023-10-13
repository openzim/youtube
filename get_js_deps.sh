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
ASSETS_PATH="${SCRIPT_PATH}/src/youtube2zim/templates/assets"

echo "About to download JS assets to ${ASSETS_PATH}"

echo "getting video.js"
curl -L -O https://github.com/videojs/video.js/releases/download/v8.6.1/video-js-8.6.1.zip
rm -rf $ASSETS_PATH/videojs
mkdir -p $ASSETS_PATH/videojs
unzip -o -d $ASSETS_PATH/videojs video-js-8.6.1.zip
rm -rf $ASSETS_PATH/videojs/alt $ASSETS_PATH/videojs/examples
rm -f video-js-8.6.1.zip

echo "getting ogv.js"
curl -L -O https://github.com/brion/ogv.js/releases/download/1.8.9/ogvjs-1.8.9.zip
rm -rf $ASSETS_PATH/ogvjs
unzip -o ogvjs-1.8.9.zip
mv ogvjs-1.8.9 $ASSETS_PATH/ogvjs
rm -f ogvjs-1.8.9.zip

echo "getting chosen.jquery.js"
curl -L -O https://github.com/harvesthq/chosen/releases/download/v1.8.7/chosen_v1.8.7.zip
rm -rf $ASSETS_PATH/chosen
mkdir -p $ASSETS_PATH/chosen
unzip -o -d $ASSETS_PATH/chosen chosen_v1.8.7.zip
rm -rf $ASSETS_PATH/chosen/docsupport $ASSETS_PATH/chosen/chosen.proto.* $ASSETS_PATH/chosen/*.html $ASSETS_PATH/chosen/*.md
rm -f chosen_v1.8.7.zip

echo "getting videojs-ogvjs.js"
curl -L -o $ASSETS_PATH/videojs-ogvjs.js https://dev.kiwix.org/videojs-ogvjs/videojs-ogvjs.min.js

echo "getting jquery.js"
curl -L -o $ASSETS_PATH/jquery.min.js https://code.jquery.com/jquery-1.12.4.min.js

echo "getting webp-hero"
curl -L -O https://unpkg.com/webp-hero@0.0.2/dist-cjs/polyfills.js
rm -f $ASSETS_PATH/polyfills.js
mv polyfills.js $ASSETS_PATH/polyfills.js
curl -L -O https://unpkg.com/webp-hero@0.0.2/dist-cjs/webp-hero.bundle.js
rm -f $ASSETS_PATH/webp-hero.bundle.js
mv webp-hero.bundle.js $ASSETS_PATH/webp-hero.bundle.js

if command -v fix_ogvjs_dist > /dev/null; then
    echo "fixing JS files"
    fix_ogvjs_dist $ASSETS_PATH "assets"
else
    echo "NOT fixing JS files (zimscraperlib not installed)"
fi
