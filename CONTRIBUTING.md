# youtube2zim devel


## setup

See [README](README.md) for details about how to install with hatch virtualenv.

## contributions

* Open issues, bug reports and send PRs [on github](https://github.com/openzim/youtube).
* Make sure it's `py3.6+` compatible.
* Use [black](https://github.com/psf/black) code formatting.

## notes

In order to support all platform, we default to `webm` video format. `mp4` one (h264), is not available in Webview on most platform due to patent restrictions.

On the other hand, `webm` is not supported in Safari (macOS, iOS).

We thus use `ogv.js`, to play webm videos on browsers that don't support it. Using `video.js`, we default to native playback if supported.

`ogv.js` is an emscripten-based JS decoder for webm and thus dynamically loads differents parts at run-time on platforms that needs them. It has two consequences:

* `file://` scheme doesn't work as the binary `.wasm` files are sent naively as `text/html` instead of `application/oct-stream`. If you want to use the HTML generated folder instead of ZIM, serve it through a web server and [configure the Content-Type response](https://emscripten.org/docs/compiling/WebAssembly.html#web-server-setup).
* [ZIM](https://wiki.openzim.org/wiki/ZIM_file_format) places JS files under the `/-/` namespace and binary ones under the `/I/` one. Dynamically loading of JS and WASM files within `ogv.js` requires us to tweak it to introduce some ZIM-specific logic. See `fix_ogvjs_dist.py`.

Because the pagination system is implemented in JS, we also need to generate links there. For that to work both in static HTML and in-ZIM, we detect it using a `<link id="favicon">` in HTML files. This link needs to be present and parsed before loading the help `zim_prefix.js` script.

## i18n

`youtube2zim` has very minimal non-content text but still uses gettext through [babel]() to internationalize.

To add a new locale (`fr` in this example, use only ISO-639-1):

1. init for your locale: `pybabel init -d locale -l fr`
2. make sure the POT is up to date `pybabel extract -o youtube2zim/locale/messages.pot youtube2zim`
3. update your locale's catalog `pybabel update -d youtube2zim/locale/ -l fr -i youtube2zim/locale/messages.pot`
3. translate the PO file ([poedit](https://poedit.net/) is your friend)
4. compile updated translation `pybabel compile -d youtube2zim/locale -l fr`

## releasing

* Update your dependencies: `pip install -U setuptools wheel twine`
* Make sure CHANGELOG is up-to-date
* Bump version on `youtube2zim/VERSION`
* Build packages `python ./setup.py sdist bdist_wheel`
* Upload to PyPI `twine upload dist/youtube2zim-2.0.0*`.
* Commit your CHANGELOG + version bump changes
* Tag version on git `git tag -a v2.0.0`
