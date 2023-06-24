<script setup lang="ts">
const modelValue = defineModel({ default: '' })
</script>

<template>
  <input
    v-model="modelValue"
    class="h-10 w-full flex border border-input rounded-md bg-background px-3 py-2 text-sm ring-offset-background disabled:cursor-not-allowed file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-ring"
  >
</template>
