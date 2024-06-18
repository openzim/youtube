<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import videojs from 'video.js'
import type Player from 'video.js/dist/types/player'

import 'video.js/dist/video-js.css'
import '@/assets/vjs-youtube.css'

const props = defineProps({
  options: {
    type: Object,
    default: () => ({})
  }
})

const videoPlayer = ref<HTMLVideoElement>()
const player = ref<Player>()

// Initialize video.js when the component is mounted
onMounted(() => {
  if (videoPlayer.value) {
    player.value = videojs(videoPlayer.value, props.options)
  }
})

// Destroy video.js when the component is unmounted
onBeforeUnmount(() => {
  if (player.value) {
    player.value.dispose()
  }
})
</script>

<template>
  <div>
    <video ref="videoPlayer" class="video-js vjs-youtube"></video>
  </div>
</template>
