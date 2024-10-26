<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { computed } from 'vue'

import LivesGridTab from './LivesGridTab.vue'

const main = useMainStore()
const hideTabs = computed(() => main.channel?.livesPlaylist)
</script>

<template>
  <div v-if="hideTabs">
    <lives-grid-tab />
  </div>
  <div v-else>
   <p style="text-align:center">No Live available</p>
  </div>
</template>
