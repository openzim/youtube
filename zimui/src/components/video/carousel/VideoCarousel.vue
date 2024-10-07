<script setup lang="ts">
import { computed } from 'vue'
import { useDisplay } from 'vuetify'
import type { VideoPreview } from '@/types/Videos'
import VideoCard from '@//components/video/VideoCard.vue'

import 'vue3-carousel/dist/carousel.css'
import { Carousel, Slide, Navigation } from 'vue3-carousel'

import thumbnailPlaceholder from '@/assets/images/thumbnail-placeholder.jpg'

const { smAndDown, md, mdAndDown, lg, xl } = useDisplay()

const itemsToShow = computed<number>(() => {
  if (smAndDown.value) {
    return 2
  } else if (md.value) {
    return 3
  } else if (lg.value) {
    return 4
  } else if (xl.value) {
    return 5
  } else {
    return 6
  }
})

const props = defineProps<{
  videos: VideoPreview[]
  playlistSlug?: string
  showViewMore?: boolean
}>()
</script>

<template>
  <v-container :fluid="mdAndDown">
    <carousel snap-align="start" :mouse-drag="false" :items-to-show="itemsToShow">
      <slide v-for="video in props.videos" :key="video.id">
        <video-card
          class="w-100"
          :video="video"
          :playlist-slug="playlistSlug"
          :carousel-mode="true"
        />
      </slide>
      <slide v-if="showViewMore" :key="'view-more'">
        <v-card flat class="w-100 mx-4">
          <v-row no-gutters>
            <v-col cols="12">
              <div class="position-relative">
                <v-img
                  class="d-block rounded-lg border-thin opacity-0"
                  :src="thumbnailPlaceholder"
                  min-width="125"
                  max-width="400"
                ></v-img>
                <v-btn
                  class="border-thin rounded-lg position-absolute w-100 h-100"
                  style="top: 50%; left: 50%; transform: translate(-50%, -50%)"
                  variant="outlined"
                  :to="{
                    name: 'view-playlist',
                    params: { slug: playlistSlug }
                  }"
                >
                  View All <v-icon class="ml-1">mdi-chevron-right-circle-outline</v-icon></v-btn
                >
              </div>
            </v-col>
            <v-col cols="12"> <v-card-text></v-card-text></v-col>
          </v-row>
        </v-card>
      </slide>
      <template #addons>
        <navigation />
      </template>
    </carousel>
  </v-container>
</template>
