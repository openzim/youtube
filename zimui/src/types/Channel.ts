export interface Channel {
  id: string
  title: string
  description: string
  channelName: string
  channelDescription: string
  profilePath?: string
  bannerPath?: string
  joinedDate: string
  collectionType: string
  mainPlaylist?: string
}

export interface Author {
  channelId: string
  channelTitle: string
  profilePath?: string
  bannerPath?: string
}

export enum CollectionType {
  Playlist = 'playlist',
  Video = 'video',
  Channel = 'channel'
}
