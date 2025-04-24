<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, nextTick, type PropType } from 'vue'
import videojs from 'video.js'
import type Player from 'video.js/dist/types/player'

import 'video.js/dist/video-js.css'
import '@/assets/vjs-youtube.css'
import '@/plugins/videojs-ogvjs.js'
import { timeToSeconds } from '@/utils/format-utils'
import type TimeTooltip from '@/types/videojs'
import { useMainStore } from '@/stores/main'

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
const isControlBarVisible = ref(false)
const isShortcutsPopupVisible = ref(false)
const main = useMainStore()

const Button = videojs.getComponent('Button')

const TheaterToggleButton = class extends Button {
  constructor(player: Player) {
    super(player)
    this.el().querySelector('.vjs-icon-placeholder')?.classList.add('mdi','mdi-rectangle-outline')
    this.on('click', toggleTheaterMode)
  }
};

const emit = defineEmits(['video-ended', 'next-video', 'prev-video'])

const addTheaterBtn = () => {
  if (player.value) {
    videojs.registerComponent('TheaterToggleButton', TheaterToggleButton);
    const controlBar = player.value.getChild('controlBar')
    const index = controlBar?.children().findIndex((item) => item.name() === 'FullscreenToggle')
    controlBar?.addChild('TheaterToggleButton', {}, index ? index - 1 : -1)
  }
}

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

const appendShortCutsPopupBtn = () => {
  if (!player.value) return
  const videoElement = player.value.el()

  if (!videoElement) return

  const btn = document.createElement('div')
  btn.classList.add('shortCutsPopupBtn')

  btn.innerHTML = '<i class="mdi mdi-keyboard"></i>'

  btn.onclick = () => {
    isShortcutsPopupVisible.value = true
  }

  videoElement.append(btn)
}

const appendShortCutsPopup = () => {
  if (!player.value) return
  const videoElement = player.value.el()

  if (!videoElement) return

  const popup = document.createElement('div')
  popup.classList.add('popup-overlay')

  popup.innerHTML = `
  <div class="table-wraper">
    <table>
      <thead>
        <tr>
          <th>Key(s)</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Shift + n</td><td>Next video</td></tr>
        <tr><td>Shift + p</td><td>Previous video</td></tr>
        <tr><td>Arrow Left</td><td>Skip -5s</td></tr>
        <tr><td>shift + Arrow Left</td><td>Go to previous chapter</td></tr>
        <tr><td>Arrow Right</td><td>Skip +5s</td></tr>
        <tr><td>shift + Arrow Right</td><td>Go to next chapter</td></tr>
        <tr><td>Arrow Up</td><td>Increase volume</td></tr>
        <tr><td>Arrow Down</td><td>Decrease volume</td></tr>
        <tr><td>Space</td><td>Play/Pause</td></tr>
        <tr><td>f</td><td>Toggle fullscreen</td></tr>
        <tr><td>t</td><td>Toggle theater mode</td></tr>
        <tr><td>m</td><td>Toggle mute</td></tr>
        <tr><td>j</td><td>Skip -10s</td></tr>
        <tr><td>k</td><td>Play/Pause</td></tr>
        <tr><td>l</td><td>Skip +10s</td></tr>
        <tr><td>></td><td>Increase playback speed</td></tr>
        <tr><td><</td><td>Decrease playback speed</td></tr>
        <tr><td>Shift + ?</td><td>Show shortcuts</td></tr>
      </tbody>
    </table>
  </div>
  `
  popup.onclick = () => {
    isShortcutsPopupVisible.value = false
  }
  popup.querySelector('.table-wraper')?.addEventListener('click', (e) => {
    e.stopPropagation()
  })

  videoElement.append(popup)
}

const appendSkipIndicator = () => {
  if (!player.value) return
  const videoElement = player.value.el()

  if (!videoElement) return

  const forwardSkipEl = document.createElement('div')
  const backwardSkipEl = document.createElement('div')

  forwardSkipEl.classList.add('custom-video-indicator', 'skip-indicator', 'forward')
  forwardSkipEl.innerHTML = '+5 seconds'
  backwardSkipEl.classList.add('custom-video-indicator', 'skip-indicator', 'backward')
  backwardSkipEl.innerHTML = '-5 seconds'

  videoElement.append(forwardSkipEl)
  videoElement.append(backwardSkipEl)
}

