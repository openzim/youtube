<script setup lang="ts">
const props = defineProps({
  description: {
    type: String,
    required: true
  }
})
</script>

<template>
  <v-row>
    <v-col>
      <v-card class="border-thin py-2" rounded="lg" flat>
        <v-card-title class="text-subtitle-1 font-weight-medium">Description</v-card-title>
        <v-card-text class="video-description text-pre-wrap">{{ props.description }}</v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>
