<script setup lang="ts">
import { ref, type Ref, onMounted } from 'vue'
import { useMainStore } from '@/stores/main'
import { useRoute, useRouter } from 'vue-router'

import type { Playlist } from '@/types/Playlists'
import { formatDate } from '@/utils/format-utils'

import PlaylistPanelItem from '@/components/playlist/panel/PlaylistPanelItem.vue'
import thumbnailPlaceholder from '@/assets/images/thumbnail-placeholder.webp'

const main = useMainStore()
const route = useRoute()
const router = useRouter()
const slug: string = route.params.slug as string

const playlist: Ref<Playlist> = ref<Playlist>() as Ref<Playlist>

// Fetch playlist data
const fetchPlaylistData = async function () {
  if (slug) {
    try {
      const resp = await main.fetchPlaylist(slug)
      if (resp) {
        playlist.value = resp
      }
    } catch (error) {
      main.setErrorMessage('An unexpected error occured when fetching playlist data.')
    }
  }
}

const onPlayAllClick = function () {
  main.setShuffle(false)
  router.push({
    name: 'watch-video',
    params: { slug: playlist.value.videos[0].slug },
    query: { list: slug }
  })
}

const onShuffleClick = function () {
  main.setShuffle(true)
  const randomIndex = Math.floor(Math.random() * playlist.value.videos.length)
  const randomVideo = playlist.value.videos[randomIndex]
  router.push({
    name: 'watch-video',
    params: { slug: randomVideo.slug },
    query: { list: slug }
  })
}

// Fetch the data on component mount
onMounted(() => {
  fetchPlaylistData()
})
</script>

<template>
  <v-container v-if="playlist">
    <v-row>
      <v-spacer />
      <v-col cols="12" md="4" xl="3" xxl="2">
        <v-card flat class="header-card rounded-lg pa-5 bg-grey-lighten-4">
          <v-img
            :lazy-src="thumbnailPlaceholder"
            :src="playlist.thumbnailPath"
            min-width="125"
            max-width="400"
            aspect-ratio="16/9"
            class="rounded-lg"
          />

          <p class="playlist-title text-h5 font-weight-bold mt-4">{{ playlist.title }}</p>
          <p class="playlist-channel text-body-1 font-weight-medium mt-2">
            {{ playlist.author.channelTitle }}
          </p>
          <p class="playlist-info text-caption mt-1">
            <v-icon>mdi-video-outline</v-icon> {{ playlist.videosCount }} videos |
            {{ formatDate(playlist.publicationDate) }}
          </p>
          <div class="mt-6 d-flex align-center justify-center">
            <v-btn
              class="border-thin flex-fill mr-2"
              rounded="lg"
              prepend-icon="mdi-play"
              variant="flat"
              @click="onPlayAllClick"
            >
              Play All
            </v-btn>
            <v-btn
              class="border-thin bg-grey-lighten-4 flex-fill"
              rounded="lg"
              prepend-icon="mdi-shuffle"
              variant="flat"
              @click="onShuffleClick"
            >
              Shuffle
            </v-btn>
          </div>

          <v-btn
            class="mt-2 border-thin"
            rounded="lg"
            :to="{ name: 'playlists' }"
            flat
            block
            color="grey-darken-3"
          >
            <v-icon icon="mdi-arrow-left" start></v-icon>
            Back to Playlists
          </v-btn>
          <p v-if="playlist.description !== ''" class="playlist-description text-caption mt-4">
            {{ playlist.description }}
          </p>
        </v-card>
      </v-col>
      <v-col cols="12" md="8" xl="6" xxl="4">
        <v-container class="pa-0">
          <v-row dense>
            <v-col
              v-for="(video, idx) in playlist.videos"
              :key="video.id"
              cols="12"
              class="py-0 my-0"
            >
              <playlist-panel-item
                :video="video"
                :order="idx + 1"
                :playlist-slug="slug"
                :selected="false"
              />
            </v-col>
          </v-row>
        </v-container>
      </v-col>
      <v-spacer />
    </v-row>
  </v-container>
</template>
