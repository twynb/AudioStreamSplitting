<script setup lang="ts">
import type { Component } from 'vue'

defineProps<{
  icon: Component
  text: string
}>()
</script>

<template>
  <li class="p-4 flex items-center space-x-4 cursor-pointer border-white transition-colors hover:-ml-[3px] hover:border-l-[3px] hover:border-primary">
    <component class="dark:text-primary" :is="icon" />
    <span> {{ text }} </span>
  </li>
</template>
