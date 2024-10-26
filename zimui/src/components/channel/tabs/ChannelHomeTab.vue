<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { computed } from 'vue'

import ChannelHomeGridTab from './ChannelHomeGridTab.vue'
import ChannelHomeListTab from './ChannelHomeListTab.vue'

const main = useMainStore()
const hideTabs = computed(() => main.channel?.playlistCount === 1)
</script>

<template>
  <div v-if="hideTabs">
    <channel-home-grid-tab />
  </div>
  <div v-else>
    <channel-Home-list-tab />
  </div>
</template>
