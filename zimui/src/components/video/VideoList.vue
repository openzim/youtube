<script setup lang="ts">
import { computed } from 'vue'
import { useDisplay } from 'vuetify'

import type { Playlist } from '@/types/Playlists'
import VideoCarousel from '@/components/video/carousel/VideoCarousel.vue'
import VideoCarouselInfo from '@/components/video/carousel/VideoCarouselInfo.vue'

const { mdAndDown } = useDisplay()

const props = defineProps<{
  playlists: Playlist[]
}>()

const items = computed(() => props.playlists.slice(0, 12))

const loadMoreItems = async () => {
  return new Promise<Playlist[]>((resolve) => {
    setTimeout(() => {
      resolve(props.playlists.slice(items.value.length, items.value.length + 12))
    }, 100)
  })
}

const load = async ({ done }: { done: (status: 'ok' | 'empty') => void }) => {
  const moreItems = await loadMoreItems()
  items.value.push(...moreItems)
  if (items.value.length === props.playlists.length) {
    done('empty')
    return
  }
  done('ok')
}
</script>

<template>
  <v-container class="px-1 py-0 video-list" :fluid="mdAndDown">
    <v-infinite-scroll class="h-full overflow-hidden" :items="items" empty-text="" @load="load">
      <div v-for="playlist in items" :key="playlist.id">
        <video-carousel-info
          :title="playlist?.title || 'Main Playlist'"
          :count="playlist?.videosCount || 0"
          :count-text="playlist?.videosCount === 1 ? 'video' : 'videos'"
          icon="mdi-video-outline"
          :video-slug="playlist.videos[0]?.slug || ''"
          :playlist-slug="playlist.slug"
        />
        <video-carousel
          v-if="playlist.videos"
          :videos="playlist.videos"
          :playlist-slug="playlist.slug"
          :show-view-more="playlist.videosCount > 12"
        />
        <v-container class="py-2"><v-divider /></v-container>
      </div>
    </v-infinite-scroll>
  </v-container>
</template>
