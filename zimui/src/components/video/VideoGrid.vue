<script setup lang="ts">
import { useDisplay } from 'vuetify'
import type { VideoPreview } from '@/types/Videos'
import VideoCard from './VideoCard.vue'

const { mdAndDown } = useDisplay()

const props = defineProps<{
  videos: VideoPreview[]
  playlistSlug?: string
}>()
</script>

<template>
  <v-container class="px-1" :fluid="mdAndDown">
    <v-row dense>
      <v-col
        v-for="video in props.videos"
        :key="video.id"
        cols="12"
        md="4"
        lg="3"
        xl="2"
        xxl="1"
        class="mb-2 mb-md-6"
      >
        <video-card :video="video" :playlist-slug="playlistSlug" />
      </v-col>
    </v-row>
  </v-container>
</template>
