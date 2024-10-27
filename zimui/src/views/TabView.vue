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
const isLoading = ref(true)

const props = defineProps({
  playlistLabel: {
    type: String,
    required: true
  },
  playlistType: {
    type: String,
    required: true
  }
})

// Watch for changes in the playlist
watch(
  () => main.channel?.[props.playlistLabel],
  () => {
    fetchData()
  }
)

// Fetch the videos for the playlist
const fetchData = async function () {
  if (main.channel?.[props.playlistLabel]) {
    try {
      const resp = await main.fetchPlaylist(main.channel?.[props.playlistLabel])
      if (resp) {
        playlist.value = resp
        videos.value = resp.videos
        isLoading.value = false
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
  <div v-if="isLoading" class="container mt-8 d-flex justify-center">
    <v-progress-circular class="d-inline" indeterminate></v-progress-circular>
  </div>
  <div v-else>
     <tab-info
      :title="[props.playlistType]+' from '+main.channel?.title"
      :count="playlist?.videosCount || 0"
      :count-text="playlist?.videos.length === 1 ? 'video' : 'videos'"
      icon="mdi-video-outline"
    />
    <video-grid v-if="videos" :videos="videos" :playlist-slug="main.channel?.[props.playlistLabel]" />
  </div>
</template>
