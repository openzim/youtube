"""Tests for the yt-dlp extractor argument parsing"""

import pytest

from youtube2zim.utils import parse_extractor_args


def test_no_values():
    assert parse_extractor_args(None) == {}
    assert parse_extractor_args([]) == {}


def test_single_argument():
    assert parse_extractor_args(["youtube:player_client=web"]) == {
        "youtube": {"player_client": ["web"]}
    }


def test_extractor_key_is_lowercased():
    assert parse_extractor_args(["YouTube:player_client=web"]) == {
        "youtube": {"player_client": ["web"]}
    }


def test_argument_name_is_lowercased_and_dashed():
    assert parse_extractor_args(
        ["youtubepot-bgutilhttp:base-url=http://host:4416"]
    ) == {"youtubepot-bgutilhttp": {"base_url": ["http://host:4416"]}}


def test_multiple_values_for_one_argument():
    assert parse_extractor_args(["youtube:player_client=web,mweb,tv"]) == {
        "youtube": {"player_client": ["web", "mweb", "tv"]}
    }


def test_escaped_comma_stays_in_value():
    assert parse_extractor_args([r"youtube:player_client=web\,mweb"]) == {
        "youtube": {"player_client": ["web,mweb"]}
    }


def test_several_arguments_of_one_extractor():
    assert parse_extractor_args(
        ["youtubepot-bgutilhttp:base_url=http://host:4416;token_ttl=6"]
    ) == {
        "youtubepot-bgutilhttp": {
            "base_url": ["http://host:4416"],
            "token_ttl": ["6"],
        }
    }


def test_argument_without_value_is_an_empty_string():
    """yt-dlp accepts `IE_KEY:ARG` and turns the value into [''], so we must too"""

    assert parse_extractor_args(["youtube:player_client"]) == {
        "youtube": {"player_client": [""]}
    }


def test_empty_value_is_kept():
    assert parse_extractor_args(["youtube:player_client="]) == {
        "youtube": {"player_client": [""]}
    }


def test_stray_separator_matches_yt_dlp():
    """yt-dlp inserts a spurious empty key for a `;;`, and so do we now"""

    assert parse_extractor_args(["youtube:player_client=web;;fetch_pot=always;"]) == {
        "youtube": {"player_client": ["web"], "": [""], "fetch_pot": ["always"]}
    }


def test_repeated_extractor_keeps_the_last_option():
    """repeating an extractor is parsed exactly like yt-dlp's CLI: last wins"""

    assert parse_extractor_args(
        [
            "youtube:player_client=web",
            "youtube:fetch_pot=always",
        ]
    ) == {"youtube": {"fetch_pot": ["always"]}}


def test_repeated_extractor_arguments_are_merged_in_one_option():
    assert parse_extractor_args(["youtube:player_client=web;fetch_pot=always"]) == {
        "youtube": {"player_client": ["web"], "fetch_pot": ["always"]}
    }


def test_different_extractors_are_kept():
    assert parse_extractor_args(
        [
            "youtube:player_client=web",
            "youtubepot-bgutilhttp:base_url=http://host:4416",
        ]
    ) == {
        "youtube": {"player_client": ["web"]},
        "youtubepot-bgutilhttp": {"base_url": ["http://host:4416"]},
    }


@pytest.mark.parametrize(
    "value",
    [
        "",
        "youtube",
        "nonsense",
    ],
)
def test_invalid_arguments_are_rejected(value):
    with pytest.raises(ValueError, match="Invalid extractor argument"):
        parse_extractor_args([value])


def test_invalid_argument_does_not_leave_partial_state():
    with pytest.raises(ValueError):
        parse_extractor_args(["youtube:player_client=web", "broken"])
