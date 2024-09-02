<script setup lang="ts">
import { watch } from 'vue'
import { useMainStore } from '@/stores/main'

import ChannelHeader from '@/components/channel/ChannelHeader.vue'

const main = useMainStore()

// Update the document title with the channel title
watch(
  () => main.channel,
  () => {
    if (main.channel) document.title = main.channel.title
  }
)
</script>

<template>
  <channel-header />
  <router-view />
</template>
