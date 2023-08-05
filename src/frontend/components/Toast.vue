<script setup lang="ts">
import { TOAST_DURATION } from '../constants'

defineProps<{
  toast: Toast
}>()

const { removeToast } = useToastStore()
const width = ref(0)

const interval = setInterval(() => {
  width.value += 1
  if (width.value >= 100)
    clearInterval(interval)
}, TOAST_DURATION / 100)
</script>

<template>
  <li
    class="relative max-w-400px overflow-hidden border border-border rounded-md bg-background p-4 pr-8"
  >
    <slot>
      <div class="grid gap-3">
        <div class="font-semibold">
          {{ toast.title }}
        </div>

        <div class="text-sm opacity-90">
          {{ toast.content }}
        </div>
      </div>
    </slot>

    <BaseButton class="absolute right-1 top-1 scale-90" variant="ghost" icon-only @click="removeToast(toast.id)">
      <span class="i-carbon-close" />
    </BaseButton>

    <div class="absolute bottom-0 left-0 h-1px bg-primary" :style="{ width: `${width}%` }" />
  </li>
</template>
