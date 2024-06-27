<script setup lang="ts">
import { computed } from 'vue'
import type { VideoPreview } from '@/types/Videos'
import { formatTimestamp, truncateText } from '@/utils/format-utils'
import { useDisplay } from 'vuetify'
import thumbnailPlaceholder from '@/assets/images/thumbnail-placeholder.webp'

const { smAndDown } = useDisplay()

const props = defineProps<{
  video: VideoPreview
  order: number
  selected: boolean
  playlistSlug: string
}>()

// Set the maximum length of the title based on the screen size
const titleLength = computed<number>(() => {
  if (smAndDown.value) {
    return 60
  } else {
    return 80
  }
})

// Truncate the title if it's too long
const truncatedTitle = computed<string>(() => {
  return truncateText(props.video.title, titleLength.value)
})
</script>

<template>
  <v-card
    class="py-2 rounded-0"
    :variant="selected ? 'tonal' : 'flat'"
    flat
    :to="{
      name: 'watch-video',
      params: { slug: props.video.slug },
      query: { list: playlistSlug }
    }"
  >
    <v-row dense>
      <v-col cols="4" md="5" xl="4">
        <div class="d-flex position-relative">
          <div class="d-flex align-center justify-center text-caption">
            <v-icon v-if="selected" class="mx-1" size="15"> mdi-play </v-icon>
            <span v-else class="mx-2">{{ order }}</span>
          </div>
          <v-img
            class="border-thin rounded-lg"
            :lazy-src="thumbnailPlaceholder"
            :src="props.video.thumbnailPath"
            min-width="50"
            max-width="300"
          ></v-img>
          <v-chip
            class="bg-black opacity-80 position-absolute bottom-0 right-0 pa-1 mb-1 mr-1 text-caption"
            size="xs"
            rounded="lg"
          >
            {{ formatTimestamp(props.video.duration) }}
          </v-chip>
        </div>
      </v-col>
      <v-col cols="8" md="7" xl="8">
        <v-card-title class="text-body-2 text-wrap py-0 pr-2" :title="props.video.title">{{
          truncatedTitle
        }}</v-card-title>
      </v-col>
    </v-row>
  </v-card>
</template>
