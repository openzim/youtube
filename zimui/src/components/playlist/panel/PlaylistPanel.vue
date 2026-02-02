<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { useDisplay } from 'vuetify'
import { formatTimestamp } from '@/utils/format-utils'

import type { Playlist } from '@/types/Playlists'
import { LoopOptions } from '@/types/Playlists'

import PlaylistPanelItem from './PlaylistPanelItem.vue'
import type { VideoPreview } from '@/types/Videos'

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

const isLoading = computed(() => props.playlist.videos === undefined)

const windowHeight = ref(
  window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight
)

// Calculate the height of the playlist panel container
const panelContainerHeight = computed<string>(() => {
  const panelHeight = Math.min(windowHeight.value - 150, smAndDown.value ? 350 : 800)
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

const items = computed(() => props.playlist.videos.slice(0, 48))

const loadMoreItems = async () => {
  return new Promise<VideoPreview[]>((resolve) => {
    setTimeout(() => {
      resolve(props.playlist.videos.slice(items.value.length, items.value.length + 12))
    }, 100)
  })
}

const load = async ({ done }: { done: (status: 'ok' | 'empty') => void }) => {
  const moreItems = await loadMoreItems()
  items.value.push(...moreItems)
  if (items.value.length === props.playlist.videos.length) {
    done('empty')
    return
  }
  done('ok')
}
</script>

<template>
  <div v-if="isLoading" class="container mt-8 d-flex justify-center">
    <v-progress-circular class="d-inline" indeterminate></v-progress-circular>
  </div>
  <v-card v-else class="border-thin rounded-lg" flat>
    <v-card-item class="border-b-thin px-2">
      <v-row class="px-2">
        <v-col :cols="showToggle ? 9 : 12">
          <v-card-title class="panel-title">{{ props.playlist.title }}</v-card-title>
          <v-card-subtitle class="panel-channel text-caption">
            <span class="font-weight-medium">
              {{ props.playlist.author.channelTitle }}
            </span>
            - {{ props.currentVideoIndex + 1 }}/{{ props.playlist.videos.length }}
          </v-card-subtitle>
          <v-card-subtitle class="panel-channel text-caption">
            Total Duration: {{ formatTimestamp(props.playlist.duration) }}
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
        <v-col class="d-flex">
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
        <v-infinite-scroll class="h-full overflow-hidden" :items="items" empty-text="" @load="load">
          <playlist-panel-item
            v-for="(item, index) in items"
            :id="`video-item-${index}`"
            :key="item.slug"
            :video="item"
            :order="index + 1"
            :selected="item.slug === props.videoSlug"
            :playlist-slug="props.playlistSlug"
          ></playlist-panel-item>
        </v-infinite-scroll>
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
