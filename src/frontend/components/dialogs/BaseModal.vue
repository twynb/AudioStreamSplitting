<script setup lang="ts">
import { VueFinalModal } from 'vue-final-modal'

defineProps<{
  title?: string
  contentClass?: string
}>()
</script>

<template>
  <VueFinalModal
    overlay-class="-z-1 bg-#00000080 inset-0 pointer-events-none absolute"
    class="fixed inset-0 flex-center"
    :content-class="`rounded-sm p-6 bg-background focus:outline-none border border-border ${contentClass}`"
  >
    <slot name="header">
      <h2 class="text-2xl">
        {{ title }}
      </h2>
    </slot>

    <div class="mt-8">
      <slot name="body" />
    </div>

    <div class="mt-8">
      <slot name="footer" />
    </div>
  </VueFinalModal>
</template>
