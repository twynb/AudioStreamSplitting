<script setup lang="ts">
const modelValue = defineModel({ default: '' })
</script>

<template>
  <input
    v-model="modelValue"
    type="text"
    class="h-10 w-full flex border border-input rounded-md bg-primary-foreground px-3 py-2 text-sm ring-offset-background disabled:cursor-not-allowed placeholder:text-muted-foreground disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-ring"
    autocomplete="off"
  >
</template>

<docs>
   ## Examples
  ```vue
  <BaseInput v-model="inputValue" />
  ```
</docs>
