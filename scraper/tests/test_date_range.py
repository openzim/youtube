from datetime import date

import pytest

import youtube2zim.scraper as scraper_module
from youtube2zim.scraper import Youtube2Zim
from youtube2zim.youtube import Playlist


def make_scraper(tmp_path, *, dateafter=None, datebefore=None):
    return Youtube2Zim(
        youtube_id="UCtest",
        api_key="test-api-key",
        video_format="mp4",
        low_quality=False,
        nb_videos_per_page=50,
        all_subtitles=False,
        output_dir=tmp_path / "output",
        zimui_dist=tmp_path / "zimui",
        fname=None,
        debug=False,
        tmp_dir=tmp_path / "tmp",
        max_concurrency=1,
        language="eng",
        tags="",
        dateafter=dateafter,
        use_any_optimized_version=False,
        s3_url_with_credentials=None,
        publisher="openZIM",
        disable_metadata_checks=True,
        stats_filename=None,
        skip_reencoding=False,
        subtitles_chapters_cache_expiry_days=30,
        datebefore=datebefore,
    )


def make_video(video_id, published_at):
    return {
        "contentDetails": {"videoId": video_id},
        "snippet": {
            "title": "Test video",
            "description": "Test description",
            "publishedAt": published_at,
        },
        "status": {"privacyStatus": "public"},
    }


def test_validate_date_range_input_without_filters(tmp_path):
    scraper = make_scraper(tmp_path)

    scraper.validate_date_range_input()

    assert scraper.dateafter is None
    assert scraper.datebefore is None
    assert scraper.video_date_range.start == date.min
    assert scraper.video_date_range.end == date.max


@pytest.mark.parametrize(
    ("dateafter", "datebefore", "expected_start", "expected_end"),
    [
        ("20200101", None, date(2020, 1, 1), date.max),
        (None, "20200101", date.min, date(2020, 1, 1)),
        ("20200101", "20201231", date(2020, 1, 1), date(2020, 12, 31)),
    ],
)
def test_validate_date_range_input(
    tmp_path, dateafter, datebefore, expected_start, expected_end
):
    scraper = make_scraper(tmp_path, dateafter=dateafter, datebefore=datebefore)

    scraper.validate_date_range_input()

    assert scraper.dateafter == dateafter
    assert scraper.datebefore == datebefore
    assert scraper.video_date_range.start == expected_start
    assert scraper.video_date_range.end == expected_end


def test_validate_dateafter_input_alias_still_works(tmp_path):
    scraper = make_scraper(tmp_path, datebefore="20200101")

    scraper.validate_dateafter_input()

    assert scraper.dateafter is None
    assert scraper.video_date_range.end == date(2020, 1, 1)


@pytest.mark.parametrize(
    ("dateafter", "datebefore"),
    [
        ("not-a-date", None),
        (None, "2020-01-01"),
        ("20210101", "20201231"),
    ],
)
def test_validate_date_range_input_rejects_invalid_ranges(
    tmp_path, dateafter, datebefore
):
    scraper = make_scraper(tmp_path, dateafter=dateafter, datebefore=datebefore)

    with pytest.raises(ValueError, match="Invalid date range"):
        scraper.validate_date_range_input()


def test_extract_videos_list_uses_combined_date_range(tmp_path, monkeypatch):
    scraper = make_scraper(tmp_path, dateafter="20200101", datebefore="20201231")
    scraper.validate_date_range_input()
    scraper.playlists = [
        Playlist(
            playlist_id="PLtest",
            title="Test playlist",
            description="Test description",
            creator_id="UCtest",
            creator_name="Test creator",
        )
    ]
    videos = [
        make_video("too-early", "2019-12-31T23:59:59Z"),
        make_video("first-day", "2020-01-01T00:00:00Z"),
        make_video("middle", "2020-06-15T12:00:00Z"),
        make_video("last-day", "2020-12-31T23:59:59Z"),
        make_video("too-late", "2021-01-01T00:00:00Z"),
    ]
    monkeypatch.setattr(scraper_module, "load_json", lambda _dir, _key: None)
    monkeypatch.setattr(scraper_module, "get_videos_json", lambda _playlist_id: videos)
    monkeypatch.setattr(scraper_module, "save_json", lambda _dir, _key, _data: None)

    scraper.extract_videos_list()

    assert scraper.videos_ids == ["first-day", "middle", "last-day"]
