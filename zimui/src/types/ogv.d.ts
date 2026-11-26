declare module 'ogv' {
  export interface OGVTimeRanges {
    readonly length: number
    start(index: number): number
    end(index: number): number
  }

  export class OGVPlayer {
    src: string
    poster: string
    loop: boolean
    autoplay: boolean
    preload: string
    controls: boolean
    currentTime: number
    duration: number
    playbackRate: number
    volume: number
    muted: boolean
    defaultMuted: boolean
    readonly paused: boolean
    readonly ended: boolean
    readonly seeking: boolean
    readonly readyState: number
    readonly networkState: number
    readonly error: unknown
    readonly currentSrc: string
    readonly videoWidth: number
    readonly videoHeight: number
    readonly played: OGVTimeRanges
    readonly buffered: OGVTimeRanges
    readonly seekable: OGVTimeRanges
    play(): Promise<void> | void
    pause(): void
    load(): void
    addEventListener(
      type: string,
      listener: EventListenerOrEventListenerObject,
      options?: AddEventListenerOptions
    ): void
    removeEventListener(type: string, listener: EventListenerOrEventListenerObject): void
  }

  export const OGVCompat: {
    supported(name: string): boolean
  }

  export const OGVLoader: {
    base: string
  }
}