const appendVolumeIndicator = () => {
  if (!player.value) return
  const videoElement = player.value.el()

  if (!videoElement) return

  const volumeEl = document.createElement('div')

  volumeEl.classList.add('custom-video-indicator', 'volume-indicator')
  volumeEl.innerHTML = '50%'

  videoElement.append(volumeEl)
}

const appendChapterIndicator = () => {
  if (!player.value) return
  const videoElement = player.value.el()

  if (!videoElement) return

  const chapterEl = document.createElement('div')

  chapterEl.classList.add('custom-video-indicator', 'chapter-indicator')
  chapterEl.innerHTML = '<span>chapter</span>'

  videoElement.append(chapterEl)
}

const appendPlaybackRateIndicator = () => {
  if (!player.value) return
  const videoElement = player.value.el()

  if (!videoElement) return

  const chapterEl = document.createElement('div')

  chapterEl.classList.add('custom-video-indicator', 'playback-rate-indicator')
  chapterEl.innerHTML = '<span>1x</span>'

  videoElement.append(chapterEl)
}

const displayChapterIndicator = (chapterTitle: string) => {
  if (!player.value) return
  const videoElement = player.value?.el()

  const targetElement = videoElement?.querySelector('.custom-video-indicator.chapter-indicator')
  if (!targetElement) return

  targetElement.innerHTML = `<span>${chapterTitle}</span>`

  targetElement?.classList.add('show')
  setTimeout(() => {
    targetElement?.classList.remove('show')
  }, 0.5 * 1000)
}

const displayPlaybackRateIndicator = (rate: number) => {
  if (!player.value) return
  const videoElement = player.value?.el()

  const targetElement = videoElement?.querySelector(
    '.custom-video-indicator.playback-rate-indicator'
  )
  if (!targetElement) return

  targetElement.innerHTML = `<span>${rate}x</span>`

  targetElement?.classList.add('show')
  setTimeout(() => {
    targetElement?.classList.remove('show')
  }, 0.5 * 1000)
}

const displayVolumeIndicator = (volume?: number) => {
  if (!player.value) return
  const videoElement = player.value?.el()

  const targetElement = videoElement?.querySelector('.custom-video-indicator.volume-indicator')
  if (!targetElement) return

  const newVolume = player.value.volume()
  if (newVolume === undefined) return
  let volumePercent = Math.round(newVolume * 100)
  if (volume) {
    volumePercent = Math.floor(volume)
  }

  targetElement.innerHTML = `<span>${volumePercent}%</span><span class="text">volume</span>`

  targetElement?.classList.add('show')
  setTimeout(() => {
    targetElement?.classList.remove('show')
  }, 0.5 * 1000)
}

const displaySkipIndicator = (skipTime: number) => {
  if (!player.value) return
  const videoElement = player.value?.el()

  let targetElement: HTMLElement | null = null
  let timeWithdirection: string = `${skipTime}`

  if (skipTime > 0) {
    targetElement = videoElement?.querySelector('.custom-video-indicator.skip-indicator.forward')
    timeWithdirection = `+${skipTime}`
  } else if (skipTime < 0) {
    targetElement = videoElement?.querySelector('.custom-video-indicator.skip-indicator.backward')
  }

  if (!targetElement) return

  targetElement.innerHTML = `${timeWithdirection} seconds`
  targetElement?.classList.add('show')
  setTimeout(() => {
    targetElement?.classList.remove('show')
  }, 0.5 * 1000)
}

const goToNextChapter = () => {
  if (!player.value) return

  const currentTime = player.value.currentTime()
  if (currentTime === undefined) return

  for (const chapter of chapterList.value) {
    if (chapter.startTime > currentTime) {
      player.value.currentTime(chapter.startTime)
      displayChapterIndicator(chapter.title)
      return
    }
  }
}

