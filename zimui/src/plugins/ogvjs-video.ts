/**
 * ogv.js media component for Video.js 10.
 *
 * Video.js 8 used a custom `Tech` plugin (src/plugins/videojs-ogvjs.js) for WebM
 * fallback on browsers without native WebM support. Video.js 10 replaced techs
 * with media components, so the fallback is now a custom element that exposes
 * the subset of the HTMLMediaElement API used by the player features.
 */
import { MediaAttachMixin } from '@videojs/html'
import { OGVCompat, OGVLoader, OGVPlayer } from 'ogv'

const OGV_BASE = './assets/ogvjs'

const MEDIA_EVENTS = [
  'loadstart',
  'suspend',
  'abort',
  'error',
  'emptied',
  'stalled',
  'loadedmetadata',
  'loadeddata',
  'canplay',
  'canplaythrough',
  'playing',
  'waiting',
  'seeking',
  'seeked',
  'ended',
  'durationchange',
  'timeupdate',
  'progress',
  'play',
  'pause',
  'ratechange',
  'resize',
  'volumechange'
] as const

// The ogv.js distribution ships without type declarations.
type OgvPlayer = {
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
  paused: boolean
  ended: boolean
  seeking: boolean
  readyState: number
  networkState: number
  error: unknown
  currentSrc: string
  videoWidth: number
  videoHeight: number
  played: TimeRanges
  buffered: TimeRanges
  seekable: TimeRanges
  play: () => Promise<void> | void
  pause: () => void
  load: () => void
  canPlayType?: (type: string) => string
  addEventListener: (
    type: string,
    listener: EventListenerOrEventListenerObject,
    options?: AddEventListenerOptions
  ) => void
  removeEventListener: (type: string, listener: EventListenerOrEventListenerObject) => void
}

type OgvConstructor = new (options?: Record<string, unknown>) => OgvPlayer

const ogv = { OGVCompat, OGVLoader, OGVPlayer } as unknown as {
  OGVCompat: { supported: (name: string) => boolean }
  OGVLoader: { base: string }
  OGVPlayer: OgvConstructor
}

/** Whether ogv.js can run in this browser. */
export const isOgvJSSupported = () => ogv.OGVCompat.supported('OGVPlayer')

/** Whether the browser can play the source natively. */
export const canPlayNatively = (type: string) => {
  if (!type) return false
  const probe = document.createElement('video')
  return probe.canPlayType(type) !== ''
}

const MediaAttachBase = MediaAttachMixin(HTMLElement) as new () => HTMLElement & {
  connectedCallback(): void
  disconnectedCallback(): void
}

class OgvJSVideoElement extends MediaAttachBase {
  static get observedAttributes() {
    return ['src', 'poster', 'loop', 'autoplay', 'preload', 'muted', 'playback-rate']
  }

  readonly #player: OgvPlayer

