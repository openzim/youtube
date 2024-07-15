import json
import os

from zimscraperlib.zim import Archive

ZIM_FILE_PATH = "/output/openZIM_testing.zim"


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

    assert "youtube2zim " in zim_fh.get_text_metadata("scraper")
    assert "openZIM_testing" in zim_fh.get_text_metadata("Title")
    assert "-" in zim_fh.get_text_metadata("Description")
    assert "en" in zim_fh.get_text_metadata("Language")
    assert "openZIM" in zim_fh.get_text_metadata("Publisher")
    assert "openZIM_testing" in zim_fh.get_text_metadata("Creator")

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
    assert channel_json["collectionType"] == "channel"
    assert channel_json["mainPlaylist"] == "uploads_from_openzim_testing-917Q"


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


def test_zim_playlists():
    """Ensure playlists json files are present in ZIM file"""

    zim_fh = Archive(ZIM_FILE_PATH)
    playlists_json_list = [
        "coffee-O2wS.json",
        "timelapses-QgGI.json",
        "trailers-5Gph.json",
        "uploads_from_openzim_testing-917Q.json",
    ]

    for playlist_json_file in playlists_json_list:
        json_path = "playlists/" + playlist_json_file
        assert zim_fh.get_item(json_path).mimetype == "application/json"
