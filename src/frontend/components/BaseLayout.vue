<script setup lang="ts">
const props = defineProps<{
  /**
   * Header of layout
   */
  header: string
}>()

useDocTitle(props.header)
</script>

<template>
  <div class="wh-full space-y-11">
    <!-- @slot Slot for header -->
    <slot name="header">
      <h1 v-if="header" class="text-4xl font-semibold">
        {{ header }}
      </h1>
    </slot>

    <div class="wh-full">
      <!-- @slot Slot for content -->
      <slot />
    </div>
  </div>
</template>
