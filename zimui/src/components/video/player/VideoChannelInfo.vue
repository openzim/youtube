<script setup lang="ts">
import profilePlaceholder from '@/assets/images/profile-placeholder.jpg'
import AboutDialogButton from '@/components/channel/AboutDialogButton.vue'

const props = defineProps({
  profilePath: {
    type: String,
    required: true
  },
  channelTitle: {
    type: String,
    required: true
  },
  channelDescription: {
    type: String,
    required: true
  },
  joinedDate: {
    type: String,
    required: true
  }
})
</script>

<template>
  <v-row>
    <v-col cols="6" class="d-flex align-center py-2">
      <router-link :to="{ name: 'home' }">
        <v-avatar size="50" class="border-thin">
          <v-img :src="props.profilePath" :lazy-src="profilePlaceholder" />
        </v-avatar>
        <span class="video-channel ml-2 font-weight-medium">{{ props.channelTitle }}</span>
      </router-link>
    </v-col>
    <v-col cols="6" class="d-flex justify-end align-center">
      <about-dialog-button
        :title="props.channelTitle"
        :description="props.channelDescription"
        :joined-date="props.joinedDate"
      />
    </v-col>
  </v-row>
</template>

<style scoped>
.video-channel {
  color: initial;
}
</style>
