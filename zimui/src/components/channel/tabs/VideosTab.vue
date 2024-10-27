<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { computed } from 'vue'

import TabView from '@/views/TabView.vue'

const main = useMainStore()
const videosAvailable = computed(() => main.channel?.longVideosPlaylist)
</script>

<template>
  <div v-if="videosAvailable">
    <tab-view
    :playlist-label="'longVideosPlaylist'"
    :playlist-type="'Videos'" />
  </div>
  <div v-else>
   <p style="text-align:center">No Video available</p>
  </div>
</template>
