<script setup lang="ts">
import { ref, type Ref, onMounted, computed } from 'vue'
import { useMainStore } from '@/stores/main'
import { useRoute } from 'vue-router'

import type { Video } from '@/types/Videos'

import VideoPlayer from '@/components/video/VideoPlayer.vue'
import VideoTitleInfo from '@/components/video/player/VideoTitleInfo.vue'
import VideoChannelInfo from '@/components/video/player/VideoChannelInfo.vue'
import VideoDescription from '@/components/video/player/VideoDescription.vue'

const main = useMainStore()
const route = useRoute()
const slug: string = route.params.slug as string
const video: Ref<Video> = ref<Video>() as Ref<Video>

// Fetch video data
const fetchData = async function () {
  if (slug) {
    try {
      const resp = await main.fetchVideo(slug)
      if (resp) {
        video.value = resp
      }
    } catch (error) {
      main.setErrorMessage('An unexpected error occured when fetching video data.')
    }
  }
}

// Fetch the data on component mount
onMounted(() => {
  fetchData()
})

const videoURL = computed<string>(() => {
  return video.value?.videoPath || ''
})

const videoPoster = computed<string>(() => {
  return video.value?.thumbnailPath || ''
})

const subtitles = computed(() => {
  return video.value?.subtitleList.map((subtitle) => {
    return {
      kind: 'subtitles',
      src: `${video.value?.subtitlePath}/video.${subtitle.code}.vtt`,
      srclang: subtitle.code,
      label: subtitle.name
    }
  })
})

const videoOptions = ref({
  controls: true,
  autoplay: false,
  preload: true,
  fluid: true,
  responsive: true,
  enableSmoothSeeking: true,
  controlBar: { pictureInPictureToggle: false },
  playbackRates: [0.25, 0.5, 1, 1.5, 2],
  techOrder: ['html5'],
  poster: videoPoster,
  sources: [
    {
      src: videoURL
    }
  ],
  tracks: subtitles
})
</script>

<template>
  <v-container v-if="video">
    <!-- Video Player -->
    <v-row>
      <v-spacer />
      <v-col cols="12" md="8">
        <video-player :options="videoOptions" />
      </v-col>
      <v-spacer />
    </v-row>
    <!-- Video Details -->
    <v-row>
      <v-spacer />
      <v-col cols="12" md="8">
        <video-title-info :title="video.title" :publication-date="video.publicationDate" />
        <video-channel-info
          :profile-path="video.author.profilePath || ''"
          :channel-title="video.author.channelTitle || ''"
          :channel-description="video.author.channelDescription || ''"
          :joined-date="video.author.channelJoinedDate || ''"
        />
        <video-description :description="video.description" />
      </v-col>
      <v-spacer />
    </v-row>
  </v-container>
</template>
