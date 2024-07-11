<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useDisplay } from 'vuetify'

import AboutDialogButton from '@/components/channel/AboutDialogButton.vue'
import { useMainStore } from '@/stores/main'

import profilePlaceholder from '@/assets/images/profile-placeholder.jpg'

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

const tabs = [
  {
    id: 0,
    title: 'Videos',
    to: { name: 'videos' }
  },
  {
    id: 1,
    title: 'Playlists',
    to: { name: 'playlists' }
  }
]

const tab = ref<number>(tabs[0].id)
</script>

<template>
  <v-container class="pt-0 pt-md-4 px-0 px-md-4" :fluid="mdAndDown">
    <v-card flat class="header-card border-thin border-t-0 rounded-lg">
      <!-- Banner -->
      <v-parallax
        :scale="1"
        height="120"
        class="banner-bg rounded-lg rounded-t-0"
        :src="main.channel?.bannerPath"
      ></v-parallax>

      <!-- Channel Info -->
      <v-container class="channel-info px-8" :fluid="mdAndDown">
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
      <v-tabs v-if="tabs.length > 0" v-model="tab" align-tabs="center">
        <v-tab v-for="item in tabs" :key="item.id" :to="item.to">
          {{ item.title }}
        </v-tab>
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
