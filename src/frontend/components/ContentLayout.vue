<script setup lang="ts">
defineProps<{
  header: string
}>()
</script>

<template>
  <div class="space-y-11">
    <h1 class="text-4xl">
      {{ header }}
    </h1>

    <div>
      <slot />
    </div>
  </div>
</template>
