<script setup lang="ts">
defineProps<{
  curr: number
  max: number
}>()
</script>

<template>
  <div aria-valuemax="100" aria-valuemin="0" role="progressbar" data-state="indeterminate" data-max="100" class="relative h-4 w-full overflow-hidden rounded-full bg-secondary">
    <div data-state="indeterminate" data-max="100" class="h-full w-full bg-primary transition-all" :style="{ transform: `translateX(${(curr * 100 / max) - 100}%)` }" />
  </div>
</template>
