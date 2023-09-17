<script setup lang="ts">
defineProps<{
  /**
   * Orientation of separator
   */
  orientation: 'horizontal' | 'vertical'
}>()
</script>

<template>
  <div
    role="none" class="shrink-0 bg-border" :class="[
      orientation === 'horizontal' ? 'my-4 h-[1px] w-full' : 'h-full w-[1px]',
    ]"
  />
</template>

<docs>
   ## Examples
  ```vue
  <BaseSeparator orientation="vertical" />
  ```
</docs>
