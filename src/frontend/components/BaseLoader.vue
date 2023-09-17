<script setup lang="ts">
withDefaults(defineProps<{
  /**
   * Size for the loader
   */
  size?: number
}>(), { size: 40 })
</script>

<template>
  <span
    class="loader border-3 border-primary border-b-transparent rounded-full"
    :style="{ width: `${size}px`, height: `${size}px` }"
  />
</template>

<style scoped>
/* https://cssloaders.github.io */
.loader {
  display: inline-block;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>

<docs>
   ## Examples
  ```vue
  <BaseLoader :size="10" />
  ```
</docs>