  constructor() {
    super()
    ogv.OGVLoader.base = OGV_BASE
    this.#player = new ogv.OGVPlayer()
    const shadow = this.attachShadow({ mode: 'open' })
    const style = document.createElement('style')
    style.textContent = `
      :host { display: block; width: 100%; height: 100%; }
      :host > * { width: 100%; height: 100%; }
      canvas { width: 100% !important; height: 100% !important; object-fit: contain; }
    `
    shadow.append(style, this.#player as unknown as Node)
    for (const type of MEDIA_EVENTS) {
      this.#player.addEventListener(type, () => {
        this.dispatchEvent(new Event(type, { bubbles: true, composed: true }))
      })
    }
  }

  connectedCallback() {
    super.connectedCallback()
    if (this.hasAttribute('src')) this.#player.src = this.getAttribute('src') ?? ''
    if (this.hasAttribute('poster')) this.#player.poster = this.getAttribute('poster') ?? ''
    if (this.hasAttribute('preload')) this.#player.preload = this.getAttribute('preload') ?? ''
    this.#player.loop = this.hasAttribute('loop')
    this.#player.autoplay = this.hasAttribute('autoplay')
    this.#player.muted = this.hasAttribute('muted')
    if (this.hasAttribute('playback-rate')) {
      this.#player.playbackRate = Number(this.getAttribute('playback-rate')) || 1
    }
  }

  disconnectedCallback() {
    this.#player.pause()
    super.disconnectedCallback()
  }

  attributeChangedCallback(name: string, _oldValue: string | null, newValue: string | null) {
    switch (name) {
      case 'src':
        this.#player.src = newValue ?? ''
        break
      case 'poster':
        this.#player.poster = newValue ?? ''
        break
      case 'preload':
        this.#player.preload = newValue ?? ''
        break
      case 'loop':
        this.#player.loop = newValue !== null
        break
      case 'autoplay':
        this.#player.autoplay = newValue !== null
        break
      case 'muted':
        this.#player.muted = newValue !== null
        break
      case 'playback-rate':
        this.#player.playbackRate = Number(newValue) || 1
        break
    }
  }

  get adapter() {
    return this.#player
  }

  get src() {
    return this.#player.src
  }

  set src(value: string) {
    this.#player.src = value
  }

  get currentSrc() {
    return this.#player.currentSrc
  }

  get poster() {
    return this.#player.poster
  }

  set poster(value: string) {
    this.#player.poster = value
  }

  get preload() {
    return this.#player.preload
  }

  set preload(value: string) {
    this.#player.preload = value
  }

  get loop() {
    return this.#player.loop
  }

  set loop(value: boolean) {
    this.#player.loop = value
  }

  get autoplay() {
    return this.#player.autoplay
  }

  set autoplay(value: boolean) {
    this.#player.autoplay = value
  }

  get controls() {
    return this.#player.controls
  }

  set controls(value: boolean) {
    this.#player.controls = value
  }

  get currentTime() {
    return this.#player.currentTime
  }

  set currentTime(value: number) {
    try {
      this.#player.currentTime = value
    } catch {
      // ogv.js throws while the media is still loading; keep the last position.
    }
  }

  get duration() {
    return Number.isFinite(this.#player.duration) ? this.#player.duration : 0
  }

  get seeking() {
    return this.#player.seeking
  }

  get paused() {
    return this.#player.paused
  }

  get ended() {
    return this.#player.ended
  }

  get volume() {
    return this.#player.volume
  }

  set volume(value: number) {
    this.#player.volume = value
  }

  get muted() {
    return this.#player.muted
  }

  set muted(value: boolean) {
    this.#player.muted = value
  }

  get defaultMuted() {
    return this.#player.defaultMuted
  }

  get playbackRate() {
    return this.#player.playbackRate || 1
  }

  set playbackRate(value: number) {
    this.#player.playbackRate = value
  }

  get played() {
    return this.#player.played
  }

  get buffered() {
    return this.#player.buffered
  }

  get seekable() {
    return this.#player.seekable
  }

  get readyState() {
    return this.#player.readyState
  }

  get networkState() {
    return this.#player.networkState
  }

  get error() {
    return this.#player.error
  }

  get videoWidth() {
    return this.#player.videoWidth
  }

  get videoHeight() {
    return this.#player.videoHeight
  }

  play() {
    return Promise.resolve(this.#player.play())
  }

  pause() {
    this.#player.pause()
  }

  load() {
    this.#player.load()
  }

  canPlayType(type: string) {
    const result = this.#player.canPlayType?.(type)
    if (result) return result
    return ogv.OGVCompat.supported('OGVPlayer') ? 'maybe' : ''
  }
}

if (!customElements.get('ogvjs-video')) {
  customElements.define('ogvjs-video', OgvJSVideoElement)
}

declare global {
  interface HTMLElementTagNameMap {
    'ogvjs-video': OgvJSVideoElement
  }
}

export { OgvJSVideoElement }
