<script setup lang="ts"></script>

<template>
  <button
    class="h-10 inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground ring-offset-background transition-colors disabled:pointer-events-none hover:bg-primary/90 disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-ring"
  >
    <slot />
  </button>
</template>
