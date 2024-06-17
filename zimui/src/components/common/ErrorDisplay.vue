<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import errImage from '@/assets/images/dead-kiwix.png'

const main = useMainStore()
</script>

<template>
  <div class="error-container h-screen d-flex flex-column justify-center">
    <div>
      <img :src="errImage" class="error-image" />
      <p class="error-text">{{ main.errorMessage }}</p>
      <p class="error-text">{{ main.errorDetails }}</p>
    </div>
  </div>
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
