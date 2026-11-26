<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch, type PropType } from 'vue'

import '@videojs/html/video/player'
import '@videojs/html/video/skin'
import '@/plugins/ogvjs-video'
import { canPlayNatively } from '@/plugins/ogvjs-video'
import '@/assets/vjs-youtube.css'
import { useMainStore } from '@/stores/main'
import type { Chapter } from '@/types/Videos'

type SeekableMedia = {
  currentTime: number
  duration: number
}

type Track = {
  kind: string
  src: string
  srclang: string
  label: string
  default?: boolean
}

const props = defineProps({
  options: {
    type: Object,
    default: () => ({})
  },
  loop: {
    type: Boolean,
    default: false
  },
  chaptersList: {
    type: Array as PropType<Chapter[]>,
    default: () => []
  }
})

const emit = defineEmits(['video-ended', 'next-video', 'prev-video'])

const main = useMainStore()
const mediaEl = ref<HTMLElement>()
const chapterList = ref<Chapter[]>([...props.chaptersList])
const isShortcutsPopupVisible = ref(false)
const chapterIndicator = ref('')

const source = computed<string>(() => props.options.sources?.[0]?.src ?? '')
const sourceType = computed<string>(() => props.options.sources?.[0]?.type ?? '')
const poster = computed<string>(() => props.options.poster ?? '')
const autoplay = computed<boolean>(() => Boolean(props.options.autoplay))
const preload = computed<string>(() => {
  const value = props.options.preload
  if (value === true || value === 'auto') return 'auto'
  if (value === 'metadata') return 'metadata'
  if (value === false || value === 'none') return 'none'
  return 'metadata'
})
const playbackRates = computed<string>(() =>
  (props.options.playbackRates ?? [0.25, 0.5, 1, 1.5, 2])
    .map((rate: number) => String(rate))
    .join(' ')
)
const tracks = computed<Track[]>(() => props.options.tracks ?? [])
const useNativeVideo = computed(() => canPlayNatively(sourceType.value))

const media = () => mediaEl.value as unknown as SeekableMedia | undefined

let indicatorTimer: ReturnType<typeof setTimeout> | null = null
const showChapter = (title: string) => {
  chapterIndicator.value = title
  if (indicatorTimer) clearTimeout(indicatorTimer)
  indicatorTimer = setTimeout(() => {
    chapterIndicator.value = ''
  }, 500)
}

const goToNextChapter = () => {
  const current = media()
  if (!current) return
  const chapter = chapterList.value.find((item) => item.startTime > current.currentTime)
  if (!chapter) return
  current.currentTime = chapter.startTime
  showChapter(chapter.title)
}

const goToPrevChapter = () => {
  const current = media()
  if (!current) return
  let previous: Chapter | undefined
  for (const chapter of chapterList.value) {
    if (chapter.startTime > current.currentTime) break
    if (chapter.endTime <= current.currentTime) previous = chapter
  }
  if (!previous) return
  current.currentTime = previous.startTime
  showChapter(previous.title)
}

const toggleTheaterMode = () => {
  main.theaterMode = !main.theaterMode
}

const toggleShortcuts = () => {
  isShortcutsPopupVisible.value = !isShortcutsPopupVisible.value
}

// Video.js 10's packaged skin already handles Space/k/m/j/l/arrows/f/>/<,
// volume steps, touch gestures and the built-in indicators. Only keep the
// shortcuts that are specific to this application.
const handleKeydown = (event: KeyboardEvent) => {
  if (event.shiftKey && event.key === '?') {
    event.preventDefault()
    toggleShortcuts()
  } else if (event.shiftKey && (event.key === 'n' || event.key === 'N')) {
    event.preventDefault()
    emit('next-video')
  } else if (event.shiftKey && (event.key === 'p' || event.key === 'P')) {
    event.preventDefault()
    emit('prev-video')
  } else if (event.shiftKey && event.key === 'ArrowLeft') {
    event.preventDefault()
    goToPrevChapter()
  } else if (event.shiftKey && event.key === 'ArrowRight') {
    event.preventDefault()
    goToNextChapter()
  } else if (!event.shiftKey && (event.key === 't' || event.key === 'T')) {
    event.preventDefault()
    toggleTheaterMode()
  }
}

