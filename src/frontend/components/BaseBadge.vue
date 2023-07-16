<script setup lang="ts">
defineProps<{
  content: string
}>()
</script>

<template>
  <div v-if="content" class="pointer-events-none aspect-square h-5 w-5 flex-center select-none border border-transparent rounded-full bg-primary text-center text-xs font-semibold text-primary-foreground">
    {{ content }}
  </div>
</template>
