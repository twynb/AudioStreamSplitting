// https://cssloaders.github.io/

<script setup lang="ts">
const { size = 40 } = defineProps<{ size?: number }>()
</script>

<template>
  <span
    class="loader border-3 border-primary border-b-transparent rounded-full"
    :style="{ width: `${size}px`, height: `${size}px` }"
  />
</template>

<style scoped>
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
