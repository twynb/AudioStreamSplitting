<script setup lang="ts">
const { initialValue = 0 } = defineProps<{
  initialValue?: number
}>()

const emits = defineEmits<{
  (e: 'input', value: number): void
}>()

const currentValue = ref(initialValue)
const offset = ref(0)

function handleInput(event: Event) {
  const value = +(event.currentTarget as HTMLInputElement).value
  currentValue.value = value
  emits('input', value)
}
watch(currentValue, () => {
  offset.value = (currentValue.value / 5) - 2
}, { immediate: true })
</script>

<template>
  <div class="relative">
    <div class="absolute top-57% z-1 h-2 w-full rounded-full rounded-r-none bg-primary -translate-y-1/2" :style="{ width: `calc(${currentValue}%  - ${offset}px` }" />
    <input type="range" min="0" max="100" :value="currentValue" class="slider relative h-2 w-full rounded-full bg-secondary" @input="handleInput">
  </div>
</template>

<style scoped>
.slider::-webkit-slider-thumb {
  @apply w-4 h-4 rounded-full border-2 border-primary bg-background;
}

.slider::-moz-range-thumb {
  @apply w-4 h-4 rounded-full border-2 border-primary bg-background;
}
</style>
