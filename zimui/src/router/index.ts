import { createRouter, createWebHashHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import VideoPlayerView from '../views/VideoPlayerView.vue'
import NotFoundView from '../views/NotFoundView.vue'

import VideosTab from '@/components/channel/tabs/VideosTab.vue'
import PlaylistsTab from '@/components/channel/tabs/PlaylistsTab.vue'
import PlaylistView from '@/views/PlaylistView.vue'

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
