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
  count: number
}
export interface PlaylistPreview {
  slug: string
  id: string
  title: string
  thumbnailPath?: string
  count: number
  videoSlug: string
}

export interface Playlists {
  playlists: PlaylistPreview[]
}
