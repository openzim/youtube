<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useDisplay } from 'vuetify'

import AboutDialogButton from '@/components/channel/AboutDialogButton.vue'
import { useMainStore } from '@/stores/main'

import profilePlaceholder from '@/assets/images/profile-placeholder.jpg'
import bannerOverlay from '@/assets/images/banner-overlay.png'

const { mdAndDown } = useDisplay()

// Fetch the channel data
const main = useMainStore()
onMounted(async () => {
  try {
    await main.fetchChannel()
  } catch (error) {
    main.setErrorMessage('An unexpected error occured.')
  }
})

// Computed tabs array based on store data
const tabs = computed(() => {
  const baseTabs = [
    { id: 0, title: 'Home', to: { name: 'home' } }
  ];

  if (main.channel?.userLongUploadsPlaylist) {
    baseTabs.push({ id: 1, title: 'Videos', to: { name: 'videos' } });
  }

  if (main.channel?.userShortUploadsPlaylist) {
    baseTabs.push({ id: 2, title: 'Shorts', to: { name: 'shorts' } });
  }

  if (main.channel?.userLivesPlaylist) {
    baseTabs.push({ id: 3, title: 'Lives', to: { name: 'lives' } });
  }

  baseTabs.push({ id: 4, title: 'Playlists', to: { name: 'playlists' } });

  return baseTabs;
});


// Hide tabs if there is only one playlist
const hideTabs = computed(() => main.channel?.playlistCount === 1)

const tab = ref<number>(tabs.value[0]?.id || 0);
</script>

<template>
  <v-container class="pt-0 pt-md-4 px-0 px-md-4" :fluid="mdAndDown">
    <v-card flat class="header-card border-thin border-t-0 rounded-lg">
      <!-- Banner -->
      <v-parallax
        :scale="1"
        height="120"
        class="banner-bg rounded-lg rounded-t-0"
        :lazy-src="bannerOverlay"
        :src="main.channel?.bannerPath"
      ></v-parallax>

      <!-- Channel Info -->
      <v-container class="channel-info px-8" :class="{ 'py-8': hideTabs }" :fluid="mdAndDown">
        <v-row>
          <v-col cols="12" md="8" class="d-flex flex-column flex-md-row align-center">
            <v-avatar size="75" class="channel-avatar border-thin">
              <v-img
                :lazy-src="profilePlaceholder"
                :src="main.channel?.profilePath"
                alt="Channel Avatar"
              />
            </v-avatar>
            <v-card-title class="channel-title text-h5 font-weight-medium">
              {{ main.channel?.channelName }}
            </v-card-title>
          </v-col>
          <v-col
            cols="12"
            md="4"
            class="d-flex align-center justify-center justify-md-end pt-0 pt-md-3"
          >
            <about-dialog-button
              :title="main.channel?.channelName || ''"
              :description="main.channel?.channelDescription || ''"
              :joined-date="main.channel?.joinedDate || ''"
            />
          </v-col>
        </v-row>
      </v-container>

      <!-- Tabs Navigation -->
      <v-tabs v-if="!hideTabs" v-model="tab" align-tabs="center">
        <router-link v-for="item in tabs" :key="item.id" :to="item.to" class="text-black">
          <v-tab :to="item.to">
            {{ item.title }}
          </v-tab>
        </router-link>
      </v-tabs>
    </v-card>
  </v-container>
</template>

<style scoped>
/* Make border zero on .header-card for mobile screens less that 960 px*/
@media (max-width: 960px) {
  .header-card {
    border-left: 0 !important;
    border-right: 0 !important;
    border-top-left-radius: 0 !important;
    border-top-right-radius: 0 !important;
  }
}

.banner-bg {
  background: rgb(var(--v-theme-primary));
  background: linear-gradient(
    120deg,
    rgba(var(--v-theme-primary-darken-1)) 0%,
    rgba(var(--v-theme-primary)) 50%,
    rgba(var(--v-theme-primary-lighten-1)) 100%
  );
}
</style>
