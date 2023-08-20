<script setup lang="ts">
const props = defineProps<{
  header?: string
}>()

useDocTitle(props.header ?? '')
</script>

<template>
  <div
    class="wh-full space-y-11"
  >
    <slot name="header">
      <h1 v-if="header" class="text-4xl">
        {{ header }}
      </h1>
    </slot>

    <div
      class="wh-full"
    >
      <slot />
    </div>
  </div>
</template>
