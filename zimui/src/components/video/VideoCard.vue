<script setup lang="ts">
import { computed } from 'vue'
import { useDisplay } from 'vuetify'

import type { VideoPreview } from '@/types/Videos'
import { formatTimestamp, truncateText } from '@/utils/format-utils'

import thumbnailPlaceholder from '@/assets/images/thumbnail-placeholder.webp'

const { smAndDown } = useDisplay()

const props = defineProps<{
  video: VideoPreview
}>()

// Set the maximum length of the title based on the screen size
const titleLength = computed<number>(() => {
  if (smAndDown.value) {
    return 40
  } else {
    return 60
  }
})

// Truncate the title if it's too long
const truncatedTitle = computed<string>(() => {
  return truncateText(props.video.title, titleLength.value)
})

// Convert the duration from ISO 8601 to a human-readable format
const duration = computed<string>(() => {
  return formatTimestamp(props.video.duration)
})
</script>

<template>
  <router-link :to="{ name: 'watch-video', params: { slug: props.video.slug } }">
    <v-card flat class="mx-4">
      <v-row no-gutters>
        <v-col cols="5" md="12">
          <div class="position-relative">
            <v-img
              class="rounded-lg border-thin"
              :lazy-src="thumbnailPlaceholder"
              :src="props.video.thumbnailPath"
              min-width="125"
              max-width="400"
            ></v-img>
            <v-chip
              class="bg-black opacity-80 position-absolute bottom-0 right-0 mr-3 mb-2 pa-1"
              size="small"
              rounded="lg"
              >{{ duration }}</v-chip
            >
          </div>
        </v-col>
        <v-col
          cols="7"
          md="12"
          class="d-flex flex-column align-start align-md-center justify-center text-left text-md-center"
        >
          <v-card-title
            class="text-body-1 text-wrap px-4 px-md-0 pb-0"
            :title="props.video.title"
            >{{ truncatedTitle }}</v-card-title
          >
        </v-col>
      </v-row>
    </v-card>
  </router-link>
</template>
