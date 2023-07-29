<script setup lang="ts">
import { useEventListener } from '@vueuse/core'

const value = defineModel({ default: 0 })

const track = ref<HTMLDivElement>()
const thumb = ref<HTMLDivElement>()

const isDragging = ref(false)
useEventListener(document, 'mouseup', () => {
  isDragging.value = false
})

useEventListener(document, 'mousemove', (e) => {
  if (!isDragging.value)
    return

  if (!track.value || !thumb.value)
    return

  const rect = track.value.getBoundingClientRect()
  const x = e.clientX - rect.left
  const maxX = rect.width - thumb.value.clientWidth
  const xPos = Math.min(Math.max(0, x), maxX)

  value.value = Math.floor(xPos * 100 / maxX)
})
</script>

<template>
  <div
    ref="track"
    dir="ltr"
    data-orientation="horizontal"
    aria-disabled="false"
    class="relative w-full flex touch-none select-none items-center"
  >
    <div
      data-orientation="horizontal"
      class="relative h-2 w-full grow overflow-hidden rounded-full bg-secondary"
    >
      <span
        data-orientation="horizontal"
        class="absolute left-0 h-full bg-primary"
        :style="{ right: `${100 - value}%` }"
      />
    </div>
    <div
      class="absolute"
      :style="{
        transform: `translate(-${value}%)`,
        left: `${value}%`,
      }"
    >
      <div
        ref="thumb"
        role="slider"
        aria-valuemin="0"
        aria-valuemax="100"
        aria-orientation="horizontal"
        data-orientation="horizontal"
        tabindex="0"
        class="h-5 w-5 border-2 border-primary rounded-full bg-background ring-offset-background transition-colors disabled:pointer-events-none disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-ring"
        :aria-valuenow="value"
        @mousedown="isDragging = true"
      />
    </div>
  </div>
</template>
