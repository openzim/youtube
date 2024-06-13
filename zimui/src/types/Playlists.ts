import type { Author } from './Channel'
import type { VideoPreview } from './Videos'

export interface Playlist {
  id: string
  author: Author
  title: string
  description: string
  publicationDate: string
  thumbnailPath?: string
  videos: VideoPreview[]
  videosCount: number
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
