<script setup lang="ts">
import { ref, type Ref, computed, watch } from 'vue'
import { useMainStore } from '@/stores/main'
import { useRoute, useRouter } from 'vue-router'
import { useDisplay } from 'vuetify'

import type { Video } from '@/types/Videos'
import { LoopOptions, type Playlist } from '@/types/Playlists'

import VideoPlayer from '@/components/video/VideoPlayer.vue'
import VideoTitleInfo from '@/components/video/player/VideoTitleInfo.vue'
import VideoChannelInfo from '@/components/video/player/VideoChannelInfo.vue'
import VideoDescription from '@/components/video/player/VideoDescription.vue'
import PlaylistPanel from '@/components/playlist/panel/PlaylistPanel.vue'
import PlaylistPanelPreview from '@/components/playlist/panel/PlaylistPanelPreview.vue'

const main = useMainStore()
const route = useRoute()
const router = useRouter()
const video_slug = ref(route.params.slug as string)
const playlist_slug = ref(route.query.list as string)

const video: Ref<Video> = ref<Video>() as Ref<Video>
const playlist: Ref<Playlist> = ref<Playlist>() as Ref<Playlist>
const showPlaylistPanel = ref<boolean>(false)

// Fetch playlist data
const fetchPlaylistData = async function (playlist_slug: string) {
  if (playlist_slug) {
    try {
      const resp = await main.fetchPlaylist(playlist_slug)
      if (resp) {
        playlist.value = resp
      }
    } catch (error) {
      main.setErrorMessage('An unexpected error occured when fetching playlist data.')
    }
  }
}

// Fetch video data
const fetchVideoData = async function (video_slug: string) {
  if (video_slug) {
    try {
      const resp = await main.fetchVideo(video_slug)
      if (resp) {
        video.value = resp
      }
    } catch (error) {
      main.setErrorMessage('An unexpected error occured when fetching video data.')
    }
  }
}

// Watch for changes in the route params and query
watch(
  () => route.params.slug,
  (newSlug) => {
    video_slug.value = newSlug as string
    fetchVideoData(video_slug.value)
  },
  { immediate: true }
)

watch(
  () => route.query.list,
  (newList) => {
    playlist_slug.value = newList as string
    fetchPlaylistData(playlist_slug.value)
  },
  { immediate: true }
)

const videoURL = computed<string>(() => {
  return video.value?.videoPath || ''
})

// This computes the video format from the video URL
// For example, if videoURL is "/some_path/video.webm", then videoFormat will be "video/webm"
const videoFormat = computed<string>(() => {
  return 'video/' + videoURL.value?.split('.').pop()
})

const videoPoster = computed<string>(() => {
  return video.value?.thumbnailPath || ''
})

