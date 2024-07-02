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


def test_zim_scraper():
    """Ensure scraper and zim title are present in metadata"""

    zim_fh = Archive(ZIM_FILE_PATH)
    scraper = zim_fh.get_text_metadata("scraper")
    zim_title = zim_fh.get_text_metadata("Title")

    assert "youtube2zim " in scraper
    assert "openZIM_testing" in zim_title
