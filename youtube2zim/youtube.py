#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import requests

from .constants import logger, YOUTUBE
from .utils import save_json, load_json, save_file, resize_image, get_slug


YOUTUBE_API = "https://www.googleapis.com/youtube/v3"
PLAYLIST_API = f"{YOUTUBE_API}/playlists"
PLAYLIST_ITEMS_API = f"{YOUTUBE_API}/playlistItems"
CHANNEL_SECTIONS_API = f"{YOUTUBE_API}/channelSections"
CHANNELS_API = f"{YOUTUBE_API}/channels"
SEARCH_API = f"{YOUTUBE_API}/search"
VIDEOS_API = f"{YOUTUBE_API}/videos"
RESULTS_PER_PAGE = 50  # max: 50


class Playlist(object):
    def __init__(self, playlist_id, title, description, creator_id, creator_name):
        self.playlist_id = playlist_id
        self.title = title
        self.description = description
        self.creator_id = creator_id
        self.creator_name = creator_name
        self.slug = get_slug(title, js_safe=True)

    @classmethod
    def from_id(cls, playlist_id):
        playlist_json = get_playlist_json(playlist_id)
        return Playlist(
            playlist_id=playlist_id,
            title=playlist_json["snippet"]["title"],
            description=playlist_json["snippet"]["description"],
            creator_id=playlist_json["snippet"]["channelId"],
            creator_name=playlist_json["snippet"]["channelTitle"],
        )


def credentials_ok():
    """ check that a Youtube search is successful, validating API_KEY """
    req = requests.get(
        SEARCH_API, params={"part": "snippet", "maxResults": 1, "key": YOUTUBE.api_key}
    )
    try:
        req.raise_for_status()
        return bool(req.json()["items"])
    except Exception:
        return False


def get_channel_json(channel_id, for_username=False):
    """ fetch or retieve-save and return the Youtube ChannelResult JSON """
    fname = f"channel_{channel_id}"
    channel_json = load_json(YOUTUBE.cache_dir, fname)
    if channel_json is None:
        logger.debug(f"query youtube-api for Channel #{channel_id}")
        req = requests.get(
            CHANNELS_API,
            params={
                "forUsername" if for_username else "id": channel_id,
                "part": "brandingSettings,snippet,localizations,contentDetails",
                "key": YOUTUBE.api_key,
            },
        )
        req.raise_for_status()
        try:
            channel_json = req.json()["items"][0]
        except IndexError:
            if for_username:
                logger.error(f"Invalid username `{channel_id}`: Not Found")
            else:
                logger.error(f"Invalid channelId `{channel_id}`: Not Found")
            raise
        save_json(YOUTUBE.cache_dir, fname, channel_json)
    return channel_json


def get_channel_playlists_json(channel_id):
    """ fetch or retieve-save and return the Youtube Playlists JSON for a channel"""
    fname = f"channel_{channel_id}_playlists"
    channel_playlists_json = load_json(YOUTUBE.cache_dir, fname)

    items = load_json(YOUTUBE.cache_dir, fname)
    if items is not None:
        return items

    logger.debug(f"query youtube-api for Playlists of channel #{channel_id}")

    items = []
    page_token = None
    while True:
        req = requests.get(
            PLAYLIST_API,
            params={
                "channelId": channel_id,
                "part": "id",
                "key": YOUTUBE.api_key,
                "maxResults": RESULTS_PER_PAGE,
                "pageToken": page_token,
            },
        )
        req.raise_for_status()
        channel_playlists_json = req.json()
        items += channel_playlists_json["items"]
        page_token = channel_playlists_json.get("nextPageToken")
        if not page_token:
            break
        save_json(YOUTUBE.cache_dir, fname, items)
    return items


def get_playlist_json(playlist_id):
    """ fetch or retieve-save and return the Youtube PlaylistResult JSON """
    fname = f"playlist_{playlist_id}"
    playlist_json = load_json(YOUTUBE.cache_dir, fname)
    if playlist_json is None:
        logger.debug(f"query youtube-api for Playlist #{playlist_id}")
        req = requests.get(
            PLAYLIST_API,
            params={"id": playlist_id, "part": "snippet", "key": YOUTUBE.api_key},
        )
        req.raise_for_status()
        try:
            playlist_json = req.json()["items"][0]
        except IndexError:
            logger.error(f"Invalid playlistId `{playlist_id}`: Not Found")
            raise
        save_json(YOUTUBE.cache_dir, fname, playlist_json)
    return playlist_json


def get_videos_json(playlist_id):
    """ retrieve a list of youtube PlaylistItem dict

        same request for both channel and playlist
        channel mode uses `uploads` playlist from channel """

    fname = f"playlist_{playlist_id}_videos"
    items = load_json(YOUTUBE.cache_dir, fname)
    if items is not None:
        return items

    logger.debug(f"query youtube-api for PlaylistItems of playlist #{playlist_id}")

    items = []
    page_token = None
    while True:
        req = requests.get(
            PLAYLIST_ITEMS_API,
            params={
                "playlistId": playlist_id,
                "part": "snippet,contentDetails",
                "key": YOUTUBE.api_key,
                "maxResults": RESULTS_PER_PAGE,
                "pageToken": page_token,
            },
        )
        req.raise_for_status()
        videos_json = req.json()
        items += videos_json["items"]
        page_token = videos_json.get("nextPageToken")
        if not page_token:
            break

    save_json(YOUTUBE.cache_dir, fname, items)
    return items


def get_videos_authors_info(videos_ids):
    """ query authors' info for each video from their relative channel """

    items = load_json(YOUTUBE.cache_dir, "videos_channels")

    if items is not None:
        return items

    logger.debug(
        "query youtube-api for Video details of {} videos".format(len(videos_ids))
    )

    items = {}
    page_token = None
    while True:
        req = requests.get(
            VIDEOS_API,
            params={
                "id": ",".join(videos_ids),
                "part": "snippet",
                "key": YOUTUBE.api_key,
                "maxResults": RESULTS_PER_PAGE,
                "pageToken": page_token,
            },
        )
        req.raise_for_status()
        videos_json = req.json()
        for item in videos_json["items"]:
            items.update(
                {
                    item["id"]: {
                        "channelId": item["snippet"]["channelId"],
                        "channelTitle": item["snippet"]["channelTitle"],
                    }
                }
            )
        page_token = videos_json.get("nextPageToken")
        if not page_token:
            break

    save_json(YOUTUBE.cache_dir, "videos_channels", items)

    return items


def save_channel_branding(channels_dir, channel_id, save_banner=False):
    """ download, save and resize profile [and banner] of a channel """
    channel_json = get_channel_json(channel_id)

    thumbnails = channel_json["snippet"]["thumbnails"]
    for quality in ("medium", "default"):  # high:800px, medium:240px, default:88px
        if quality in thumbnails.keys():
            thumnbail = thumbnails[quality]["url"]
            break

    profile_path = channels_dir.joinpath(channel_id, "profile.jpg")
    if not profile_path.exists():
        save_file(thumnbail, profile_path)
        # resize profile as we only use up 100px/80 sq
        resize_image(profile_path, width=100, height=100)

    if save_banner:
        banner = channel_json["brandingSettings"]["image"]["bannerImageUrl"]
        banner_path = channels_dir.joinpath(channel_id, "banner.jpg")
        if not banner_path.exists():
            save_file(banner, banner_path)
