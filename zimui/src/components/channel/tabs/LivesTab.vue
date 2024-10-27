<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { computed } from 'vue'

import TabView from '@/views/TabView.vue'

const main = useMainStore()
const livesAvailable = computed(() => main.channel?.livesPlaylist)
</script>

<template>
  <div v-if="livesAvailable">
    <tab-view :playlist-label="'livesPlaylist'" :playlist-type="'Lives'" />
  </div>
  <div v-else>
    <p style="text-align: center">No Live available</p>
  </div>
</template>
