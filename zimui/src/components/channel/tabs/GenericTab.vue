<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useMainStore } from '@/stores/main'
import type { VideoPreview } from '@/types/Videos'

import VideoGrid from '@/components/video/VideoGrid.vue'
import TabInfo from '@/components/common/ViewInfo.vue'
import type { Playlist } from '@/types/Playlists'

const props = defineProps({
  playlistSlug: {
    type: String,
    required: true
  },
  titlePrefix: {
    type: String,
    required: true
  }
})

const main = useMainStore()
const videos = ref<VideoPreview[]>([])
const playlist = ref<Playlist>()
const isLoading = ref(true)

// Fetch the videos for the playlist
const fetchData = async function () {
  const currentPlaylist = main.channel?.[props.playlistSlug as keyof typeof main.channel]
  if (currentPlaylist) {
    try {
      if (typeof currentPlaylist !== 'string')
        throw new Error('Invalid playlistSlug: expected a string value.')
      const resp = await main.fetchPlaylist(currentPlaylist)
      if (resp) {
        playlist.value = resp
        videos.value = resp.videos
        isLoading.value = false
      }
    } catch (error) {
      console.error('Error fetching videos:', error)
      main.setErrorMessage('An unexpected error occurred when fetching videos.')
    }
  }
}
// Watch for changes in the playlist slug prop
watch(
  () => main.channel?.[props.playlistSlug as keyof typeof main.channel],
  () => {
    fetchData()
  }
)

// Fetch the data on component mount
onMounted(() => {
  fetchData()
})
</script>

<template>
  <div v-if="isLoading" class="container mt-8 d-flex justify-center">
    <v-progress-circular class="d-inline" indeterminate></v-progress-circular>
  </div>
  <div v-else>
    <tab-info
      :title="titlePrefix + ' from ' + main.channel?.title"
      :count="playlist?.videosCount || 0"
      :count-text="playlist?.videos.length === 1 ? 'video' : 'videos'"
      icon="mdi-video-outline"
    />
    <video-grid
      v-if="videos"
      :videos="videos"
      :playlist-slug="`main.channel?.${props.playlistSlug}`"
    />
  </div>
</template>
