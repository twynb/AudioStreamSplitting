<script setup lang="ts">
defineProps<{
  /**
   * If label is for error field
   */
  hasError?: boolean
}>()
</script>

<template>
  <label
    class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
    :class="{ 'text-destructive': hasError }"
  >
    <!-- @slot Slot for content -->
    <slot />
  </label>
</template>

<docs>
   ## Examples
  ```vue
  <BaseLabel for="name">Label for name</BaseLabel>
  ```
</docs>
