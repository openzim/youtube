import { createRouter, createWebHashHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import VideoPlayerView from '../views/VideoPlayerView.vue'
import NotFoundView from '../views/NotFoundView.vue'

import ChannelHomeTab from '@/components/channel/tabs/ChannelHomeTab.vue'
import VideosTab from '@/components/channel/tabs/VideosTab.vue'
import ShortsTab from '@/components/channel/tabs/ShortsTab.vue'
import LivesTab from '@/components/channel/tabs/LivesTab.vue'
import PlaylistsTab from '@/components/channel/tabs/PlaylistsTab.vue'
import PlaylistView from '@/views/PlaylistView.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      redirect: '/channel-home',
      children: [
        {
          path: 'channel-home',
          name: 'channel-home',
          component: ChannelHomeTab
        },
        {
          path: 'videos',
          name: 'videos',
          component: VideosTab
        },
        {
          path: 'shorts',
          name: 'shorts',
          component: ShortsTab
        },
        {
          path: 'lives',
          name: 'lives',
          component: LivesTab
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
    },
    {
      path: '/playlist/:slug',
      name: 'view-playlist',
      component: PlaylistView
    },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFoundView }
  ],
  scrollBehavior() {
    return { top: 0, behavior: 'smooth' }
  }
})

export default router
