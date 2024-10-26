<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { computed } from 'vue'

import ShortsGridTab from './ShortsGridTab.vue'

const main = useMainStore()
const hideTabs = computed(() => main.channel?.shortsPlaylist)
</script>

<template>
  <div v-if="hideTabs">
    <shorts-grid-tab />
  </div>
  <div v-else>
   <p style="text-align:center">No short available</p>
  </div>
</template>
