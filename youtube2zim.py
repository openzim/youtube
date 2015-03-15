#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import pycountry

type = ""
videos = []
def get_list_item_info(url):
	"""
	Create dictionnary with all info about video playlist or user video
	structure is {dict [list of dict {dict for each video} ] }
	Only return list of video and write title of playlist/user name
	"""
        with youtube_dl.YoutubeDL({'writesubtitles': True}) as ydl:
				attempts = 0
                                while attempts < 5:
                                        try:
						result = ydl.extract_info(url, download=False)
                                                break
                                        except:
                                                e = sys.exc_info()[0]
                                                attempts += 1
                                                print "error : " + e
                                                if attempts == 5:
                                                        sys.exit("Error during getting list of video")
                                                print "We will re-try to get this video in 10s"
                                                time.sleep(10)

        type = result['extractor_key']
	global title
        if type == "YoutubePlaylist":
                title = slugify.slugify(result['title'])
        else:
                title =  slugify.slugify(result.get('entries')[0].get('uploader'))

	global scraper_dir
        scraper_dir = "build/"+title+"/"
        if not os.path.exists(scraper_dir):
                os.makedirs(scraper_dir)
        if not os.path.exists(scraper_dir+"CSS/"):
                shutil.copytree("templates/CSS/", scraper_dir+"CSS/")
        if not os.path.exists(scraper_dir+"JS/"):
                shutil.copytree("templates/JS/", scraper_dir+"JS/")
        if not os.path.exists(scraper_dir+"favicon.png"):
                shutil.copy("templates/favicon.png", scraper_dir+"favicon.png")
        if not os.path.exists(scraper_dir+"index.html"):
                shutil.copy("templates/welcome.html", scraper_dir+"index.html")

	if type != "YoutubePlaylist":
		get_user_pictures(url,result.get('entries')[0].get('uploader_id'),1)
	else:
		get_user_pictures(url,result.get('entries')[0].get('uploader_id'),0)
	return result.get('entries')

def welcome_page(title, author, id, description):
        videos.append({
            'id': id,
            'title': title.encode('ascii', 'ignore'),
            'description': description.encode('ascii', 'ignore'),
            'speaker': author.encode('ascii', 'ignore'),
            'thumbnail': id+"/thumbnail.jpg".encode('ascii', 'ignore')})

def write_video_info(list):
        """
        Render static html pages from the scraped video data and
        save the pages in build/{video id}/index.html.
	Save video in best quality in build/{title of user/playlist}/{video id}/video.mp4
        """
	print 'Rendering template...'
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('video.html')
        for item in list:
		title_clean = slugify.slugify(item.get('title'))
		video_directory = scraper_dir+title_clean+"/"
                if not os.path.exists(video_directory):
                        url = "https://www.youtube.com/watch?v="+item.get('id')
                        with youtube_dl.YoutubeDL({'outtmpl': scraper_dir+title_clean+'/video.mp4'})  as ydl:
				attempts = 0
				while attempts < 5:
	                                try:
						ydl.download([url])
						break
					except:
						e = sys.exc_info()[0]
						attempts += 1						
						print "error : " + e
						if attempts == 5:
							sys.exit("Error during getting video")
						print "We will re-try to get this video in 10s"
						time.sleep(10)
                        date = item.get('upload_date')
                        id = item.get('id')
                        publication_date = date[6:8]+"/"+date[4:6]+"/"+date[0:4]
                        subtitles = download_video_thumbnail_subtitles(id, item.get('subtitles'), title_clean)

                        html = template.render(
                                title=item.get('title'),
                                author=item.get('uploader'),
                                vtt = subtitles,
                                description=item.get('description'),
                                url=item.get('webpage_url'),
                                date=publication_date)

                        html = html.encode('utf-8')
                        index_path = os.path.join(video_directory, 'index.html')
                        with open(index_path, 'w') as html_page:
                            html_page.write(html)
                        welcome_page(item.get('title'), item.get('uploader'), title_clean, item.get('description'))
                else:
                        print "Video directory " + video_directory + "already exists. Skipping."
			welcome_page(item.get('title'), item.get('uploader'), title_clean, item.get('description'))

