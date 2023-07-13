<script setup lang="ts">
defineProps<{
  content: string
}>()
</script>

<template>
  <div v-if="content" class="pointer-events-none relative aspect-square h-5 w-5 select-none border border-transparent rounded-full bg-primary text-center text-xs font-semibold text-primary-foreground">
    <span class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
      {{ content }}
    </span>
  </div>
</template>
