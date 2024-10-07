<script setup lang="ts">
import { useDisplay } from 'vuetify'

const { mdAndDown } = useDisplay()

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  count: {
    type: Number,
    required: true
  },
  countText: {
    type: String,
    required: true
  },
  icon: {
    type: String,
    required: true
  },
  videoSlug: {
    type: String,
    required: true
  },
  playlistSlug: {
    type: String,
    required: true
  }
})
</script>

<template>
  <v-container class="py-2 px-1" :fluid="mdAndDown">
    <v-row dense class="align-center">
      <v-col cols="7" class="d-flex align-center">
        <p
          class="text-body-2 text-wrap ml-4 mr-2 font-weight-medium title d-inline-block text-truncate"
        >
          <router-link
            :to="{
              name: 'view-playlist',
              params: { slug: props.playlistSlug }
            }"
            class="text-black"
          >
            {{ props.title }}
          </router-link>
        </p>
        <v-btn
          size="small"
          variant="text"
          :to="{
            name: 'watch-video',
            params: { slug: props.videoSlug },
            query: { list: props.playlistSlug }
          }"
        >
          <template #prepend>
            <v-icon size="small" icon="mdi-play" />
          </template>
          Play all
        </v-btn>
      </v-col>
      <v-col cols="5">
        <p class="d-flex align-center text-body-2 text-wrap mx-4 justify-end">
          <v-icon class="mr-1" size="small" :icon="props.icon"></v-icon>
          {{ props.count }} {{ props.countText }}
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.title:hover {
  text-decoration: underline;
}
</style>
