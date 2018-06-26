from setuptools import setup, find_packages
from pip._internal.req import parse_requirements

setup(
    name='youtube2zim',
    version='1.2.7',
    description="Make zimfile from youtube channel or playlist",
    long_description=open('README.md').read(),
    author='dattaz',
    author_email='taz@dattaz.fr',
    url='http://github.com/kiwix/youtube',
    keywords="kiwix zim youtube offline",
    license="TODO",
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
       'youtube-dl',
       'requests',
       'jinja2',
       'pillow',
       'envoy',
       'beautifulsoup4',
       'cssutils',
       'awesome-slugify',
       'docopt'
        ],
    zip_safe=False,
    platforms='Linux',
    include_package_data=True,
    entry_points={
            'console_scripts': ['youtube2zim=youtube.youtube2zim:run'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ],
)
