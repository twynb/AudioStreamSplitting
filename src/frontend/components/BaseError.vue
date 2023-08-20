<script setup lang="ts">
defineProps<{
  error?: string
}>()
</script>

<template>
  <p v-if="error" class="text-sm text-destructive">
    {{ error }}
  </p>
</template>
