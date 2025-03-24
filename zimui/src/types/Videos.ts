import type { Author } from './Channel'

export interface Video {
  id: string
  title: string
  description: string
  author: Author
  publicationDate: string
  videoPath: string
  thumbnailPath?: string
  subtitlePath?: string
  subtitleList: Subtitle[]
  chaptersPath?: string
  chapterList: Chapter[]
  duration: string
}

export interface VideoPreview {
  slug: string
  id: string
  title: string
  thumbnailPath?: string
  duration: string
}

export default interface Subtitle {
  code: string
  name: string
}

export interface Chapter {
  startTime: number
  endTime: number
  title: string
}
