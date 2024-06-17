<script setup lang="ts">
import { formatDate } from '@/utils/format-utils'
import { ref, computed } from 'vue'

const dialog = ref<boolean>(false)
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  joinedDate: {
    type: String,
    required: true
  }
})

const notAvailable = 'Not available'

const formattedDate = computed(() => {
  if (!props.joinedDate) return notAvailable
  return formatDate(props.joinedDate)
})
</script>

<template>
  <v-btn class="border-thin" flat @click="dialog = true">
    <v-icon icon="mdi-information-outline" start></v-icon>
    About Channel
  </v-btn>
  <v-dialog v-model="dialog" width="500">
    <v-card prepend-icon="mdi-information-outline" title="About" class="rounded-lg">
      <v-card-text>
        <v-row>
          <v-col cols="12">
            <p class="text-h6">Channel</p>
            <p>{{ props.title || notAvailable }}</p>
          </v-col>
          <v-col cols="12">
            <p class="text-h6">Description</p>
            <p>{{ props.description || notAvailable }}</p>
          </v-col>
          <v-col cols="12">
            <p class="text-h6">Joined Date</p>
            <p>{{ formattedDate }}</p>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn class="ms-auto" @click="dialog = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
