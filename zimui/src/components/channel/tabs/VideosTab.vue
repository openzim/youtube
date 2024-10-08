<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { computed } from 'vue'

import VideosGridTab from './VideosGridTab.vue'
import VideosListTab from './VideosListTab.vue'

const main = useMainStore()
const hideTabs = computed(() => main.channel?.playlistCount === 1)
</script>

<template>
  <div v-if="hideTabs">
    <videos-grid-tab />
  </div>
  <div v-else>
    <videos-list-tab />
  </div>
</template>
