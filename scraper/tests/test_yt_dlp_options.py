"""Tests for the yt-dlp options youtube2zim passes to yt-dlp"""

from typing import Any, cast

import pytest
import yt_dlp

from youtube2zim import scraper as scraper_module
from youtube2zim.scraper import Youtube2Zim


def build_scraper(tmp_path, **kwargs):
    """a Youtube2Zim instance, without running anything"""

    defaults = {
        "youtube_id": "UC8elThf5TGMpQfQc_VE917Q",
        "api_key": "dummy",
        "video_format": "webm",
        "low_quality": False,
        "nb_videos_per_page": 40,
        "all_subtitles": False,
        "output_dir": str(tmp_path / "output"),
        "zimui_dist": str(tmp_path / "zimui"),
        "fname": "test.zim",
        "debug": False,
        "tmp_dir": str(tmp_path / "tmp"),
        "max_concurrency": 1,
        "language": "eng",
        "tags": "youtube",
        "dateafter": "now-1d",
        "use_any_optimized_version": False,
        "s3_url_with_credentials": None,
        "publisher": "openZIM",
        "disable_metadata_checks": True,
        "stats_filename": None,
        "skip_reencoding": False,
        "subtitles_chapters_cache_expiry_days": 30,
    }
    defaults.update(kwargs)
    scraper = Youtube2Zim(**defaults)
    scraper.videos_dir.mkdir(parents=True, exist_ok=True)
    return scraper


def test_no_yt_dlp_option_by_default(tmp_path, monkeypatch):
    """the defaults must not change anything for existing users"""

    monkeypatch.setattr(scraper_module, "BUNDLED_PLUGIN_DIR", tmp_path / "absent")

    scraper = build_scraper(tmp_path)

    assert scraper.extractor_args == {}
    assert scraper.yt_dlp_plugin_dirs == []

    options = scraper.get_yt_dlp_options()
    assert "extractor_args" not in options
    assert "plugin_dirs" not in options


def test_bundled_plugin_dir_is_used_when_present(tmp_path, monkeypatch):
    """the image ships a provider, so it should be picked up without any flag"""

    bundled = tmp_path / "yt-dlp-plugins"
    bundled.mkdir()
    monkeypatch.setattr(scraper_module, "BUNDLED_PLUGIN_DIR", bundled)

    scraper = build_scraper(tmp_path)

    assert scraper.yt_dlp_plugin_dirs == [bundled]
    assert scraper.get_yt_dlp_options()["plugin_dirs"] == [str(bundled)]


def test_explicit_plugin_dir_replaces_the_bundled_one(tmp_path, monkeypatch):
    """--yt-dlp-plugin-dir is how a caller opts out of the bundled provider"""

    bundled = tmp_path / "yt-dlp-plugins"
    bundled.mkdir()
    monkeypatch.setattr(scraper_module, "BUNDLED_PLUGIN_DIR", bundled)
    custom = tmp_path / "plugins"
    custom.mkdir()

    scraper = build_scraper(tmp_path, yt_dlp_plugin_dirs=[str(custom)])

    assert scraper.yt_dlp_plugin_dirs == [custom.resolve()]


def test_extractor_args_are_forwarded(tmp_path):
    scraper = build_scraper(
        tmp_path,
        yt_dlp_extractor_args=["youtubepot-bgutilhttp:base_url=http://127.0.0.1:4416"],
    )

    assert scraper.get_yt_dlp_options()["extractor_args"] == {
        "youtubepot-bgutilhttp": {"base_url": ["http://127.0.0.1:4416"]}
    }


def test_player_client_becomes_an_extractor_arg(tmp_path):
    scraper = build_scraper(tmp_path, player_client="mweb,web")

    assert scraper.extractor_args == {"youtube": {"player_client": ["mweb", "web"]}}
    assert scraper.get_yt_dlp_options()["extractor_args"] == {
        "youtube": {"player_client": ["mweb", "web"]}
    }


def test_player_client_keeps_other_youtube_args(tmp_path):
    scraper = build_scraper(
        tmp_path,
        player_client="mweb",
        yt_dlp_extractor_args=["youtube:fetch_pot=always"],
    )

    assert scraper.extractor_args == {
        "youtube": {"fetch_pot": ["always"], "player_client": ["mweb"]}
    }


def test_player_client_wins_over_the_raw_option(tmp_path):
    """the dedicated option is the more specific one, so it takes precedence"""

    scraper = build_scraper(
        tmp_path,
        player_client="mweb",
        yt_dlp_extractor_args=["youtube:player_client=web"],
    )

    assert scraper.extractor_args == {"youtube": {"player_client": ["mweb"]}}


def test_plugin_dirs_are_resolved(tmp_path):
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()

    scraper = build_scraper(
        tmp_path, yt_dlp_plugin_dirs=[str(plugin_dir), f"{plugin_dir}/"]
    )

    assert scraper.yt_dlp_plugin_dirs == [plugin_dir.resolve(), plugin_dir.resolve()]
    assert scraper.get_yt_dlp_options()["plugin_dirs"] == [
        str(plugin_dir.resolve()),
        str(plugin_dir.resolve()),
    ]


def test_missing_plugin_dir_fails_early(tmp_path):
    with pytest.raises(ValueError, match="--yt-dlp-plugin-dir could not be found"):
        build_scraper(tmp_path, yt_dlp_plugin_dirs=[str(tmp_path / "nope")])


def test_invalid_extractor_arg_fails_early(tmp_path):
    with pytest.raises(ValueError, match="Invalid extractor argument"):
        build_scraper(tmp_path, yt_dlp_extractor_args=["nonsense"])


def test_blank_player_client_fails_early(tmp_path):
    with pytest.raises(ValueError, match="Invalid player client value"):
        build_scraper(tmp_path, player_client=" , ")


def test_yt_dlp_accepts_the_generated_options(tmp_path):
    """the shape must be one yt-dlp can actually be handed"""

    scraper = build_scraper(
        tmp_path,
        player_client="mweb",
        yt_dlp_extractor_args=[
            "youtubepot-bgutilhttp:base_url=http://127.0.0.1:4416",
            "youtube:fetch_pot=always",
        ],
    )
    options = scraper.get_yt_dlp_options()
    options.pop("y2z_videos_dir")  # our own marker, unknown to yt-dlp

    with yt_dlp.YoutubeDL(cast(Any, options)) as ydl:
        assert cast(dict, ydl.params).get("extractor_args") == {
            "youtube": {"player_client": ["mweb"], "fetch_pot": ["always"]},
            "youtubepot-bgutilhttp": {"base_url": ["http://127.0.0.1:4416"]},
        }
