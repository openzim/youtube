#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""youtube to zim.
Create a ZIM snapshot by scraping your prefered Youtube channel or playlist
Url format for playlist : https://www.youtube.com/playlist?list=PL1rRii_tzDcK47PQTWUX5yzoL8xz7Kgna
Url format for user : https://www.youtube.com/channel/UC2gwowvVGh7NMYtHHeyzMmw 

Usage:
  youtube2zim <url> <lang> <publisher> [--lowquality] [--zimpath=<zimpath>] [--nozim] [--transcode2webm]

Options:
    -h --help  
    --lowquality  download in mp4 and re-encode aggressively in webm
    --zimpath=<zimpath>   Final path of the zim file
    --nozim  doesn't make zim file, output will be in build/[donwloaded name]/ in html (otherwise will produice a zim file)
    --transcode2webm    Download or transcode videos to webm
"""

import sys
import os
import youtube_dl
import urllib
import requests
import subprocess
import datetime
from sys import platform as _platform
from jinja2 import Environment, FileSystemLoader
import json
import shutil
import envoy
import bs4 as BeautifulSoup
import cssutils
import slugify
import time
import codecs
from dominantColor import *
import re
from docopt import docopt
from functools import partial

def get_list_item_info(url):
    """
    Create dictionnary with all info about video playlist or user video
    structure is {dict [list of dict {dict for each video} ] }
    Only return list of video and write title of playlist/user name
    """
    with youtube_dl.YoutubeDL({'writesubtitles': True, 'ignoreerrors': True}) as ydl:
        attempts = 0
        while attempts < 5:
            try:
                result = ydl.extract_info(url, download=False)
                break
            except:
                e = sys.exc_info()[0]
                attempts += 1
                print "error : " + str(e)
                if attempts == 5:
                    sys.exit("Error during getting list of video")
                print "We will re-try to get this video"
                time_to_wait = 60 * attempts
                time.sleep(time_to_wait)

    return result

def prepare_folder(list, url):
    type = list['extractor_key']
    if "www.youtube.com/user/" in url:
        type = "user"

    if type == "YoutubePlaylist":
        if "channel" in url:
            title =  slugify.slugify(list.get('entries')[0].get('uploader'))
            title_html = list.get('entries')[0].get('uploader')
        else:
            title = slugify.slugify(list['title'])
            title_html = list['title']
    else:
        title =  slugify.slugify(list.get('entries')[0].get('uploader'))
        title_html = list.get('entries')[0].get('uploader')
    

    scraper_dir = os.path.join( "build/", title) + "/"

    if not os.path.exists(scraper_dir):
        os.makedirs(scraper_dir)
    if not os.path.exists(scraper_dir+"CSS/"):
        shutil.copytree(os.path.join(os.path.abspath(os.path.dirname(__file__)),"templates/CSS/"), scraper_dir+"CSS/")
    if not os.path.exists(scraper_dir+"JS/"):
        shutil.copytree(os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates/JS/"), scraper_dir+"JS/")
    get_user_pictures(list.get('entries')[0].get('uploader_id'),scraper_dir,type)

    color = colorz(scraper_dir+"CSS/img/header.png", 1)[0]

    background_color = solarize_color(color);
    return [ type, title , title_html, scraper_dir, color, background_color ]

def make_welcome_page(list, playlist,scraper_dir,title_html,color,background_color,format):
    if len(playlist) == 0:
        options = "<form name=\"playlist\" id=\"header-playlists\" style=\"display:none\">\n                        <select name=\"list\" onChange=\"genplaylist()\">"
    else:
        options = "<form name=\"playlist\" id=\"header-playlists\">\n            <select name=\"list\" onChange=\"genplaylist()\">"

    options += "<option value=\"All\">--</option>"
    for j in sorted(playlist):
        options += "<option value=\"" + j  + "\">" + j.replace('_', ' ') + "</option>"
    options += "\n </select>\n                                              </form>"
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.abspath(os.path.dirname(__file__)),'templates')))
    template = env.get_template('welcome.html')
    html = template.render(title=title_html, color=color, background_color=background_color, options=options)
    html = html.encode('utf-8')
    index_path = os.path.join(scraper_dir, 'index.html')
    with open(index_path, 'w') as html_page:
        html_page.write(html)
    template = env.get_template(os.path.join("JS","app.js"))
    js_app = template.render(format=format)
    js_app = js_app.encode('utf-8')
    jsapp_path = os.path.join(scraper_dir, "JS", "app.js")
    with open(jsapp_path, 'w') as jsapp_file:
        jsapp_file.write(js_app)

def welcome_page(title, author, id, description,videos):
    videos.append({
        'id': id,
        'title': title.encode('utf-8', 'ignore'),
        'description': description.encode('utf-8', 'ignore'),
        'speaker': author.encode('utf-8', 'ignore'),
        'thumbnail': id+"/thumbnail.jpg".encode('utf-8', 'ignore')})
    return videos

def hook_youtube_dl_ffmpeg(format,data):
    if data["status"] == "finished":
        tmp_path=os.path.join(os.path.dirname(data["filename"]), "tmp."+format)
        final_path=os.path.join(os.path.dirname(data["filename"]) , "video."+format)
	codec_video={"mp4" : "h264", "webm" : "libvpx"}
	codec_audio={"mp4" : "mp3", "webm": "libvorbis"}
        cmd="ffmpeg -y -i file:" + data["filename"] + " -codec:v " + codec_video[format] + " -quality best -cpu-used 0 -b:v 300k -qmin 30 -qmax 42 -maxrate 300k -bufsize 1000k -threads 8 -vf scale=480:-1 -codec:a " + codec_audio[format] + " -b:a 128k file:" + tmp_path
        print "convert from " + data["filename"] + " to " + final_path
	print cmd
        if exec_cmd(cmd) == 0:
            os.remove(data["filename"])
            os.rename(tmp_path,final_path)
        else:
            print "Convertion error"
            raise Exception('Convertion error')

def hook_youtube_dl_avconv(format,data):
    if data["status"] == "finished":
        tmp_path=os.path.join(os.path.dirname(data["filename"]), "tmp."+format)
        final_path=os.path.join(os.path.dirname(data["filename"]) , "video."+format)
	codec_video={"mp4" : "h264", "webm" : "libvpx"}
	codec_audio={"mp4" : "mp3", "webm": "libvorbis"}
        cmd="avconv -y -i file:" + data["filename"] + " -codec:v " + codec_video[format] + " -qscale 1 -cpu-used 0 -b:v 300k -qmin 30 -qmax 42 -maxrate 300k -bufsize 1000k -threads 8 -vf scale=480:-1 -codec:a " + codec_audio[format] + " -b:a 128k file:" +  tmp_path
        print "convert from " + data["filename"] + " to " + final_path
	print cmd
        if exec_cmd(cmd) == 0:
            os.remove(data["filename"])
            os.rename(tmp_path,final_path)
        else:
            print "Convertion error"
            raise Exception('Convertion error')

def write_video_info(list, parametre,scraper_dir,background_color, videos,format):
    """
    Render static html pages from the scraped video data and
    save the pages in build/{video id}/index.html.
    Save video in best quality in build/{title of user/playlist}/{video id}/video.mp4
    """
    print 'Rendering template...'
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.abspath(os.path.dirname(__file__)),'templates')))
    template = env.get_template('video.html')
    for item in list:
        if item != None :
            title_clean = slugify.slugify(item.get('title'))
            video_directory = scraper_dir+title_clean+"/"
            html_file = os.path.join(video_directory, 'index.html')
            if not os.path.exists(video_directory):
                url = "https://www.youtube.com/watch?v="+item.get('id')
                parametre['outtmpl'] = scraper_dir+title_clean+'/video.%(ext)s'
                with youtube_dl.YoutubeDL(parametre)  as ydl:
                    attempts = 0
                    while attempts < 5:
                        try:
                            ydl.download([url])
                            break
                        except:
                            e = sys.exc_info()[0]
                            attempts += 1
                            print "error : " + str(e)
                            if attempts == 5:
                                sys.exit("Error during getting video")
                            print "We will re-try to get this video " + url + " in 10s"
                            time_to_wait = 60 * attempts
                            time.sleep(time_to_wait)
                    date = item.get('upload_date')
                    id = item.get('id')
                    publication_date = date[6:8]+"/"+date[4:6]+"/"+date[0:4]
                    subtitles = download_video_thumbnail_subtitles(id, item.get('subtitles'), title_clean,scraper_dir)
                    description=re.sub("\n","<br>", item.get('description'))
                    html = template.render(
                            title=item.get('title'),
                            author=item.get('uploader'),
                            vtt = subtitles,
                            description=description,
                            url=item.get('webpage_url'),
                            date=publication_date,
                            background_color=background_color,
                            format=format)
                    html = html.encode('utf-8')
                    index_path = os.path.join(video_directory, 'index.html')
                    with open(index_path, 'w') as html_page:
                        html_page.write(html)
                    videos=welcome_page(item.get('title'), item.get('uploader'), title_clean, item.get('description'), videos)
            elif not os.path.exists(html_file):
                date = item.get('upload_date')
                id = item.get('id')
                publication_date = date[6:8]+"/"+date[4:6]+"/"+date[0:4]
                subtitles = download_video_thumbnail_subtitles(id, item.get('subtitles'), title_clean,scraper_dir)

                html = template.render(
                        title=item.get('title'),
                        author=item.get('uploader'),
                        vtt = subtitles,
                        description=item.get('description'),
                        url=item.get('webpage_url'),
                        date=publication_date,
                        background_color=background_color
                        )

                html = html.encode('utf-8')
                index_path = os.path.join(video_directory, 'index.html')
                with open(index_path, 'w') as html_page:
                    html_page.write(html)
                videos=welcome_page(item.get('title'), item.get('uploader'), title_clean, item.get('description'),videos)

            else:
                print "Video directory " + video_directory + " already exists. Skipping."
                videos=welcome_page(item.get('title'), item.get('uploader'), title_clean, item.get('description'),videos)
        else:
            print "We can't get this video"
    return videos

def dump_data(videos, title,scraper_dir):
    """
    Dump all the data about every youtube video in a JS/data.js file
    inside the 'build' folder.
    """
    # Prettified json dump
    data = 'var json_' + title + ' = ' + json.dumps(videos, indent=4, separators=(',', ': ')) + ";"
    # Check, if the folder exists. Create it, if it doesn't.
    if not os.path.exists(scraper_dir):
        os.makedirs(scraper_dir)
    # Create or override the 'TED.json' file in the build
    # directory with the video data gathered from the scraper.
    with open(scraper_dir + 'JS/data.js', 'a') as youtube_file:
        youtube_file.write(data + ' \n')

def download_video_thumbnail_subtitles(id, subtitles, title,scraper_dir):
    """ Download thumbnail and subtitles of each video in his folder """
    #download thumbnail
    thumbnail_url = "https://i.ytimg.com/vi/"+id+"/hqdefault.jpg"
    thumbnail_file = scraper_dir+title+"/thumbnail.jpg"
    download(thumbnail_url , thumbnail_file)



    resize_image(thumbnail_file)
    #download substitle and add it to video.html if they exist
    if subtitles != "none" or subtitles != {}:
        subs_list = []
        for key in subtitles:
            for element in subtitles.get(key):
                if element.get('ext') == "vtt":
                    url =  element.get('url')
                    key_name = language_codeToLanguage_Name(key)
                    dict_lang = {'code': key, 'name': key_name}
                    subs_list.append(dict_lang)
                    webvtt_file = scraper_dir+title+"/"+key+".vtt"
                    download(url , webvtt_file)
                    with open(webvtt_file, "r") as vttfile:
                        vtt_str = ''.join(vttfile.readlines()[3:])
                        vttfile.close()
                    with open(webvtt_file, "w") as vttfile:
                        vtt_str = "WEBVTT\n" + vtt_str
                        vttfile.write(vtt_str)



    return subs_list


def get_user_pictures(api_key,scraper_dir,type):
    """
    Get profile picture of a user or the profile picture of the uploader of the first video if it's a playlist
    Get user header if it's a user
    """
    url_channel = "https://www.youtube.com/user/"+api_key
    if type == "user" or type == "YoutubeChannel" or type == "YoutubePlaylist":
        url_channel = sys.argv[1]
    attempts = 0
    while attempts < 5:
        try:
            api = urllib.urlopen(url_channel).read()
            break
        except:
            e = sys.exc_info()[0]
            attempts += 1
            print "error : " + str(e)
            if attempts == 5:
                sys.exit("Error during getting api data")
            print "We will re-try to get this in 10s"
            time_to_wait = 60 * attempts
            time.sleep(time_to_wait)


    soup_api = BeautifulSoup.BeautifulSoup(api, "html.parser")
#       url_profile_picture = soup_api.find('img',attrs={"class":u"appbar-nav-avatar"})['src']
    url_profile_picture = soup_api.find('img',attrs={"class":u"channel-header-profile-image"})['src']
    if "https:" not in url_profile_picture :
        url_profile_picture = "https:" + url_profile_picture

    download(url_profile_picture , scraper_dir+"CSS/img/header_profile.png")


    shutil.copy(scraper_dir+"CSS/img/header_profile.png", scraper_dir+"favicon.png")
    resize_image_profile(scraper_dir+"favicon.png")

    #get user header
    attempts = 0
    while attempts < 5:
        try:
            html = urllib.urlopen(url_channel).read()
            break
        except:
            e = sys.exc_info()[0]
            attempts += 1
            print "error : " + str(e)
            if attempts == 5:
                sys.exit("Error during getting html data of user")
            print "We will re-try to get this in 10s"
            time_to_wait = 60 * attempts
            time.sleep(time_to_wait)


    soup = BeautifulSoup.BeautifulSoup(html, "html.parser")
    header = soup.find('div',attrs={"id":u"gh-banner"}).find('style').text
    sheet = cssutils.parseString(header)
    for rule in sheet:
        if rule.type == rule.STYLE_RULE:
            for property in rule.style:
                if property.name == 'background-image':
                    urls = property.value
    if "playlist?list=" in url_channel:
        url_user_header = "https://youtube.com" + urls[4:-1]
    else:
        if urls[4] == '"':
            url_user_header = "https:"+urls[5:-2]
        else:
            url_user_header = "https://youtube.com"+urls[4:-1]
    download(url_user_header , scraper_dir+"CSS/img/header.png")

def resize_image(image_path):
    from PIL import Image
    image = Image.open(image_path)
    w, h = image.size
    image = image.resize((248, 187), Image.ANTIALIAS)
    image.save(image_path)

def resize_image_profile(image_path):
    from PIL import Image
    image = Image.open(image_path)
    w, h = image.size
    image = image.resize((48, 48), Image.ANTIALIAS)
    image.save(image_path)

def exec_cmd(cmd):
    return envoy.run(str(cmd.encode('utf-8'))).status_code

def sort_by_view_count(k):
    if k != None and k.has_key('view_count'):
        return k['view_count']
    else:
        return 0

def sort_list_by_view(list):
    """ The most seen video is first, the rest does not change """
    list_sorted= sorted(list, key=sort_by_view_count,reverse=True)
    list.remove(list_sorted[0])
    new_list= [ list_sorted[0] ] + list
    return new_list

def sort_list_by_welcome(list,url):
    """ Welcome video first, the rest does not change """
    attempts = 0
    while attempts < 5:
        try:
            api = urllib.urlopen(url).read()
            break
        except:
            e = sys.exc_info()[0]
            attempts += 1
            print "error : " + str(e)
            if attempts == 5:
                sys.exit("Error during getting lsit of playlist")
            print "We will re-try to get this in 10s"
            time_to_wait = 60 * attempts
            time.sleep(time_to_wait)

    soup_api = BeautifulSoup.BeautifulSoup(api, "html.parser")
    try:
        welcome_id=soup_api.find('div', attrs={"class":u"c4-flexible-player-box", "id":u"upsell-video"}).get('data-video-id')
        welcome_obj=(item for item in list if item["id"] == welcome_id).next()
        list.remove(welcome_obj)
        return [welcome_obj] + list
    except: #if we doesn't find welcome video
        return sort_list_by_view(list)

def create_zims(list_title, lang_input, publisher,scraper_dir,zim_path):
    print 'Creating ZIM files'
    # Check, if the folder exists. Create it, if it doesn't.
    html_dir = os.path.join(scraper_dir)
    lang_input_alpha2 = languageIso3ToIso2(lang_input)
    if zim_path == None:
        zim_path = os.path.join("build/", "{title}_{lang}_all_{date}.zim".format(title=list_title.lower(),lang=lang_input_alpha2,date=datetime.datetime.now().strftime('%Y-%m')))
    title = list_title.replace("-", " ")
    description = "{title} videos".format(title=title)
    return create_zim(html_dir, zim_path, title, description, list_title, lang_input, publisher)

def create_zim(static_folder, zim_path, title, description, list_title, lang_input, publisher):

    print "\tWritting ZIM for {}".format(title)

    context = {
        'languages': lang_input,
        'title': title,
        'description': description,
        'creator': list_title.replace("-", " "),
        'publisher': publisher,
        'home': 'index.html',
        'favicon': 'favicon.png',
        'static': static_folder,
        'tags' : "youtube",
        'name' : "kiwix."+title.encode("utf-8"),
        'zim': zim_path
    }

    cmd = ('zimwriterfs --welcome="{home}" --favicon="{favicon}" '
           '--language="{languages}" --title="{title}" '
           '--description="{description}" '
           '--creator="{creator}" --tags="{tags}" --name="{name}" --publisher="{publisher}" "{static}" "{zim}"'
           .format(**context))
    print cmd

    if exec_cmd(cmd) == 0:
        print "Successfuly created ZIM file at {}".format(zim_path)
        return True
    else:
        print "Unable to create ZIM file :("
        return False

def bin_is_present(binary):
    try:
        subprocess.Popen(binary,
                         universal_newlines=True,
                         shell=False,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         bufsize=0)
    except OSError:
        return False
    else:
        return True

def languageIso3ToIso2(iso3):
    f = codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ISO-639-2_utf-8.txt'), 'rb', 'utf-8')
    for line in f:
        iD = {}
        iD['bibliographic'], iD['terminologic'], iD['alpha2'], \
            iD['english'], iD['french'] = line.strip().split('|')

        if iD['terminologic'] == iso3 or iD['bibliographic'] == iso3:
            f.close();
            return iD['alpha2'];

    f.close()
    return ""

def language_codeToLanguage_Name(lang):
    f = codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ISO-639-2_utf-8.txt'), 'rb', 'utf-8')
    for line in f:
        iD = {}
        iD['bibliographic'], iD['terminologic'], iD['alpha2'], \
            iD['english'], iD['french'] = line.strip().split('|')

        if iD['terminologic'] == lang or iD['bibliographic'] == lang or iD['alpha2'] == lang:
            f.close();
            return iD['english'];

    f.close()
    return ""
def download(url, destination):
    attempts = 0
    while attempts < 5:
        try:
            urllib.urlretrieve(url, destination )
            break
        except:
            e = sys.exc_info()[0]
            attempts += 1
            print "error : " + str(e)
            if attempts == 5:
                sys.exit("Error during getting user header")
            print "We will re-try to get this resources in 10s"
            time_to_wait = 60 * attempts
            time.sleep(time_to_wait)

def get_playlist(url):
    playlist = []
    url_channel = url + "/playlists"
    attempts = 0
    while attempts < 5:
        try:
            api = urllib.urlopen(url_channel).read()
            break
        except:
            e = sys.exc_info()[0]
            attempts += 1
            print "error : " + str(e)
            if attempts == 5:
                sys.exit("Error during getting lsit of playlist")
            print "We will re-try to get this in 10s"
            time_to_wait = 60 * attempts
            time.sleep(time_to_wait)

    soup_api = BeautifulSoup.BeautifulSoup(api, "html.parser")
    for link in  soup_api.find_all('a', attrs={"class":u"yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2"}):
        new = "https://youtube.com" + link.get('href')
        if new not in playlist:
            playlist.append(new)
    return playlist

def run():
    arguments = docopt(__doc__, version='youtube2zim 1.2.5')
    if not arguments['--nozim'] and not bin_is_present("zimwriterfs"):
        sys.exit("zimwriterfs is not available, please install it.")

    if arguments["--transcode2webm"]:
        preferredcodec = "webm"
        format = "webm"
    else:
        preferredcodec = "mp4"
        format = "mp4"
    if arguments["--lowquality"]:
        if bin_is_present("avconv"):
            print "avconv"
            parametre = { 'prefer_ffmpeg' : False, 'preferredcodec': preferredcodec, 'format' : format, 'progress_hooks': [partial(hook_youtube_dl_avconv,format)] }
        elif bin_is_present("ffmpeg"):
            print "ffmpeg"
            parametre = { 'prefer_ffmpeg' : True, 'preferredcodec': preferredcodec, 'format' : format, 'progress_hooks': [partial(hook_youtube_dl_ffmpeg,format)] }
        else:
            sys.exit("avconv and ffmpeg are not available, please install one.")
    else:
        parametre = {'preferredcodec': preferredcodec,  'format' : format}

    if arguments["<url>"][24:28] == "user" or arguments["<url>"][23:27] == "user" :
        get_page = urllib.urlopen(arguments["<url>"]).read()
        soup_page = BeautifulSoup.BeautifulSoup(get_page, "html.parser")
        url_channel = soup_page.find('meta',attrs={"itemprop":u"channelId"})['content']
        url = str("https://www.youtube.com/channel/"+url_channel)

    else:
        url = arguments["<url>"]

    script_dirname=(os.path.dirname(sys.argv[0]) or ".") + "/"
    lang_input=arguments["<lang>"]
    publisher=arguments["<publisher>"]
    list=get_list_item_info(arguments["<url>"])
    if list != None :
        videos = []
        type, title , title_html, scraper_dir, color, background_color = prepare_folder(list,url)
        if not ".com/playlist?list=" in sys.argv[1]:
            sorted_list = sort_list_by_welcome(list.get('entries'),sys.argv[1])
        else:
            sorted_list = sort_list_by_view(list.get('entries'))
        videos=write_video_info(sorted_list,parametre,scraper_dir,background_color,videos,format)
        dump_data(videos, "All",scraper_dir)
        playlist=get_playlist(sys.argv[1])
        list_of_playlist = []
        for x in playlist:
            list=get_list_item_info(x)
            if list != None :
                videos = []
                sorted_list = sort_list_by_view(list.get('entries'))
                vidoes=write_video_info(sorted_list, parametre,scraper_dir,background_color,videos,format)
                title = slugify.slugify(list.get('title'))
                title = re.sub(r'-', '_', title)
                dump_data(videos, title,scraper_dir)
                list_of_playlist.append(title)

        make_welcome_page(list, list_of_playlist,scraper_dir,title_html,color,background_color,format)

        title_zim  = slugify.slugify(title_html)
        if not arguments['--nozim']:
            done=create_zims(title_zim, lang_input,publisher,scraper_dir,arguments["--zimpath"])
            if done == True:
                shutil.rmtree(scraper_dir)


if __name__ == '__main__':
    run()
