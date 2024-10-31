<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { computed } from 'vue'

import VideosGridTab from './VideosGridTab.vue'

const main = useMainStore()
const videosAvailable = computed(() => main.channel?.userLongUploadsPlaylist)
</script>

<template>
  <div v-if="videosAvailable">
    <videos-grid-tab/>
  </div>
  <div v-else>
   <p style="text-align:center">No Video available</p>
  </div>
</template>
