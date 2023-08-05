<script setup lang="ts">
import { DEFAULT_TOAST_DURATION } from '../constants'

const props = defineProps<{
  toast: Toast
}>()

const { removeToast } = useToastStore()
const width = ref(0)

const interval = setInterval(() => {
  width.value += 1
  if (width.value >= 100)
    clearInterval(interval)
}, (props.toast.duration ?? DEFAULT_TOAST_DURATION) / 100)
</script>

<template>
  <li
    class="group relative min-w-350px overflow-hidden border rounded-md p-6 pr-10"
    :class="{
      'border-border bg-background': toast.variant === 'default',
      'border-destructive bg-destructive text-destructive-foreground': toast.variant === 'destructive',
    }"
  >
    <slot>
      <div class="grid gap-3">
        <div v-if="toast.title" class="font-semibold">
          {{ toast.title }}
        </div>

        <div class="text-sm opacity-90">
          {{ toast.content }}
        </div>
      </div>
    </slot>

    <div class="absolute right-1 top-1 cursor-pointer p-2 opacity-0 transition-opacity group-hover:opacity-50 hover:!opacity-100" @click="removeToast(toast.id)">
      <span class="i-carbon-close" />
    </div>

    <div class="absolute bottom-0 left-0 h-1px bg-primary transition-width" :style="{ width: `${width}%` }" />
  </li>
</template>
