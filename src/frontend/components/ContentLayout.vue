<script setup lang="ts">
defineProps<{
  header?: string
}>()
</script>

<template>
  <div class="space-y-11">
    <slot name="header">
      <h1 v-if="header" class="text-4xl">
        {{ header }}
      </h1>
    </slot>

    <div>
      <slot />
    </div>
  </div>
</template>
