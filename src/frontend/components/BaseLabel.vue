<script setup lang="ts">
defineProps<{
  hasError?: boolean
}>()
</script>

<template>
  <label
    class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
    :class="{ 'text-destructive': hasError }"
  >
    <slot />
  </label>
</template>
