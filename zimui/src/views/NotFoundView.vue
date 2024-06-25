<script setup lang="ts">
import notFoundImg from '@/assets/images/dead-kiwix.png'
</script>

<template>
  <v-empty-state
    headline="Whoops, 404"
    title="Page not found"
    text="The page you were looking for does not exist"
    class="h-screen"
    :image="notFoundImg"
  ></v-empty-state>
</template>
