<script setup lang="ts">
defineProps<{
  header: string
}>()
</script>

<template>
  <div class="space-y-14">
    <header class="text-4xl">
      {{ header }}
    </header>

    <div>
      <slot />
    </div>
  </div>
</template>
