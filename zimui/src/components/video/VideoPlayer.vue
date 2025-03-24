<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, nextTick, type PropType } from 'vue'
import videojs from 'video.js'
import type Player from 'video.js/dist/types/player'

import 'video.js/dist/video-js.css'
import '@/assets/vjs-youtube.css'
import '@/plugins/videojs-ogvjs.js'
import { timeToSeconds } from '@/utils/format-utils'
import type TimeTooltip from '@/types/videojs'

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
    type: Array as PropType<{ startTime: number; endTime: number; title: string }[]>,
    default: () => []
  }
})

const videoContainer = ref<HTMLVideoElement>()
const player = ref<Player>()
const chapterList = ref<{ startTime: number; endTime: number; title: string }[]>([])

const emit = defineEmits(['video-ended'])

const addMarkers = () => {
  if (player.value) {
    const progressBar = player.value
      ?.getChild('controlBar')
      ?.getChild('progressControl')
      ?.getChild('seekBar')
      ?.el()

    if (!progressBar) return
    const duration = player.value?.duration()
    if (!duration) return

    progressBar.querySelectorAll('.custom-marker').forEach((el) => el.remove())

    chapterList.value.forEach((marker) => {
      const markerEl = document.createElement('div')
      markerEl.classList.add('custom-marker')
      if (marker.startTime < 0 || marker.startTime > duration) return
      markerEl.style.left = `${(marker.startTime / duration) * 100}%`
      progressBar.appendChild(markerEl)
    })
  }
}

const getChapterAtTime = (timestr: string) => {
  const inputSeconds = timeToSeconds(timestr)

  for (const chapter of chapterList.value) {
    if (chapter.startTime <= inputSeconds && chapter.endTime > inputSeconds) {
      return chapter.title
    }
  }

  return null
}

const initPlayer = () => {
  if (!videoContainer.value) return

  // Remove existing video element if present
  videoContainer.value.innerHTML = ''

  // Create a new video element dynamically
  const videoElement = document.createElement('video')
  videoElement.className = 'video-js vjs-youtube'
  videoElement.setAttribute('playsinline', '')
  videoElement.setAttribute('controls', props.options.controls ? 'true' : 'false')
  videoElement.setAttribute('preload', props.options.preload)
  videoElement.setAttribute('autoplay', props.options.autoplay ? 'true' : 'false')
  if (props.options.poster) {
    videoElement.setAttribute('poster', props.options.poster)
  }

  // Append sources dynamically
  props.options.sources.forEach((source: Record<string, string>) => {
    const sourceElement = document.createElement('source')
    sourceElement.src = source.src
    sourceElement.type = source.type
    videoElement.appendChild(sourceElement)
  })

  // Append the new video element to the container
  videoContainer.value.appendChild(videoElement)

  // Initialize Video.js on the new video element
  nextTick(() => {
    player.value = videojs(videoElement, props.options)
    player.value.loop(props.options.loop)
    player.value.on('ended', () => {
      emit('video-ended')
    })
    if (props.chaptersList) {
      chapterList.value = props.chaptersList
    }

    player.value?.on('loadedmetadata', () => {
      addMarkers()
      nextTick(() => {
        updateChapterTimeTooltip()
      })
    })
  })
}

const updateChapterTimeTooltip = () => {
  if (player.value) {
    const timeTooltip = player.value
      ?.getChild('controlBar')
      ?.getChild('progressControl')
      ?.getChild('seekBar')
      ?.getChild('mouseTimeDisplay')
      ?.getChild('timeTooltip') as TimeTooltip

    if (!timeTooltip) return

    timeTooltip.update = function (seekBarRect: DOMRect, seekBarPoint: number, time: string) {
      const chapter = getChapterAtTime(time)
      if (chapter) {
        this.write(`${chapter.replace(/ /g, '\u00A0')}\n${time}`)
        return
      }
      this.write(`${time}`)
    }
  }
}

// Initialize video.js when the component is mounted
onMounted(() => {
  initPlayer()
})

// Watch for changes in the options prop
watch(
  () => props.options,
  () => {
    if (player.value) {
      player.value.dispose()
      initPlayer()
    }
  },
  { deep: true }
)

watch(
  () => props.chaptersList,
  (newList) => {
    chapterList.value = newList
    nextTick(() => {
      addMarkers()
      updateChapterTimeTooltip()
    })
  },
  { deep: true }
)

// Watch for changes in the loop prop
watch(
  () => props.loop,
  (newLoop) => {
    if (player.value) {
      player.value.loop(newLoop)
    }
  }
)

// Destroy video.js when the component is unmounted
onBeforeUnmount(() => {
  if (player.value) {
    player.value.dispose()
  }
})
</script>

<template>
  <div ref="videoContainer"></div>
</template>
