## Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (as of version 2.1.15).

## [Unreleased]

### Added

- Added Total playlist duration in the Playlist view and Playlist panel. (#435)

## [3.5.0] - 2025-11-17

### Added

- Skip re-encoding downloaded videos with `--skip-reencoding` optional argument (#415)
- Upgrade to Python 3.14 (and dependencies) and Node.JS 24 (and dependencies) and Debian Trixie (#426)
- Add `deno` dependency to fix yt-dlp requirement for Youtube (#418)
- Add impersonation library (#428)

## [3.4.1] - 2025-07-22

### Fixed

- Thumbnails processing crashes (#408)
- Upgrade frontend dependencies, especially Video.JS 8.23.3 (#407 #411)

## [3.4.0] - 2025-07-03

### Added

- Add support for video chapters (#170)
- Activate links, emails of video description (#390)
- Add skip forward/backward functionality and keyboard & touch controls (#397)
- Add theater mode to video player (#399)

### Fixed

- Fix detection of credentials validity (#402)

### Changed

- Upgraded to zimscraperlib 5.1.1, Python 3.13, and upgraded other Python dependencies (#404)

## [3.3.0] - 2024-12-05

### Changed

- Differentiate user uploaded shorts, lives & long videos (#367)

### Fixed

- Corrected the short video resolution in the UI (#366)
- Check for empty playlists after filtering, and after downloading videos (#375)
- Unlisted videos must also be included inside the ZIM (#379)

## [3.2.1] - 2024-11-01

### Deprecated

- `--type` CLI argument is now deprecated (will be removed in next major)

### Changed

- Raise exception if there are no videos in the playlists (#347)
- Drop `--type` CLI argument and guess `--id` type (#361)
- Always reencode using our presets (even for high quality) and choose best format when downloading from Youtube (#356)

### Fixed

- Filter-out non-public videos and properly cleanup unsuccessful videos (#362)
- Use proper ZIM metadata key for `Scraper` and `Tags` (#369)
- Add missing `playsinline` attribute for Video.JS on iOS (#368)

## [3.2.0] - 2024-10-11

### Deprecated

- `--type user` is now deprecated (will be removed in next major)

### Fixed

- Ignore empty playlists (#340)
- Fix `format` setting passed to yt-dlp (#351)

### Changed

- Merge behaviors of user/channel types and add support for `forHandle` (#339, fix for #338)
- Update layout of `Videos` tab in `zimui` to display videos from all playlists in the ZIM (#337)

## [3.1.0] - 2024-09-05

### Added

- Report scraper progress in a JSON file specified with `--stats-filename` (#228)

### Fixed

- Fix main playlist selection to respect the order of provided playlist IDs (#286)
- Fix `PLAYLISTS` tab not being highlighted when the page is reloaded (#299)

### Changed

- Update dependencies, including zimscraperlib 4 (#306)
- Update `zimui` title dynamically with the selected playlist/video title (#298)

## [3.0.1] - 2024-08-13

### Fixed

- Disable preloading of subtitles in video.js in `zimui` (#38)
- Fix scraper to exit properly when `Too much videos failed to download` exceptions are raised (#285)
- Clean up temporary files properly in case of exceptions during scraper run (#288)
- Implement infinite scroll for video/playlist lists and add loading spinners in `zimui` (#284)
- Update video.JS to 8.17.3, brings support for Chrome 58 and 59 (#275)

## [3.0.0] - 2024-07-29

### Changed

This release represent a very significant update of the scraper UI and the underlying technology (use Vue.JS 3 JS framework).

- Move scraper files to `scraper` subfolder and update workflows
- Bump `requests` package from 2.32.0 to 2.32.2
- Initialize new Vue.js project in `zimui` subfolder
- Update dependencies in pyproject.toml (pydantic, pyhumps, python-slugify)
- Update scraper to generate JSON files for `zimui` (#212)
- Remove old UI files and methods: template files (home.html, article.html) and `make_html_files` method in scraper.py
- Remove `--locale` arg, broken locale folder, files used for translation; translation will be restored with #222
- Create "Videos" and "Playlists" tabs for homepage in new Vue.js UI (#213, #214)
- Create video player page in new Vue.js UI (#215)
- Add support for variable playback speed in video player (#174)
- Updgrade to zimscraperlib 3.4.0 (including **new webm encoder presets to migrate to VP9 instead of VP8**) (#204)
- Add playlist panel for playing videos in a playlist (#216)
- Remove `--autoplay` CLI argument and set autoplay to always be true (#233)
- Add playlist view page in new Vue.js UI (#223)
- Add support for ogv.js in video-js player (#230)
- Remove openzim.toml and install all dependencies using Yarn (#218)
- Validate if ZIM cannot be created at given output location (#204)
- Add videos, subtitles, thumbnails and channel branding to the ZIM "on the fly" (#209)
- Remove `--no-zim`, `--keep` CLI arguments
- Add support to index content from `zimui` JSON files in the ZIM using custom `IndexData` (#224)
- Add integration tests to check the content of the ZIM created by the scraper (#268)
- Add an overlay image for the channel banner (#279)

## [2.3.0] - 2024-05-22

### Added

- New `long_description` CLI argument to set the ZIM long description
- New `disable_metadata_check` CLI argument to disable the metadata checks which are automated since zimscraperlib 3.x

### Changed

- Changed default publisher metadata to 'openZIM'
- Validate ZIM metadata (tags, title, description, long_description) as early as possible
- Migrate to zimscraperlib 3.3.2 (including **new VideoLowWebm encoder preset version 2**)
- Upgrade Python dependencies, including migration to Python 3.12

## [2.2.0] - 2023-11-17

### Changed

- Using zimscraperlib 2.0.0 (#171)
- Using python 3.10 + debian bookworm (dropped support for older Python versions) (#180)
- Adopt Python bootstrap conventions (including hatch) (#180)

### Fixed

- Fixed local path media (profile, banner) not working (#178)
- Unset `metadata_from` in `youtube2zim-playlists` (#185)
- Do not move local banner and profile images, copy them instead #179

## [2.1.18] - 2022-11-09

### Changed

- Switched to yt-dlp instead of youtube_dl
- Added fallback for subtitle languages with IDs-like suffixes (#161)
- Removed a reference to ZIM namespace that would break if first video has subtitles
- Fixed expected returncodes on errors (#166)
- Using ogv.js 1.8.9, videojs 7.20.3 and latest videojs-ogvjs (master)
- Using zimscraperlib 1.8.0

## [2.1.17] - 2022-08-01

### Changed

- Fixed typo breaking JS

## [2.1.16] - 2022-08-01

### Changed

- Fixed Jinja2's dependency: Markup_safe version (#156)

## [2.1.15] - 2022-07-29

### Added

- Additional YT language code mapping: zh-Hant-HK, zh-Hans-SG

### Changed

- using zimscraperlib 1.6.2
- fixed crash adding ogvjs's js.mem file
- fixed playlists switching removing videos
- Removed inline JS to comply with some CSP (#154)

## [2.1.13]

- More YT language code mapping

## [2.1.12]

- fixed inter-dependencies issue

## [2.1.11]

- removed banner retrieval due to API change

## [2.1.10]

- fixes to Webp for apple polyfill

## [2.1.9]

- fixed WebP poster for apple on video pages

## [2.1.8]

- fixed subtitles not showing on homepage preview video
- fixed crash on iw (Hebrew) subtitles
- fixed usage on older browsers (without ES6 support)
- use WebP for thumbnails
- fix seeking on Apple browsers

## [2.1.7]

- using zimscraperlib 1.2.0
- replaced zimwriterfs with pylibzim
- tmp-dir now sanitized as build-dir
- fixed --debug not forwarded in playlists mode
- changed workdir to /output in docker image

## [2.1.6]

- using video-js-7.8.1
- Added youtube2zim-playlists script to create one zim per playlist
- --zim-file now supports the `{period}` replacement string to insert date (#99)
- picture-in-picture toggle now hidden
- using zimscraperlib to encode videos
- logging transfer before starting them
- added video_encoding_tester script in contrib/
- --tmp-dir option to set where temp files are downloaded/handled (system temp otherwise)
- thumbnail now converted to JPEG if received as WebP
- thumbnail resize now supports upscaling if original is too small
- thumnail resize and conversion from zimscraperlib
- using zimscraperlib 1.1.2
- removed skip-download option
- removed only_test_branding option
- docker to use zimwriterfs 1.3.10

## [2.1.5]

- Fixed regression causing S3 to only use videos from cache (never youtube)

## [2.1.4]

- Fixed compression issue on system without swap (#75)
- Using 44kHz audio sample rate on low-quality to save some space (#74)
- Added S3 Optimization Cache support (#69 #80)
- Bumped some dependencies (zimscraperlib, kiwixstorage)
- Filtering out videos with missing channel (#76)

## [2.1.3]

- Fixed regresssion on --low-quality not working anymore

## [2.1.2]

- Fixed video without sound due to change on Youtube side (#70)

## [2.1.1]

- Using zimscraperlib

## [2.1.0]

- Fixed not working with too much videos (URI too long)
- Secondary color now using 2nd most used color in profile picture
- Display playlists select only if there is multiple playlists
- Added --autoplay option
- Added kiwix-desktop workaround (no status check on XHR)
- Added support for playlists with missing videos
- Added period (YYYY-MM) to filename
- Fixed crash if using subtitles with non-iso language code
- Fixed missing subtitles (non-auto-generated)
- Added --pagination option to set max number of videos per page
- Added subtitles to welcome video as well
- Use (and convert from) `best` format if chosen (mp4|webm) not available
- Fixed colors assignation
- Added --only-test-branding option to generate a fake home page to test branding/colors
- Fixed playlists list for channels not saved to cache
- Removed `chosen` style on playlist select element (back to native)
- Playlists now sorted by title. First playlist remains `Uploads` one though.
- Docker container auto-updates youtube-dl on start
- Added concurrency via --concurrency (defaults to none)
- Fixed date formatting: localized medium-sized version as in Youtube
- Displaying error messages from youtube on API errors
- Fixed API requests for large number of videos in playlist
- Made --name mandatory
- Tags now specified as comma-separated list
- Fixed channel info retrieval in some cases
- Don't fail on non-matching language-to-locale (defaults to EN)
- Added --locale to specify locale to use for translations/dates
- Splitted logs into stdout and stderr
- Failed to download videos don't stop the process. Nb of failed displayed on stderr

## [2.0] 2019-08

- Rewrote scraper script
  - using Youtube API instead of parsing DOM
  - simpler code (less)
  - using youtube-dl to download video, thumbnail, subtitles
  - faster (bundled download for video, thumbnail and subtitles – single ytdl call)
  - option to use auto-generated subtitles
  - added favicon in HTML (for kiwix-serve use)
  - kept FFMPEF options code for lower-quality
  - kept UI: html, css, js.
  - updated videojs
  - added support for webm in all browsers via ogv.js and videosjs-ogvjs
  - defaults to webm
  - made sure video are included only once (even if on multiple playlists)
  - Dockerfile runs current code, not a pypi version
  - improved UI on mobile/responsive
  - translatable UI-texts, using --language (supports EN,FR atm.)
  - fixed audio in low-quality mp4 files on quicktime-based platforms
- Known bugs:
  - --all-subtitles is slow #38
  - Safari (iOS/macOS) via kiwix-serve:
     -  Fullscreen is broken in Safari #33
  - firefox/chromium via kiwix-serve:
     - Controls buggy in firefox/chrome #34
     - Fullscreen-exit is broken in firefox/chrome #35
  - android:
     - No fullscreen support in android #36
     - exit rotation is buggy on android #37
  - iOS:
     - fullscreen is broken on iOS #39
  - macOS:
     - not working on macOS #40
  - desktop (linux/windows):
     - no fullscreen support on kiwix-desktop #42
     - subtitles don't work on kiwix-desktop #41

## [1.1] - 2017-04-04:

- Make it as python package

## [1.0] - 2016-06-23:

- Get playlist or user channel (and playlist of user) from youtube
- the most view video is show on top and bigger
- --lowquality option for downloading in mp4 and re-encode aggressively in webm
