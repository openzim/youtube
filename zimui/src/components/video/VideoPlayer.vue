<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import videojs from 'video.js'
import type Player from 'video.js/dist/types/player'

import 'video.js/dist/video-js.css'
import '@/assets/vjs-youtube.css'
import '@/plugins/videojs-ogvjs.js'

const props = defineProps({
  options: {
    type: Object,
    default: () => ({})
  },
  loop: {
    type: Boolean,
    default: false
  }
})

const videoPlayer = ref<HTMLVideoElement>()
const player = ref<Player>()

const emit = defineEmits(['video-ended'])

// Initialize video.js when the component is mounted
onMounted(() => {
  if (videoPlayer.value) {
    player.value = videojs(videoPlayer.value, props.options)
    player.value.loop(props.loop)
    player.value.on('ended', () => {
      emit('video-ended')
    })
  }
})

// Watch for changes in the options prop
watch(
  () => props.options,
  (newOptions) => {
    if (player.value) {
      player.value.src(newOptions.sources)
      if (newOptions.autoplay === true) {
        player.value.play()
      } else {
        player.value.poster(newOptions.poster)
      }
    }
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
  <div>
    <video
      ref="videoPlayer"
      class="video-js vjs-youtube"
      :controls="props.options.controls"
      :preload="props.options.preload"
      :autoplay="props.options.autoplay"
      :poster="props.options.poster"
    >
      <source
        v-for="(source, idx) in props.options.sources"
        :key="idx"
        :src="source.src"
        :type="source.type"
      />
      <track
        v-for="(track, idx) in props.options.tracks"
        :key="idx"
        :kind="track.kind"
        :src="track.src"
        :srclang="track.code"
        :label="track.label"
      />
    </video>
  </div>
</template>
