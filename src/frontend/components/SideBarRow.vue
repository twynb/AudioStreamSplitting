<script setup lang="ts">
import { storeToRefs } from 'pinia'
import type { Component } from 'vue'
import { useGlobalStyle } from '../store/useGloalStyle'

defineProps<{
  icon: Component
  text: string
}>()

const { isSidebarMinimized } = storeToRefs(useGlobalStyle())
</script>

<template>
  <li class="p-4 flex items-center space-x-4 cursor-pointer border-white transition-colors hover:-ml-[3px] hover:border-l-[3px] hover:border-primary">
    <component class="dark:text-primary" :is="icon" />
    <span :class="[isSidebarMinimized ? 'hidden' : 'inline']"> {{ text }} </span>
  </li>
</template>
