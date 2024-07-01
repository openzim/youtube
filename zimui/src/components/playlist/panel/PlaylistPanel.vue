<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { useDisplay } from 'vuetify'

import type { Playlist } from '@/types/Playlists'
import { LoopOptions } from '@/types/Playlists'

import PlaylistPanelItem from './PlaylistPanelItem.vue'

const { smAndDown } = useDisplay()

const props = defineProps<{
  playlist: Playlist
  videoSlug: string
  playlistSlug: string
  currentVideoIndex: number
  showToggle: boolean
  loop: LoopOptions
  shuffle: boolean
}>()

const windowHeight = ref(
  window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight
)

// Calculate the height of the playlist panel container
const panelContainerHeight = computed<string>(() => {
  if (smAndDown.value) return '350px'

  const panelHeight = Math.min(windowHeight.value - 150, 800)
  const totalItemsHeight = props.playlist.videos.length * 90

  return totalItemsHeight < panelHeight ? '100%' : `${panelHeight}px`
})

watch(
  () => props.videoSlug,
  () => {
    nextTick(() => {
      scrollToCurrentVideo()
    })
  }
)

// Scroll to the current video in the playlist panel
const scrollToCurrentVideo = () => {
  const currentVideoId = `video-item-${props.currentVideoIndex}`
  const currentVideoElement = document.getElementById(currentVideoId)
  const panelContainer = document.getElementById('panel-items-container')
  if (currentVideoElement && panelContainer) {
    panelContainer.scrollTop = currentVideoElement.offsetTop - panelContainer.offsetTop
  }
}

const emit = defineEmits(['shuffle', 'loop', 'hide-panel'])
</script>

<template>
  <v-card class="border-thin rounded-lg" flat>
    <v-card-item class="border-b-thin bg-grey-lighten-5 px-2">
      <v-row class="px-2">
        <v-col :cols="showToggle ? 9 : 12">
          <v-card-title class="panel-title">{{ props.playlist.title }}</v-card-title>
          <v-card-subtitle class="panel-channel text-caption">
            <span class="font-weight-medium">
              {{ props.playlist.author.channelTitle }}
            </span>
            - {{ props.currentVideoIndex + 1 }}/{{ props.playlist.videos.length }}
          </v-card-subtitle>
        </v-col>
        <v-col v-if="showToggle" cols="3" class="d-flex align-center justify-end">
          <v-btn
            class="pa-2"
            icon="mdi-close"
            size="md"
            variant="text"
            @click="() => emit('hide-panel')"
          ></v-btn>
        </v-col>
      </v-row>
      <v-row dense no-gutters>
        <v-col>
          <v-btn
            class="pa-2"
            size="md"
            variant="text"
            :icon="loop === LoopOptions.loopVideo ? 'mdi-repeat-once' : 'mdi-repeat'"
            :color="loop === LoopOptions.off ? 'grey' : 'grey-darken-3'"
            :title="
              loop === LoopOptions.off
                ? 'Loop playlist'
                : loop === LoopOptions.loopPlaylist
                ? 'Loop video'
                : 'Turn off loop'
            "
            flat
            @click="() => emit('loop')"
          >
          </v-btn>
          <v-btn
            class="pa-2"
            size="md"
            variant="text"
            icon="mdi-shuffle"
            :color="shuffle ? 'grey-darken-3' : 'grey'"
            title="Shuffle Playlist"
            flat
            @click="() => emit('shuffle')"
          ></v-btn>
        </v-col>
      </v-row>
    </v-card-item>

    <v-card-item class="pa-0">
      <div id="panel-items-container" :style="{ height: panelContainerHeight }">
        <playlist-panel-item
          v-for="(item, index) in props.playlist.videos"
          :id="`video-item-${index}`"
          :key="item.slug"
          :video="item"
          :order="index + 1"
          :selected="item.slug === props.videoSlug"
          :playlist-slug="props.playlistSlug"
        ></playlist-panel-item>
      </div>
    </v-card-item>
  </v-card>
</template>

<style scoped>
#panel-items-container {
  overflow: auto;
  scroll-behavior: smooth;
}
</style>
