<script setup lang="ts">
import { useDisplay } from 'vuetify'
import type { PlaylistPreview } from '@/types/Playlists'
import PlaylistCard from './PlaylistCard.vue'

const { mdAndDown } = useDisplay()

const props = defineProps<{
  playlists: PlaylistPreview[]
}>()
</script>

<template>
  <v-container class="px-1" :fluid="mdAndDown">
    <v-row dense>
      <v-col
        v-for="playlist in props.playlists"
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
  </v-container>
</template>