const onEnded = () => {
  emit('video-ended')
}

watch(
  () => props.chaptersList,
  (newList) => {
    chapterList.value = [...newList]
  },
  { deep: true }
)

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleKeydown)
  if (indicatorTimer) clearTimeout(indicatorTimer)
})
</script>

<template>
  <div class="video-player-container">
    <video-player :key="source" :default-playback-rates="playbackRates">
      <video-skin>
        <video
          v-if="useNativeVideo"
          ref="mediaEl"
          :src="source"
          :poster="poster"
          :loop="loop"
          :autoplay="autoplay"
          :preload="preload"
          playsinline
          @ended="onEnded"
        >
          <track
            v-for="track in tracks"
            :key="`${track.kind}-${track.src}`"
            :kind="track.kind"
            :src="track.src"
            :srclang="track.srclang"
            :label="track.label"
            :default="track.default"
          />
        </video>
        <ogvjs-video
          v-else
          ref="mediaEl"
          :src="source"
          :poster="poster"
          :loop="loop"
          :autoplay="autoplay"
          :preload="preload"
          @ended="onEnded"
        />
      </video-skin>
    </video-player>

    <!-- Kept outside <video-skin>: its shadow-DOM content paints over slotted
         children, so controls placed inside it cannot be clicked. -->
    <button
      type="button"
      class="theater-toggle-button"
      aria-label="Toggle theater mode"
      @click="toggleTheaterMode"
    >
      <i class="mdi mdi-rectangle-outline" />
    </button>
    <button
      type="button"
      class="shortcuts-popup-button"
      aria-label="Show keyboard shortcuts"
      @click="toggleShortcuts"
    >
      <i class="mdi mdi-keyboard" />
    </button>
    <div v-if="chapterIndicator" class="custom-video-indicator show">
      {{ chapterIndicator }}
    </div>

    <teleport to="body">
      <div
        v-if="isShortcutsPopupVisible"
        class="popup-overlay show"
        @click="isShortcutsPopupVisible = false"
      >
        <div class="table-wraper" @click.stop>
          <table>
            <thead>
              <tr>
                <th>Key(s)</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Shift + n</td>
                <td>Next video</td>
              </tr>
              <tr>
                <td>Shift + p</td>
                <td>Previous video</td>
              </tr>
              <tr>
                <td>Arrow Left</td>
                <td>Skip -5s</td>
              </tr>
              <tr>
                <td>shift + Arrow Left</td>
                <td>Go to previous chapter</td>
              </tr>
              <tr>
                <td>Arrow Right</td>
                <td>Skip +5s</td>
              </tr>
              <tr>
                <td>shift + Arrow Right</td>
                <td>Go to next chapter</td>
              </tr>
              <tr>
                <td>Arrow Up</td>
                <td>Increase volume</td>
              </tr>
              <tr>
                <td>Arrow Down</td>
                <td>Decrease volume</td>
              </tr>
              <tr>
                <td>Space</td>
                <td>Play/Pause</td>
              </tr>
              <tr>
                <td>f</td>
                <td>Toggle fullscreen</td>
              </tr>
              <tr>
                <td>t</td>
                <td>Toggle theater mode</td>
              </tr>
              <tr>
                <td>m</td>
                <td>Toggle mute</td>
              </tr>
              <tr>
                <td>j</td>
                <td>Skip -10s</td>
              </tr>
              <tr>
                <td>k</td>
                <td>Play/Pause</td>
              </tr>
              <tr>
                <td>l</td>
                <td>Skip +10s</td>
              </tr>
              <tr>
                <td>&gt;</td>
                <td>Increase playback speed</td>
              </tr>
              <tr>
                <td>&lt;</td>
                <td>Decrease playback speed</td>
              </tr>
              <tr>
                <td>Shift + ?</td>
                <td>Show shortcuts</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </teleport>
  </div>
</template>

<style scoped>
:deep(.popup-overlay .table-wraper) {
  background-color: rgb(var(--v-theme-surface));
  color: rgb(var(--v-theme-on-surface));
}

:deep(.popup-overlay table th) {
  color: rgb(var(--v-theme-on-surface));
}

@media (prefers-color-scheme: dark) {
  :deep(.popup-overlay) {
    background-color: rgba(0, 0, 0, 0.7);
  }
}
</style>
