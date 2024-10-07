<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useDisplay } from 'vuetify'

import type { VideoPreview } from '@/types/Videos'
import { formatTimestamp, truncateText } from '@/utils/format-utils'
import { polyfillThumbnail } from '@/plugins/webp-hero'

import thumbnailPlaceholder from '@/assets/images/thumbnail-placeholder.jpg'

const { smAndDown } = useDisplay()

const props = defineProps<{
  video: VideoPreview
  playlistSlug?: string
  carouselMode?: boolean
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

const thumbnailSrc = ref(props.video.thumbnailPath)

// Polyfill the thumbnail if the browser doesn't support WebP
onMounted(async () => {
  if (!thumbnailSrc.value) return
  thumbnailSrc.value = await polyfillThumbnail(thumbnailSrc.value)
})
</script>

<template>
  <router-link
    :to="{
      name: 'watch-video',
      params: { slug: props.video.slug },
      query: { list: props.playlistSlug }
    }"
  >
    <v-card flat class="mx-4">
      <v-row no-gutters>
        <v-col :cols="carouselMode ? 12 : 5" md="12">
          <div class="position-relative">
            <v-img
              class="d-block rounded-lg border-thin"
              :lazy-src="thumbnailPlaceholder"
              :src="thumbnailSrc"
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
          :cols="carouselMode ? 12 : 7"
          md="12"
          class="d-flex flex-column align-md-center justify-center text-md-center"
          :class="{
            'align-center': carouselMode,
            'text-center': carouselMode,
            'align-start': !carouselMode,
            'text-left': !carouselMode
          }"
        >
          <v-card-title
            class="text-body-2 text-wrap px-4 px-md-0 pb-0"
            :title="props.video.title"
            >{{ truncatedTitle }}</v-card-title
          >
        </v-col>
      </v-row>
    </v-card>
  </router-link>
</template>
