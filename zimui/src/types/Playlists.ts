import type { Author } from './Channel'
import type { VideoPreview } from './Videos'

export interface Playlist {
  id: string
  slug: string
  author: Author
  title: string
  description: string
  publicationDate: string
  thumbnailPath?: string
  videos: VideoPreview[]
  videosCount: number
  duration: string
}
export interface PlaylistPreview {
  slug: string
  id: string
  title: string
  thumbnailPath?: string
  videosCount: number
  mainVideoSlug: string
}

export interface Playlists {
  playlists: PlaylistPreview[]
}

export interface HomePlaylists {
  playlists: Playlist[]
}

export enum LoopOptions {
  off = 'off',
  loopVideo = 'loop-video',
  loopPlaylist = 'loop-playlist'
}
