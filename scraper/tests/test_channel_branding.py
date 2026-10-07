from youtube2zim import youtube
from youtube2zim.youtube import BANNER_DOWNLOAD_SIZE, save_channel_branding

CHANNEL_ID = "UCTq1zHztiV69Ur8t6jco4CQ"
BANNER_URL = "https://yt3.googleusercontent.com/banner-id"


def _channel_json(*, banner=True):
    channel = {
        "id": CHANNEL_ID,
        "snippet": {"thumbnails": {"medium": {"url": "https://example.com/p.jpg"}}},
        "brandingSettings": {"image": {}},
    }
    if banner:
        channel["brandingSettings"]["image"]["bannerExternalUrl"] = BANNER_URL
    return channel


def _patch(monkeypatch, channel_json):
    downloaded = []
    monkeypatch.setattr(youtube, "get_channel_json", lambda _channel_id: channel_json)
    monkeypatch.setattr(
        youtube, "stream_file", lambda url, path: (downloaded.append(url), path.touch())
    )
    monkeypatch.setattr(youtube, "resize_image", lambda *_args, **_kwargs: None)
    return downloaded


def test_banner_saved_from_banner_external_url(tmp_path, monkeypatch):
    downloaded = _patch(monkeypatch, _channel_json())

    save_channel_branding(tmp_path, CHANNEL_ID, save_banner=True)

    assert f"{BANNER_URL}={BANNER_DOWNLOAD_SIZE}" in downloaded
    assert (tmp_path / CHANNEL_ID / "banner.jpg").exists()


def test_banner_not_saved_unless_requested(tmp_path, monkeypatch):
    downloaded = _patch(monkeypatch, _channel_json())

    save_channel_branding(tmp_path, CHANNEL_ID, save_banner=False)

    assert downloaded == ["https://example.com/p.jpg"]
    assert not (tmp_path / CHANNEL_ID / "banner.jpg").exists()


def test_channel_without_banner(tmp_path, monkeypatch):
    downloaded = _patch(monkeypatch, _channel_json(banner=False))

    save_channel_branding(tmp_path, CHANNEL_ID, save_banner=True)

    assert downloaded == ["https://example.com/p.jpg"]
    assert not (tmp_path / CHANNEL_ID / "banner.jpg").exists()
