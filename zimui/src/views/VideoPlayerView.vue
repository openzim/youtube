<script setup lang="ts">
import { ref, type Ref, onMounted } from 'vue'
import { useMainStore } from '@/stores/main'
import { useRoute } from 'vue-router'

import type { Video } from '@/types/Videos'

const main = useMainStore()
const route = useRoute()
const slug: string = route.params.slug as string
const video: Ref<Video> = ref<Video>() as Ref<Video>

// Fetch video data
const fetchData = async function () {
  if (slug) {
    try {
      const resp = await main.fetchVideo(slug)
      if (resp) {
        video.value = resp
      }
    } catch (error) {
      main.setErrorMessage('An unexpected error occured when fetching video data.')
    }
  }
}

// Fetch the data on component mount
onMounted(() => {
  fetchData()
})
</script>

<template>
  <v-container v-if="video">
    <h1>Video Player Page</h1>
    <h2>Slug: {{ slug }}</h2>
    <p>Title: {{ video.title }}</p>
  </v-container>
</template>
