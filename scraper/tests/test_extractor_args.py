"""Tests for the yt-dlp extractor argument parsing"""

import pytest
from yt_dlp.options import parseOpts

from youtube2zim.utils import parse_extractor_args


def yt_dlp_parse(*args):
    """the `extractor_args` yt-dlp itself builds for the same CLI input"""

    return parseOpts(list(args))[1].extractor_args


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


def test_repeated_extractor_is_merged():
    assert parse_extractor_args(
        [
            "youtube:player_client=web",
            "youtube:fetch_pot=always",
            "youtubepot-bgutilhttp:base_url=http://host:4416",
        ]
    ) == {
        "youtube": {"player_client": ["web"], "fetch_pot": ["always"]},
        "youtubepot-bgutilhttp": {"base_url": ["http://host:4416"]},
    }


def test_empty_value_is_kept():
    """yt-dlp turns `key=` into an empty list, so we must not silently drop it"""

    assert parse_extractor_args(["youtube:player_client="]) == {
        "youtube": {"player_client": [""]}
    }


def test_empty_segments_are_skipped():
    assert parse_extractor_args(["youtube:player_client=web;;fetch_pot=always;"]) == {
        "youtube": {"player_client": ["web"], "fetch_pot": ["always"]}
    }


@pytest.mark.parametrize(
    "value",
    [
        "",
        "youtube",
        "youtube:",
        ":player_client=web",
        "youtube:player_client",
    ],
)
def test_invalid_arguments_are_rejected(value):
    with pytest.raises(ValueError, match="Invalid extractor argument"):
        parse_extractor_args([value])


def test_invalid_argument_does_not_leave_partial_state():
    with pytest.raises(ValueError):
        parse_extractor_args(["youtube:player_client=web", "broken"])


@pytest.mark.parametrize(
    "value",
    [
        "youtube:player_client=web",
        "youtubepot-bgutilhttp:base_url=http://host:4416",
        "youtube:player_client=web,mweb",
        r"youtube:player_client=web\,mweb",
        "youtube:player-client=web\\,mweb;fetch_pot=always",
        "youtubepot-bgutilhttp:base_url=http://host:4416;token_ttl=6",
    ],
)
def test_matches_yt_dlp_own_parsing(value):
    """our output must be exactly what yt-dlp builds for the same CLI input"""

    assert parse_extractor_args([value]) == yt_dlp_parse("--extractor-args", value)


def test_repeated_extractor_merges_instead_of_overriding():
    """yt-dlp's CLI keeps only the last option for an extractor, which silently
    drops whatever came before; we merge so nothing gets lost"""

    values = [
        "youtube:player_client=web",
        "youtube:fetch_pot=always",
    ]
    assert parse_extractor_args(values) == {
        "youtube": {"player_client": ["web"], "fetch_pot": ["always"]}
    }

    # yt-dlp itself only keeps the last one
    assert yt_dlp_parse(
        "--extractor-args",
        values[0],
        "--extractor-args",
        values[1],
    ) == {"youtube": {"fetch_pot": ["always"]}}

    # which is what a single option holding both arguments gives
    assert parse_extractor_args(values) == yt_dlp_parse(
        "--extractor-args", "youtube:player_client=web;fetch_pot=always"
    )


def test_matches_yt_dlp_across_repeated_options():
    """repeated options for *different* extractors must behave like yt-dlp"""

    values = [
        "youtube:player_client=web",
        "youtubepot-bgutilhttp:base_url=http://host:4416",
    ]
    cli = []
    for value in values:
        cli += ["--extractor-args", value]

    assert parse_extractor_args(values) == yt_dlp_parse(*cli)
