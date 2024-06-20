<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import errImage from '@/assets/images/dead-kiwix.png'

const main = useMainStore()
</script>

<template>
  <v-empty-state
    headline="Something went wrong"
    :title="main.errorMessage"
    :text="main.errorDetails"
    class="h-screen"
    :image="errImage"
  >
    <v-btn href="/" variant="tonal">Go back home</v-btn>
  </v-empty-state>
</template>

<style scoped>
.error-container {
  text-align: center;
  padding: 20px;
}

.error-image {
  width: 300px;
  margin-bottom: 20px;
}

.error-text {
  font-size: 16px;
}
</style>
