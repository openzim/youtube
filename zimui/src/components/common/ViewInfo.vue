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
  }
})
</script>

<template>
  <v-container class="py-2 px-1" :fluid="mdAndDown">
    <v-row dense>
      <v-col cols="7">
        <p class="d-flex align-center text-body-2 text-wrap mx-4">{{ props.title }}</p>
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
