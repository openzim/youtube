<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'

import { useMainStore } from '@/stores/main'
import type { PlaylistPreview } from '@/types/Playlists'

import PlaylistGrid from '@/components/playlist/PlaylistGrid.vue'
import TabInfo from '@/components/common/ViewInfo.vue'

const main = useMainStore()
const playlists = ref<PlaylistPreview[]>()

// Watch for changes in the main playlist
watch(
  () => main.channel?.mainPlaylist,
  () => {
    fetchData()
  }
)

// Fetch the playlists for the playlist tab
const fetchData = async function () {
  if (main.channel?.mainPlaylist) {
    try {
      const resp = await main.fetchPlaylists()
      if (resp) {
        playlists.value = resp.playlists
      }
    } catch (error) {
      main.setErrorMessage('An unexpected error occured when fetching playlists.')
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
    :title="'Playlists from ' + main.channel?.title || ''"
    :count="playlists?.length || 0"
    :count-text="playlists?.length === 1 ? 'playlist' : 'playlists'"
    icon="mdi-playlist-play"
  />
  <playlist-grid v-if="playlists" :playlists="playlists" />
</template>
