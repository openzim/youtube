#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import youtube_dl
import urllib
import requests
from datetime import datetime
from sys import platform as _platform
from jinja2 import Environment, FileSystemLoader
import pycaption
import json

type = ""
title = ""
videos = []
#prepare build folder
scraper_dir = "build/"
if not os.path.exists(scraper_dir):
	os.makedirs(scraper_dir)
if not os.path.exists(scraper_dir+"CSS/"):
	os.rename("templates/CSS/", scraper_dir+"CSS/")
if not os.path.exists(scraper_dir+"JS/"):
        os.rename("templates/JS/", scraper_dir+"JS/")
if not os.path.exists(scraper_dir+"favicon.png"):
        os.rename("templates/favicon.png", scraper_dir+"favicon.png")
if not os.path.exists(scraper_dir+"index.html"):
        os.rename("templates/welcome.html", scraper_dir+"index.html")

def get_list_item_info(url):
	"""
	Create dictionnary with all info about video playlist or user video
	structure is {dict [list of dict {dict for each video} ] }
	Only return list of video and write title of playlist/user name
	Save video in best quality in build/{id}/video.mp4 
	"""
        with youtube_dl.YoutubeDL({'outtmpl': scraper_dir+'%(id)s/video.mp4', 'writesubtitles': True}) as ydl:
        	result = ydl.extract_info(url, download=True) 
	title = result['title']
	type = result['extractor_key']
	return result.get('entries')

def welcome_page(title, author, id, description):
        videos.append({
            'id': id,
            'title': title.encode('ascii', 'ignore'),
            'description': description.encode('ascii', 'ignore'),
            'speaker': author.encode('ascii', 'ignore'),
            'thumbnail': id+"thumbnail.jpg".encode('ascii', 'ignore')})

def write_video_info(list):
        """
        Render static html pages from the scraped video data and
        save the pages in build/{video id}/index.html.
        """
	print 'Rendering template...'
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('video.html')

	for item in list:
		date = item.get('upload_date')
		id = item.get('id')
		publication_date = date[6:8]+"/"+date[4:6]+"/"+date[0:4]		
		subtitles = download_video_thumbnail_subtitles(id, item.get('subtitles'))
 		video_path = scraper_dir+id+"/" 

                html = template.render(
                        title=item.get('title'),
                        author=item.get('uploader'),
			vtt = subtitles,
                        description=item.get('description'),
                        url=item.get('webpage_url'),
                        date=publication_date)

                html = html.encode('utf-8')
                index_path = os.path.join(video_path, 'index.html')
                with open(index_path, 'w') as html_page:
                    html_page.write(html)
		welcome_page(item.get('title'), item.get('uploader'), id, item.get('description'))

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

def download_video_thumbnail_subtitles(id, subtitles):
	""" Download thumbnail and subtitles of each video in his folder """
	#download thumbnail
	thumbnail_url = "https://i.ytimg.com/vi/"+id+"/hqdefault.jpg"
	thumbnail_file = scraper_dir+id+"/thumbnail.jpg" 
	urllib.urlretrieve (thumbnail_url , thumbnail_file)  
	resize_image(thumbnail_file)
	#download substitle and add it to video.html if they exist
	if subtitles != "none" or subtitles != {}:
		subs_list = []
		for key in subtitles:
			caps = subtitles.get(key) 
			subs_list.append(caps)
		        reader = pycaption.detect_format(caps)
       			if reader:
			    file_name = scraper_dir+id+key+".vtt"
       			    subtitle_vtt = pycaption.WebVTTWriter().write(reader().read(caps))
			    webvttfile = open(file_name, "w") 
			    webvttfile.write(subtitle_vtt)
			    webvttfile.close()
	return subs_list

def resize_image(image_path):
    from PIL import Image
    image = Image.open(image_path)
    w, h = image.size
    image = image.resize((248, 187), Image.ANTIALIAS)
    image.save(image_path)

def encode_videos(list,scraper_dir):
         """
         Encode the videos from mp4 to webm. We will use ffmpeg over the 
         command line for this. There is a static binary version
         in the kiwix-other/youtube/ directory, that we will use on macs. 
         """
         for item in list:
                 video_id = str(item.get('id'))
                 video_path = os.path.join(scraper_dir, video_id, 'video.mp4')
                 video_copy_path = os.path.join(scraper_dir, video_id, 'video.webm')

                 if os.path.exists(video_copy_path):
                     print 'Video already encoded. Skipping.'
                     continue

                 if os.path.exists(video_path):
                      print 'Converting Video... ' + item.get('title')
                      convert_video_and_move_to_rendering(video_path, video_copy_path)


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


def create_zims():
        print 'Creating ZIM files'
        # Check, if the folder exists. Create it, if it doesn't.
      	zim_dir = scraper_dir
        if not os.path.exists(zim_dir):
            os.makedirs(zim_dir)
        html_dir = os.path.join(scraper_dir)
	zim_path = os.path.join(zim_dir, "youtube_{title}_{date}.zim".format(title=title,date=datetime.datetime.now().strftime('%Y-%m')))
	if type == "YoutubePlaylist":
		title = "Youtube - Playlist - {title} ".format(title=title)
	        description = "Youtube - {title} playlist video".format(title=title)	
	else:
		title = "Youtube - User - {title} ".format(title=title)
	        description = "Youtube - {title} user video".format(title=title)
        create_zim(html_dir, zim_path, title, description)

def create_zim(static_folder, zim_path, title, description):

    print "\tWritting ZIM for {}".format(title)

    context = {
        'languages': 'eng',
        'title': title,
        'description': description,
        'creator': 'Youtube',
        'publisher': 'Kiwix',

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

if not bin_is_present("zimwriterfs"):
        sys.exit("zimwriterfs is not available, please install it.")

list=get_list_item_info(sys.argv[1])
write_video_info(list)
dump_data(videos)
encode_videos(list, scraper_dir)
create_zims()
