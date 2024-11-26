import json
import os

from zimscraperlib.zim import Archive

ZIM_FILE_PATH = os.getenv("ZIM_FILE_PATH") or "/output/openZIM_testing.zim"


def test_is_file():
    """Ensure ZIM file exists"""
    assert os.path.isfile(ZIM_FILE_PATH)


def test_zim_main_page():
    """Ensure main page is a redirect to index.html"""

    main_entry = Archive(ZIM_FILE_PATH).main_entry
    assert main_entry.is_redirect
    assert main_entry.get_redirect_entry().path == "index.html"


def test_zim_metadata():
    """Ensure scraper and zim title are present in metadata"""

    zim_fh = Archive(ZIM_FILE_PATH)

    assert "youtube2zim " in zim_fh.get_text_metadata("Scraper")
    assert zim_fh.get_text_metadata("Tags") == "tEsTing;x-mark:yes;_videos:yes"
    assert zim_fh.get_text_metadata("Title") == "openZIM_testing"
    assert zim_fh.get_text_metadata("Description") == "-"
    assert zim_fh.get_text_metadata("Language") == "eng"
    assert zim_fh.get_text_metadata("Name") == "tests_en_openzim-testing"
    assert zim_fh.get_text_metadata("Publisher") == "openZIM"
    assert zim_fh.get_text_metadata("Creator") == "Youtube Channel “openZIM_testing”"

    assert zim_fh.get_item("profile.jpg").mimetype == "image/jpeg"
    assert zim_fh.get_item("favicon.png").mimetype == "image/png"


def test_zim_channel_json():
    """Ensure channel.json exists and is valid"""

    zim_fh = Archive(ZIM_FILE_PATH)
    assert zim_fh.get_item("channel.json").mimetype == "application/json"
    channel_json = zim_fh.get_content("channel.json")
    channel_json = json.loads(channel_json)

    assert channel_json["id"] == "UC8elThf5TGMpQfQc_VE917Q"
    assert channel_json["channelName"] == "openZIM_testing"
    assert channel_json["firstPlaylist"] == "videos-917Q"


def test_zim_videos():
    """Ensure videos and video thumbnails are present in ZIM file"""

    zim_fh = Archive(ZIM_FILE_PATH)
    videos_json_list = [
        "cloudy_sky_time_lapse_4k_free_footage_video_gopro_11-k02q.json",
        "coffee_machine-DYvY.json",
        "marvel_studios_avengers_endgame_official_trailer-TcMB.json",
        "timelapse-9Tgo.json",
    ]

    for video_json_file in videos_json_list:
        json_path = "videos/" + video_json_file
        assert zim_fh.get_item(json_path).mimetype == "application/json"

        video_json = zim_fh.get_content(json_path)
        video_json = json.loads(video_json)

        assert zim_fh.get_item(video_json["videoPath"]).mimetype == "video/webm"
        assert zim_fh.get_item(video_json["thumbnailPath"]).mimetype == "image/webp"

        for subtitle in video_json["subtitleList"]:
            assert (
                zim_fh.get_item(
                    video_json["subtitlePath"] + f"/video.{subtitle["code"]}.vtt"
                ).mimetype
                == "text/vtt"
            )


def test_zim_playlists_file():
    """Ensure playlists json files are present in ZIM file"""

    zim_fh = Archive(ZIM_FILE_PATH)

    json_path = "playlists.json"
    assert zim_fh.get_item(json_path).mimetype == "application/json"

    video_json = zim_fh.get_content(json_path)
    video_json = json.loads(video_json)
    assert [video["slug"] for video in video_json["playlists"]] == [
        "trailers-5Gph",
        "timelapses-QgGI",
        "coffee-O2wS",
    ]
    assert set(video_json["playlists"][0].keys()) == {
        "slug",
        "id",
        "title",
        "thumbnailPath",
        "videosCount",
        "mainVideoSlug",
    }


def test_zim_home_playlists_file():
    """Ensure playlists json files are present in ZIM file"""

    zim_fh = Archive(ZIM_FILE_PATH)

    json_path = "home_playlists.json"
    assert zim_fh.get_item(json_path).mimetype == "application/json"

    video_json = zim_fh.get_content(json_path)
    video_json = json.loads(video_json)
    assert [video["slug"] for video in video_json["playlists"]] == [
        "videos-917Q",
        "short_videos-917Q",
        "trailers-5Gph",
        "timelapses-QgGI",
        "coffee-O2wS",
    ]
    assert set(video_json["playlists"][0].keys()) == {
        "slug",
        "id",
        "title",
        "thumbnailPath",
        "author",
        "description",
        "videosCount",
        "publicationDate",
        "videos",
    }
    assert set(video_json["playlists"][0]["videos"][0].keys()) == {
        "slug",
        "id",
        "title",
        "thumbnailPath",
        "duration",
    }


def test_zim_individual_playlists_files():
    """Ensure playlists json files are present in ZIM file"""

    zim_fh = Archive(ZIM_FILE_PATH)

    playlists_json_list = [
        "videos-917Q",
        "short_videos-917Q",
        "trailers-5Gph",
        "timelapses-QgGI",
        "coffee-O2wS",
    ]

    for playlist_json_file in playlists_json_list:
        json_path = f"playlists/{playlist_json_file}.json"
        assert zim_fh.get_item(json_path).mimetype == "application/json"
        content_json = zim_fh.get_content(json_path)
        content_json = json.loads(content_json)
        assert set(content_json.keys()) == {
            "slug",
            "id",
            "title",
            "thumbnailPath",
            "author",
            "description",
            "videosCount",
            "publicationDate",
            "videos",
        }
        assert set(content_json["videos"][0].keys()) == {
            "slug",
            "id",
            "title",
            "thumbnailPath",
            "duration",
        }