def dump_data(videos):
        """
        Dump all the data about every youtube video in a JS/data.js file
        inside the 'build' folder.
        """
        # Prettified json dump
        data = 'json_data = ' + json.dumps(videos, indent=4, separators=(',', ': '))
        # Check, if the folder exists. Create it, if it doesn't.
        if not os.path.exists(scraper_dir):
            os.makedirs(scraper_dir)
        # Create or override the 'TED.json' file in the build
        # directory with the video data gathered from the scraper.
        with open(scraper_dir + 'JS/data.js', 'w') as youtube_file:
            youtube_file.write(data)

def download_video_thumbnail_subtitles(id, subtitles, title):
	""" Download thumbnail and subtitles of each video in his folder """
	#download thumbnail
	thumbnail_url = "https://i.ytimg.com/vi/"+id+"/hqdefault.jpg"
	thumbnail_file = scraper_dir+title+"/thumbnail.jpg" 
	attempts = 0
	while attempts < 5:
		try:
			urllib.urlretrieve (thumbnail_url , thumbnail_file)
			break
		except:
			e = sys.exc_info()[0]
			attempts += 1
			print "error : " + e
			if attempts == 5:
				sys.exit("Error during getting list of video")
                        print "We will re-try to get this video in 10s"
                        time.sleep(10)

	resize_image(thumbnail_file)
	#download substitle and add it to video.html if they exist
	if subtitles != "none" or subtitles != {}:
                subs_list = []
                print subtitles
                for key in subtitles:
                        for element in subtitles.get(key):
                                if element.get('ext') == "vtt":
                                        url =  element.get('url')        
                                        subs_list.append(key)
                                        webvtt_file = scraper_dir+title+"/"+key+".vtt"
                                        while attempts < 5:
                                                try:
                                                        urllib.urlretrieve (url , webvtt_file)
                                                        break
                                                except:
                                                        e = sys.exc_info()[0]
                                                        attempts += 1
                                                        print "error : " + e
			                                if attempts == 5:  
                                                                sys.exit("Error during getting subtitleof video")  
                                                        print "We will re-try to get this video in 10s"
                                                        time.sleep(10)
        return subs_list


def get_user_pictures(url,api_key, is_user):
	""" 
	Get profile picture of a user or the profile picture of the uploader of the first video if it's a playlist
	Get user header if it's a user
	"""
	url_api = "https://gdata.youtube.com/feeds/api/users/"+api_key+"?v=2.1"
        attempts = 0
        while attempts < 5:
                try:
                        api = urllib.urlopen(url_api).read()
                        break
                except:
                        e = sys.exc_info()[0]
                        attempts += 1
                        print "error : " + e
                        if attempts == 5:
                                sys.exit("Error during getting api data")
                        print "We will re-try to get this in 10s"
                        time.sleep(10)

	soup_api = BeautifulSoup.BeautifulSoup(api)
	url_profile_picture = soup_api.find('media:thumbnail')['url']
        attempts = 0
        while attempts < 5:
                try:
                        urllib.urlretrieve (url_profile_picture , scraper_dir+"CSS/img/YOUTUBE_small.png")
                        break
                except:
                        e = sys.exc_info()[0]
                        attempts += 1
                        print "error : " +e
                        if attempts == 5:
                                sys.exit("Error during getting user pic profile")
                        print "We will re-try to get this video in 10s"
                        time.sleep(10)
	shutil.copy(scraper_dir+"CSS/img/YOUTUBE_small.png", scraper_dir+"favicon.png")
	resize_image_profile(scraper_dir+"favicon.png")

	#get user header
	if is_user == 1:
		attempts = 0
		while attempts < 5:
			try:
				html = urllib.urlopen(url).read()
				break
			except:
				e = sys.exc_info()[0]
				attempts += 1
				print "error : " + e
				if attempts == 5:
					sys.exit("Error during getting html data of user")
				print "We will re-try to get this in 10s"
	                        time.sleep(10)
	
		soup = BeautifulSoup.BeautifulSoup(html)
		header = soup.find('div',attrs={"id":u"gh-banner"}).find('style').text
		sheet = cssutils.parseString(header)
		for rule in sheet:
		    if rule.type == rule.STYLE_RULE:
		        for property in rule.style:
		            if property.name == 'background-image':
		                urls = property.value
	        if urls[4] == '"':
	                url_user_header = "https:"+urls[5:-1]
	        else:
	                url_user_header = "https:"+urls[4:-1]
		print url_user_header
	        attempts = 0
	        while attempts < 5:
			try:
				urllib.urlretrieve (url_user_header , scraper_dir+"CSS/img/YOUTUBE_header.png")
        	                break
        	        except:
        	                e = sys.exc_info()[0]
	                        attempts += 1
	                        print "error : " + e
	                        if attempts == 5:
	                                sys.exit("Error during getting user header")
	                        print "We will re-try to get this user header in 10s"
	                        time.sleep(10)
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
    return envoy.run(str(cmd.encode('utf-8')))

