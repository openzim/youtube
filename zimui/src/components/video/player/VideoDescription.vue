<script setup lang="ts">
import {computed} from "vue"
import {formatVideoDescription} from "@/utils/description-utils";

const props = defineProps({
  description: {
    type: String,
    required: true
  }
})

const description = computed(() => formatVideoDescription(props.description));
</script>

<template>
  <v-row>
    <v-col>
      <v-card class="border-thin py-2" rounded="lg" flat>
        <v-card-title class="text-subtitle-1 font-weight-medium">Description</v-card-title>
        <v-card-text class="video-description text-pre-wrap" v-if="description.length">
          <template v-for="(item, index) in description" :key="index">
            <component 
              :is="item[1] === 'a' ? 'a' : item[1] === 'br' ? 'br' : 'span'"
              v-bind="item[1] === 'a' ? { href: item[0], target: '_blank', rel: 'noopener noreferrer' } : {}"
            >
              {{ item[1] === 'br' ? '\n' : item[0] }}
            </component>
          </template>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>
