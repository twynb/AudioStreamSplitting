<script setup lang="ts">
import type { Component } from 'vue'

defineProps<{
  icon: Component
  text: string
}>()

const { isSidebarMinimized } = storeToRefs(useGlobalStyle())
</script>

<template>
  <li
    class="flex cursor-pointer items-center space-x-4 border-white p-4 transition-colors hover:-ml-[3px] hover:border-l-[3px] hover:border-primary"
  >
    <component :is="icon" class="dark:text-primary" />
    <span :class="[isSidebarMinimized ? 'hidden' : 'inline']">
      {{ text }}
    </span>
  </li>
</template>