def encode_videos(list,scraper_dir):
         """
         Encode the videos from mp4 to webm. We will use ffmpeg over the 
         command line for this. There is a static binary version
         in the kiwix-other/youtube/ directory, that we will use on macs. 
         """
         for item in list:
                 video_id = slugify.slugify(item.get('title'))
                 video_path = os.path.join(scraper_dir, video_id, 'video.mp4')
                 video_copy_path = os.path.join(scraper_dir, video_id, 'video.webm')

                 if os.path.exists(video_copy_path):
                     print 'Video ' + video_copy_path + ' already encoded. Skipping.'
                     continue

                 if os.path.exists(video_path):
                      print 'Converting Video... ' + slugify.slugify(item.get('title'))
                      convert_video_and_move_to_rendering(video_path, video_copy_path)
		      os.remove(video_path)


def convert_video_and_move_to_rendering(from_path, to_path):
        ffmpeg = ''
        if _platform == "linux" or _platform == "linux2":
           ffmpeg = 'ffmpeg'
	#   ffmpeg = 'avconv' # You need to modify command with good avconv argument
        elif _platform == "darwin":
           ffmpeg = path.join(os.getcwd(), '..', 'ffmpeg')

        command = ''.join(("""{} -i "{}" -codec:v libvpx -quality best -cpu-used 0 -b:v 300k""",
            """ -qmin 30 -qmax 42 -maxrate 300k -bufsize 1000k -threads 8 -vf scale=480:-1""",
            """ -codec:a libvorbis -b:a 128k -f webm "{}" """)).format(ffmpeg, from_path, to_path)

        os.system(command)


def create_zims(list_title):
        print 'Creating ZIM files'
        # Check, if the folder exists. Create it, if it doesn't.
        html_dir = os.path.join(scraper_dir)
	lang_alpha2 = pycountry.countries.get(alpha3=lang_input).alpha2
	zim_path = os.path.join("build/", "{title}_{lang}_all_{date}.zim".format(title=list_title.lower(),lang=lang_alpha2,date=datetime.datetime.now().strftime('%Y-%m')))
	title = list_title.replace("-", " ")
	description = "{title} videos".format(title=title)
        create_zim(html_dir, zim_path, title, description, list_title)

def create_zim(static_folder, zim_path, title, description, list_title):

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
        'zim': zim_path
    }

    cmd = ('zimwriterfs --welcome="{home}" --favicon="{favicon}" '
           '--language="{languages}" --title="{title}" '
           '--description="{description}" '
           '--creator="{creator}" --publisher="{publisher}" "{static}" "{zim}"'
           .format(**context))
    print cmd

    if exec_cmd(cmd):
        print "Successfuly created ZIM file at {}".format(zim_path)
    else:
        print "Unable to create ZIM file :("

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

def usage():
    print "\nYoutube to zim script\n"
    print 'Usage: python youtube2zim.py [your user url or playlist url] [lang of your zim archive] [publisher]]\n'
    print 'Exemple : \npython youtube2zim.py https://www.youtube.com/channel/UC2gwowvVGh7NMYtHHeyzMmw ara  kiwix => for an user channel \npython youtube2zim.py https://www.youtube.com/playlist?list=PL1rRii_tzDcK47PQTWUX5yzoL8xz7Kgna en kiwix=> for an playlist '

if len(sys.argv) != 4 :
	usage()
	exit()

if not bin_is_present("zimwriterfs"):
        sys.exit("zimwriterfs is not available, please install it.")

lang_input=sys.argv[2]
publisher=sys.argv[3]
list=get_list_item_info(sys.argv[1])
write_video_info(list)
dump_data(videos)
encode_videos(list, scraper_dir)
print title
create_zims(title)
