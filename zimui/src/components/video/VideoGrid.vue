<script setup lang="ts">
import type { VideoPreview } from '@/types/Videos'
import VideoCard from './VideoCard.vue'

const props = defineProps<{
  videos: VideoPreview[]
}>()
</script>

<template>
  <v-container>
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
        <video-card :video="video" />
      </v-col>
    </v-row>
  </v-container>
</template>
