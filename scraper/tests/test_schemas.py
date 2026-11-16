from youtube2zim.schemas import (
    Author,
    Config,
    Playlist,
    Subtitle,
    Subtitles,
    Video,
    VideoPreview,
)


def test_aliases_are_camel_case():
    video = Video(
        id="video-id",
        title="Video title",
        description="Video description",
        author=Author(
            channel_id="channel-id",
            channel_title="Channel title",
            channel_description="Channel description",
            channel_joined_date="2024-01-01",
        ),
        publication_date="2024-01-01",
        video_path="videos/video-id.mp4",
        subtitle_list=[Subtitle(code="en", name="English")],
        chapter_list=[],
        duration="00:01:00",
    )

    payload = video.model_dump(by_alias=True)

    assert payload["publicationDate"] == "2024-01-01"
    assert payload["videoPath"] == "videos/video-id.mp4"
    assert payload["subtitleList"] == [{"code": "en", "name": "English"}]
    assert payload["chapterList"] == []
    assert "publication_date" not in payload
    assert payload["author"]["channelId"] == "channel-id"
    assert payload["author"]["channelTitle"] == "Channel title"
    assert payload["author"]["channelDescription"] == "Channel description"
    assert payload["author"]["channelJoinedDate"] == "2024-01-01"


def test_aliases_round_trip_snake_case_input():
    playlist = Playlist(
        id="playlist-id",
        slug="playlist-slug",
        author=Author(
            channel_id="channel-id",
            channel_title="Channel title",
            channel_description="Channel description",
            channel_joined_date="2024-01-01",
        ),
        title="Playlist title",
        description="Playlist description",
        publication_date="2024-01-01",
        videos=[
            VideoPreview(
                slug="video-slug",
                id="video-id",
                title="Video title",
                duration="00:01:00",
            )
        ],
        videos_count=1,
        duration="00:01:00",
    )

    assert playlist.model_dump(by_alias=True)["videosCount"] == 1
    assert Playlist(**playlist.model_dump()).videos_count == 1


def test_optional_fields_keep_camel_case_aliases():
    subtitles = Subtitles(subtitles=[Subtitle(code="fr", name="French")])
    config = Config(main_color=None, secondary_color="#ffffff")

    assert subtitles.model_dump(by_alias=True) == {
        "subtitles": [{"code": "fr", "name": "French"}]
    }
    assert config.model_dump(by_alias=True) == {
        "mainColor": None,
        "secondaryColor": "#ffffff",
    }
