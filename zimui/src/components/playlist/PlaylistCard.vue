<script setup lang="ts">
import { computed } from 'vue'
import { useDisplay } from 'vuetify'

import type { PlaylistPreview } from '@/types/Playlists'
import { truncateText } from '@/utils/format-utils'

import thumbnailPlaceholder from '@/assets/images/thumbnail-placeholder.webp'

const { smAndDown } = useDisplay()

const props = defineProps<{
  playlist: PlaylistPreview
}>()

// Set the maximum length of the title based on the screen size
const titleLength = computed<number>(() => {
  if (smAndDown.value) {
    return 30
  } else {
    return 60
  }
})

// Truncate the title if it's too long
const truncatedTitle = computed<string>(() => {
  return truncateText(props.playlist.title, titleLength.value)
})

const videoCount = computed<string>(() => {
  return props.playlist.videosCount === 1 ? '1 video' : `${props.playlist.videosCount} videos`
})
</script>

<template>
  <router-link
    :to="{
      name: 'watch-video',
      params: { slug: props.playlist.mainVideoSlug },
      query: { list: props.playlist.slug }
    }"
  >
    <v-card flat class="mx-4">
      <v-row no-gutters>
        <v-col cols="5" md="12">
          <div class="d-flex flex-column align-center">
            <v-card
              height="5"
              width="90%"
              color="black"
              class="playlist-bg rounded-t-lg rounded-b-0 opacity-80"
              flat
            ></v-card>
          </div>
          <div class="position-relative">
            <v-img
              class="d-block border-thin rounded-lg"
              :lazy-src="thumbnailPlaceholder"
              :src="props.playlist.thumbnailPath"
              min-width="125"
              max-width="400"
            ></v-img>
            <v-chip
              class="bg-black opacity-80 position-absolute bottom-0 right-0 mr-2 mb-2"
              prepend-icon="mdi-playlist-play"
              size="small"
              rounded="lg"
              >{{ videoCount }}</v-chip
            >
          </div>
        </v-col>
        <v-col
          cols="7"
          md="12"
          class="d-flex flex-column align-start align-md-center justify-center justify-md-center text-left text-md-center"
        >
          <v-card-title
            class="text-body-1 text-wrap px-4 px-md-0 pb-0"
            :title="props.playlist.title"
            >{{ truncatedTitle }}</v-card-title
          >
          <router-link
            :to="{
              name: 'view-playlist',
              params: { slug: props.playlist.slug }
            }"
          >
            <v-card-subtitle class="view-playlist-link text-caption text-wrap px-4 px-md-0">
              View full playlist
            </v-card-subtitle>
          </router-link>
        </v-col>
      </v-row>
    </v-card>
  </router-link>
</template>

<style scoped>
.view-playlist-link {
  color: initial;
}

.view-playlist-link:hover {
  text-decoration: underline;
}

.playlist-bg {
  margin-bottom: 0.1rem;
}
</style>
