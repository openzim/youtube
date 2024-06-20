<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useMainStore } from '@/stores/main'
import { triggerWebpPolyfill } from './plugins/webp-hero'

import ErrorDisplay from '@/components/common/ErrorDisplay.vue'

const main = useMainStore()

onMounted(() => {
  triggerWebpPolyfill()
})
</script>

<template>
  <v-app>
    <v-main>
      <div v-if="main.errorMessage">
        <error-display />
      </div>
      <div v-else>
        <router-view />
      </div>
    </v-main>
  </v-app>
</template>

<style scoped></style>
