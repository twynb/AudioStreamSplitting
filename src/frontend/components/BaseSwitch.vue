<script setup lang="ts">
const checked = defineModel({ default: false })
</script>

<template>
  <button
    type="button"
    role="switch"
    :aria-checked="!!checked"
    :data-state="checked ? 'checked' : 'unchecked'"
    value="on"
    class="h-[24px] w-[44px] inline-flex shrink-0 cursor-pointer items-center border-2 border-transparent rounded-full transition-colors disabled:cursor-not-allowed data-[state=checked]:bg-primary data-[state=unchecked]:bg-input disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-ring focus-visible:ring-offset-background"
    @click="checked = !checked"
  >
    <div
      :data-state="checked ? 'checked' : 'unchecked'"
      class="pointer-events-none block h-5 w-5 rounded-full bg-background shadow-lg ring-0 transition-transform data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0.25"
    >
      <div class="flex-center">
        <slot name="knob" />
      </div>
    </div>
  </button>
</template>
