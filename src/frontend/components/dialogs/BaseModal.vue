<script setup lang="ts">
import { VueFinalModal } from 'vue-final-modal'

defineProps<{
  title: string
  contentClass?: string
}>()

const emits = defineEmits<{
  (e: 'closeWithX'): void
}>()
</script>

<template>
  <VueFinalModal
    overlay-class="-z-1 bg-#00000080 inset-0 pointer-events-none absolute"
    class="fixed inset-0 flex-center"
    :content-class="`rounded-sm p-6 bg-background focus:outline-none border border-border ${contentClass}`"
    overlay-transition="modal-fade"
    content-transition="modal-fade"
  >
    <slot name="header">
      <header class="flex items-center justify-between">
        <h2 class="text-2xl">
          {{ title }}
        </h2>

        <BaseButton variant="ghost" icon-only @click="emits('closeWithX')">
          <span class="i-carbon-close" />
        </BaseButton>
      </header>
    </slot>

    <div class="mt-5">
      <slot name="body" />
    </div>

    <div class="mt-5">
      <slot name="footer" />
    </div>
  </VueFinalModal>
</template>

<style>
@keyframes fade-in {
    0% {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
@keyframes fade-out {
    0% {
        opacity: 1;
    }
    to {
        opacity: 0;
    }
}
.modal-fade-enter-active {
    animation: fade-in 0.3s ease;
}
.modal-fade-leave-active {
    animation: fade-out 0.3s ease;
}
</style>
