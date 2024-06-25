<script setup lang="ts">
import type { Playlist } from '@/types/Playlists'

const props = defineProps<{
  playlist: Playlist
  currentVideoIndex: number
}>()

const emit = defineEmits(['click'])
</script>

<template>
  <v-card
    class="mx-auto border-thin rounded-lg"
    prepend-icon="mdi-playlist-play"
    append-icon="mdi-chevron-down"
    link
    flat
    color="grey-lighten-5"
    @click="() => emit('click')"
  >
    <template #title>
      <v-card-title>{{ props.playlist.title }}</v-card-title>
    </template>
    <template #subtitle>
      <v-card-subtitle class="text-caption">
        <span class="font-weight-medium">
          {{ props.playlist.author.channelTitle }}
        </span>
        - {{ props.currentVideoIndex + 1 }}/{{ props.playlist.videos.length }}
      </v-card-subtitle>
    </template>
  </v-card>
</template>