const goToPrevChapter = () => {
  if (!player.value) return

  const currentTime = player.value.currentTime()
  if (currentTime === undefined) return

  let prevChapter
  for (const chapter of chapterList.value) {
    if (chapter.startTime > currentTime) {
      break
    }
    if (chapter.endTime <= currentTime) {
      prevChapter = chapter
    }
  }

  if (!prevChapter) return
  player.value.currentTime(prevChapter.startTime)
  displayChapterIndicator(prevChapter.title)
}

const changePlaybackRate = (direction: number) => {
  if (!player.value) return
  const currentRate = player.value.playbackRate()
  if (!currentRate) return

  if (direction < 0) {
    if (currentRate <= 0.25) {
      displayPlaybackRateIndicator(0.25)
      return
    }

    const willChange = currentRate === 0.5 ? 0.25 : 0.5

    player.value.playbackRate(currentRate - willChange)
    displayPlaybackRateIndicator(currentRate - willChange)
  } else if (direction > 0) {
    if (currentRate >= 2) {
      displayPlaybackRateIndicator(2)
      return
    }

    const willChange = currentRate === 0.25 ? 0.25 : 0.5

    player.value.playbackRate(currentRate + willChange)
    displayPlaybackRateIndicator(currentRate + willChange)
  }
}

const togglePause = () => {
  if (player.value) {
    player.value.paused() ? player.value.play() : player.value.pause()
  }
}

const toggleFullScreen = () => {
  if (player.value) {
    player.value.isFullscreen() ? player.value.exitFullscreen() : player.value.requestFullscreen()
  }
}

const toggleTheaterMode = () => {
  main.theaterMode = !main.theaterMode
}

const toggleMute = () => {
  if (!player.value) return
  const volume = player.value.volume()

  if (volume != undefined && volume <= 0) {
    const newVolume = Number((0.1).toFixed(2))
    player.value.volume(newVolume)
    return
  }

  player.value.muted(!player.value.muted())
}

const changeVolume = (direction: number) => {
  if (!player.value) return
  let newVolume = player.value.volume()
  if (newVolume === undefined) {
    newVolume = 0
  }
  if (direction < 0) {
    if (player.value.muted()) return
    if (!(newVolume <= 0)) {
      newVolume = Number((newVolume - 0.1).toFixed(2))
    }
  } else if (direction > 0) {
    if (!(newVolume >= 1)) {
      newVolume = Number((newVolume + 0.1).toFixed(2))
    }
    if (player.value.muted()) {
      player.value.muted(false)
      newVolume = Number((0.1).toFixed(2))
    }
  }
  player.value.volume(newVolume)
  displayVolumeIndicator()
}

const skip = (value: number) => {
  if (!player.value) return
  const currentTime = player.value.currentTime()

  let skipTime
  if (value < 0) {
    skipTime = currentTime !== undefined ? currentTime + value : null

    if (!skipTime || skipTime <= 0) {
      player.value.currentTime(0)
      displaySkipIndicator(value)
      return
    }

    displaySkipIndicator(value)
  } else if (value > 0) {
    const duration = player.value.duration()
    skipTime = currentTime !== undefined ? currentTime + value : null

    if (!skipTime || !duration) return
    if (duration < skipTime) {
      player.value.currentTime(duration)
      displaySkipIndicator(value)
      return
    }
  }

  if (!skipTime) return
  displaySkipIndicator(value)
  player.value.currentTime(skipTime)
}

let tappedOnVideoElement: ReturnType<typeof setTimeout> | null = null
const handleTouch = (e: TouchEvent) => {
  if (!player.value) return

  if (!tappedOnVideoElement) {
    tappedOnVideoElement = setTimeout(() => {
      tappedOnVideoElement = null
      player.value?.hasStarted_ || player.value?.play()
    }, 300)
  } else {
    clearTimeout(tappedOnVideoElement)
    tappedOnVideoElement = null

    const videoElement = player.value.el()
    if (!videoElement) return

    const touch = e.touches[0]
    const clickX = touch.clientX - videoElement.getBoundingClientRect().left
    const middle = videoElement.clientWidth / 2

    if (clickX < middle) {
      skip(-10)
    } else {
      skip(10)
    }
  }
}

