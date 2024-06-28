<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'

import { useMainStore } from '@/stores/main'
import type { VideoPreview } from '@/types/Videos'

import VideoGrid from '@/components/video/VideoGrid.vue'
import TabInfo from '@/components/common/ViewInfo.vue'
import type { Playlist } from '@/types/Playlists'

const main = useMainStore()
const videos = ref<VideoPreview[]>([])
const playlist = ref<Playlist>()

// Watch for changes in the main playlist
watch(
  () => main.channel?.mainPlaylist,
  () => {
    fetchData()
  }
)

// Fetch the videos for the main playlist
const fetchData = async function () {
  if (main.channel?.mainPlaylist) {
    try {
      const resp = await main.fetchPlaylist(main.channel?.mainPlaylist)
      if (resp) {
        playlist.value = resp
        videos.value = resp.videos
      }
    } catch (error) {
      main.setErrorMessage('An unexpected error occured when fetching videos.')
    }
  }
}

// Fetch the data on component mount
onMounted(() => {
  fetchData()
})
</script>

<template>
  <tab-info
    :title="playlist?.title || 'Main Playlist'"
    :count="playlist?.videosCount || 0"
    :count-text="playlist?.videos.length === 1 ? 'video' : 'videos'"
    icon="mdi-video-outline"
  />
  <video-grid v-if="videos" :videos="videos" :playlist-slug="main.channel?.mainPlaylist" />
</template>
