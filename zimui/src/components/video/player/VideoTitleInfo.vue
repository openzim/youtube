<script setup lang="ts">
import { formatDate } from '@/utils/format-utils'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  publicationDate: {
    type: String,
    required: true
  }
})
</script>

<template>
  <v-row>
    <v-col class="d-flex flex-column py-2">
      <h2 class="video-title">{{ props.title }}</h2>
      <p class="video-date text-caption">Published on {{ formatDate(props.publicationDate) }}</p>
    </v-col>
  </v-row>
</template>