const updateControlBarState = () => {
  if (player.value) {
    isControlBarVisible.value =
      player.value?.el()?.classList.contains('vjs-user-active') || player.value?.paused()
        ? true
        : false
    const videoElement = player.value.el()

    const targetElement = videoElement?.querySelector('.shortCutsPopupBtn')
    if (!targetElement) return

    if (isControlBarVisible.value) {
      targetElement?.classList.add('show')
    } else if (!isControlBarVisible.value) {
      targetElement?.classList.remove('show')
    }
  }
}

const keyActions: Record<string, (e: KeyboardEvent) => void> = {
  '?': (e: KeyboardEvent) => {
    if (e.shiftKey) {
      isShortcutsPopupVisible.value
        ? (isShortcutsPopupVisible.value = false)
        : (isShortcutsPopupVisible.value = true)
    }
  },

  n: (e: KeyboardEvent) => e.shiftKey && emit('next-video'),
  N: (e: KeyboardEvent) => e.shiftKey && emit('next-video'),
  p: (e: KeyboardEvent) => e.shiftKey && emit('prev-video'),
  P: (e: KeyboardEvent) => e.shiftKey && emit('prev-video'),

  ArrowLeft: (e: KeyboardEvent) => (e.shiftKey ? goToPrevChapter() : skip(-5)),
  ArrowRight: (e: KeyboardEvent) => (e.shiftKey ? goToNextChapter() : skip(5)),
  j: () => skip(-10),
  J: () => skip(-10),
  l: () => skip(10),
  L: () => skip(10),

  ArrowUp: () => changeVolume(+1),
  ArrowDown: () => changeVolume(-1),

  ' ': () => togglePause(),
  k: () => togglePause(),
  K: () => togglePause(),

  f: () => toggleFullScreen(),
  F: () => toggleFullScreen(),

  t: () => toggleTheaterMode(),
  T: () => toggleTheaterMode(),

  m: () => toggleMute(),
  M: () => toggleMute(),

  '>': () => changePlaybackRate(1),
  '<': () => changePlaybackRate(-1)
}

const handleKeydown = (e: KeyboardEvent) => {
  if (keyActions[e.key]) {
    e.preventDefault()
    keyActions[e.key](e)
  }
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
    player.value.on('useractive', updateControlBarState)
    player.value.on('userinactive', updateControlBarState)

    player.value.on('pause', updateControlBarState)
    player.value.on('play', updateControlBarState)

    player.value?.on('loadedmetadata', () => {
      addTheaterBtn()
      addMarkers()
      appendShortCutsPopupBtn()
      appendShortCutsPopup()
      appendSkipIndicator()
      appendVolumeIndicator()
      appendChapterIndicator()
      appendPlaybackRateIndicator()
      if (player.value) {
        const playerEl = player.value.el() as HTMLElement
        playerEl.addEventListener('touchstart', handleTouch, { passive: false })
        playerEl.addEventListener('click', () => {
          if (!player.value) return
          player.value.hasStarted_ || player.value.play()
        })
      }
      nextTick(() => {
        updateChapterTimeTooltip()
      })
    })
  })
}

// Initialize video.js when the component is mounted
onMounted(() => {
  initPlayer()
  document.addEventListener('keydown', handleKeydown)
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

watch(
  () => isShortcutsPopupVisible.value,
  () => {
    if (player.value) {
      const videoElement = player.value.el()

      const targetElement = videoElement?.querySelector('.popup-overlay')
      if (!targetElement) return

      if (isShortcutsPopupVisible.value) {
        targetElement?.classList.add('show')
      } else if (!isShortcutsPopupVisible.value) {
        targetElement?.classList.remove('show')
      }
    }
  }
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
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div ref="videoContainer"></div>
</template>
