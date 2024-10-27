<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { computed } from 'vue'

import TabView from '@/views/TabView.vue'

const main = useMainStore()
const shortsAvailable = computed(() => main.channel?.shortsPlaylist)
</script>

<template>
  <div v-if="shortsAvailable">
    <tab-view 
    :playlist-label="'shortsPlaylist'" 
    :playlist-type="'Shorts'"
    />
  </div>
  <div v-else>
    <p style="text-align: center">No short available</p>
  </div>
</template>
