<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'

import { useMainStore } from '@/stores/main'

import type { Playlist } from '@/types/Playlists'
import VideoList from '@/components/video/VideoList.vue'

const main = useMainStore()
const playlists = ref<Playlist[]>()
const isLoading = ref(true)

// Watch for changes in the main playlist
watch(
  () => main.channel?.id,
  () => {
    fetchData()
  }
)

// Fetch the videos for the main playlist
const fetchData = async function () {
  if (main.channel?.id) {
    try {
      const resp = await main.fetchHomePlaylists()
      if (resp) {
        playlists.value = resp.playlists
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
    <video-list v-if="playlists" :playlists="playlists" />
  </div>
</template>
