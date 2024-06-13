import { createRouter, createWebHashHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import VideoPlayerView from '../views/VideoPlayerView.vue'

import VideosTab from '@/components/channel/tabs/VideosTab.vue'
import PlaylistsTab from '@/components/channel/tabs/PlaylistsTab.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      redirect: '/videos',
      children: [
        {
          path: 'videos',
          name: 'videos',
          component: VideosTab
        },
        {
          path: 'playlists',
          name: 'playlists',
          component: PlaylistsTab
        }
      ]
    },
    {
      path: '/watch/:slug',
      name: 'watch-video',
      component: VideoPlayerView
    }
  ],
  scrollBehavior() {
    return { top: 0, behavior: 'smooth' }
  }
})

export default router