const chapterList = computed(() => {
  return video.value?.chapterList ?? []
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

const chapters = computed(() => {
  if (!video.value?.chaptersPath) {
    return []
  }
  return [
    {
      kind: 'chapters',
      src: `${video.value?.chaptersPath}/chapters.vtt`,
      srclang: 'en',
      label: 'Chapters',
      default: true
    }
  ]
})

const tracks = computed(() => {
  return [...subtitles.value, ...chapters.value]
})

const videoOptions = ref({
  controls: true,
  autoplay: true,
  preload: true,
  fluid: true,
  responsive: true,
  enableSmoothSeeking: true,
  controlBar: { pictureInPictureToggle: false },
  playbackRates: [0.25, 0.5, 1, 1.5, 2],
  techOrder: ['html5', 'ogvjs'],
  html5: { preloadTextTracks: false },
  ogvjs: {
    base: './assets/ogvjs',
    preloadTextTracks: false
  },
  poster: videoPoster,
  sources: [
    {
      src: videoURL,
      type: videoFormat
    }
  ],
  tracks: tracks
})

const currentVideoIndex = computed(() => {
  return playlist.value.videos.findIndex((video) => video.slug === video_slug.value) || 0
})

const onVideoEnded = () => {
  if (!playlist.value) return
  if (main.loop === LoopOptions.loopVideo) return
  if (main.shuffle) {
    let randomIndex: number
    do {
      randomIndex = Math.floor(Math.random() * playlist.value.videos.length)
    } while (randomIndex === currentVideoIndex.value)
    video_slug.value = playlist.value.videos[randomIndex].slug
    router.push({
      name: 'watch-video',
      params: { slug: video_slug.value },
      query: { list: playlist_slug.value }
    })
  } else {
    // If the current video is the last video in the playlist and loop is disabled, do nothing
    if (
      currentVideoIndex.value === playlist.value.videos.length - 1 &&
      main.loop === LoopOptions.off
    ) {
      return
    }
    video_slug.value =
      playlist.value.videos[(currentVideoIndex.value + 1) % playlist.value.videos.length].slug
    router.push({
      name: 'watch-video',
      params: { slug: video_slug.value },
      query: { list: playlist_slug.value }
    })
  }
}

const goToNextVideo = () => {
  if (!playlist.value) return
  if (currentVideoIndex.value === playlist.value.videos.length - 1) return
  video_slug.value =
    playlist.value.videos[(currentVideoIndex.value + 1) % playlist.value.videos.length].slug
  router.push({
    name: 'watch-video',
    params: { slug: video_slug.value },
    query: { list: playlist_slug.value }
  })
}

const goToPrevVideo = () => {
  if (!playlist.value) return
  if (currentVideoIndex.value === 0) return
  video_slug.value =
    playlist.value.videos[(currentVideoIndex.value - 1) % playlist.value.videos.length].slug
  router.push({
    name: 'watch-video',
    params: { slug: video_slug.value },
    query: { list: playlist_slug.value }
  })
}

const { smAndDown, mdAndDown } = useDisplay()

const loopOptions: LoopOptions[] = [
  LoopOptions.off,
  LoopOptions.loopPlaylist,
  LoopOptions.loopVideo
]
const cycleLoopOption = () => {
  const currentIndex = loopOptions.indexOf(main.loop)
  main.setLoop(loopOptions[(currentIndex + 1) % loopOptions.length])
}

// Update the document title with the video title
watch(
  () => video.value,
  () => {
    if (video.value) document.title = video.value.title
  }
)
</script>

<template>
  <v-container v-if="video" :fluid="mdAndDown" :class="{'watch-theater-mode': main.theaterMode, 'watch-default-mode': !main.theaterMode && !smAndDown, 'watch-default-mode-smAndDown': !main.theaterMode && smAndDown}">
    <!-- Video Player -->
    <div class="video-player">
      <video-player
        :options="videoOptions"
        :loop="main.loop === LoopOptions.loopVideo"
        :chapters-list="chapterList"
        @video-ended="onVideoEnded"
        @next-video="goToNextVideo" 
        @prev-video="goToPrevVideo"
        />
    </div>

    <!-- Video Details & Mobile Playlist Panel -->
    <div>
      <!-- Playlist panel for mobile devices -->
      <div v-if="smAndDown && playlist" class="mt-5">
        <playlist-panel-preview
          v-if="!showPlaylistPanel"
          :playlist="playlist"
          :current-video-index="currentVideoIndex"
          @click="() => (showPlaylistPanel = !showPlaylistPanel)"
        />
        <playlist-panel
          v-else
          :playlist="playlist"
          :video-slug="video_slug"
          :playlist-slug="playlist_slug"
          :current-video-index="currentVideoIndex"
          :loop="main.loop"
          :shuffle="main.shuffle"
          :show-toggle="true"
          @shuffle="() => main.setShuffle(!main.shuffle)"
          @loop="cycleLoopOption"
          @hide-panel="() => (showPlaylistPanel = false)"
        />
      </div>
      <!-- Video Details -->
      <div class="mt-5">
        <video-title-info :title="video.title" :publication-date="video.publicationDate" />
        <video-channel-info
          :profile-path="video.author.profilePath || ''"
          :channel-title="video.author.channelTitle || ''"
          :channel-description="video.author.channelDescription || ''"
          :joined-date="video.author.channelJoinedDate || ''"
        />
        <video-description :description="video.description" />
      </div>
    </div>

    <!-- Desktop Playlist Panel -->
    <div v-if="!smAndDown" :class="['playlist-panel ml-5', main.theaterMode ? 'mt-5': '']">
      <playlist-panel
          :playlist="playlist"
          :video-slug="video_slug"
          :playlist-slug="playlist_slug"
          :current-video-index="currentVideoIndex"
          :loop="main.loop"
          :shuffle="main.shuffle"
          :show-toggle="false"
          @shuffle="() => main.setShuffle(!main.shuffle)"
          @loop="cycleLoopOption"
        />
    </div>
  </v-container>
</template>
