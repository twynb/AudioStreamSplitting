<script setup lang="ts">
import { VueFinalModal } from 'vue-final-modal'
</script>

<template>
  <VueFinalModal
    overlay-class="-z-1 bg-#00000080 inset-0 pointer-events-none absolute"
    class="fixed inset-0 flex-center"
    content-class="rounded-sm p-6 bg-background focus:outline-none border border-border"
    overlay-transition="modal-fade"
    content-transition="modal-fade"
  >
    <slot />
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
