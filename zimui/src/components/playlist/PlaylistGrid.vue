<script setup lang="ts">
import { computed } from 'vue'
import { useDisplay } from 'vuetify'
import type { PlaylistPreview } from '@/types/Playlists'
import PlaylistCard from './PlaylistCard.vue'

const { mdAndDown } = useDisplay()

const props = defineProps<{
  playlists: PlaylistPreview[]
}>()

const items = computed(() => props.playlists.slice(0, 48))

const loadMoreItems = async () => {
  return new Promise<PlaylistPreview[]>((resolve) => {
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
  <v-container class="px-1" :fluid="mdAndDown">
    <v-infinite-scroll class="h-full overflow-hidden" :items="items" empty-text="" @load="load">
      <v-row dense>
        <v-col
          v-for="playlist in items"
          :key="playlist.id"
          cols="12"
          md="4"
          lg="3"
          xl="2"
          xxl="1"
          class="mb-2 mb-md-6"
        >
          <playlist-card :playlist="playlist" />
        </v-col>
      </v-row>
    </v-infinite-scroll>
  </v-container>
</template>
