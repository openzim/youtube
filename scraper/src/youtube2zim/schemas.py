from humps import camelize
from pydantic import BaseModel


class CamelModel(BaseModel):
    """Model to transform Python snake_case into JSON camelCase."""

    class Config:
        alias_generator = camelize
        populate_by_name = True


class Author(CamelModel):
    channel_id: str
    channel_title: str
    channel_description: str
    channel_joined_date: str
    profile_path: str | None = None
    banner_path: str | None = None


class Subtitle(CamelModel):
    """Class to serialize data about a YouTube video subtitle."""

    code: str
    name: str


class Subtitles(CamelModel):
    """Class to serialize data about a list of YouTube video subtitles."""

    subtitles: list[Subtitle]


class Video(CamelModel):
    """Class to serialize data about a YouTube video."""

    id: str
    title: str
    description: str
    author: Author
    publication_date: str
    video_path: str
    thumbnail_path: str | None = None
    subtitle_path: str | None = None
    subtitle_list: list[Subtitle]
    duration: str


class VideoPreview(CamelModel):
    """Class to serialize data about a YouTube video for preview."""

    slug: str
    id: str
    title: str
    thumbnail_path: str | None = None
    duration: str


class Playlist(CamelModel):
    """Class to serialize data about a YouTube playlist."""

    id: str
    author: Author
    title: str
    description: str
    publication_date: str
    thumbnail_path: str | None = None
    videos: list[VideoPreview]
    videos_count: int


class PlaylistPreview(CamelModel):
    """Class to serialize data about a YouTube playlist for preview."""

    slug: str
    id: str
    title: str
    thumbnail_path: str | None = None
    videos_count: int
    main_video_slug: str


class Playlists(CamelModel):
    """Class to serialize data about a list of YouTube playlists."""

    playlists: list[PlaylistPreview]


class Channel(CamelModel):
    """Class to serialize data about a YouTube channel."""

    id: str
    title: str
    description: str
    channel_name: str
    channel_description: str
    profile_path: str | None = None
    banner_path: str | None = None
    joined_date: str
    collection_type: str
    main_playlist: str | None = None
    playlist_count: int


class Config(CamelModel):
    """Class to serialize configuration data for the ZIM UI."""

    main_color: str | None
    secondary_color: str | None
