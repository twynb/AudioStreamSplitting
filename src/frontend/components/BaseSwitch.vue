<script setup lang="ts">
defineProps<{
  id: string;
  label: string;
}>();
const checked = ref(false);
</script>

<template>
  <div class="flex items-center gap-x-2">
    <button
      type="button"
      role="switch"
      :aria-checked="!!checked"
      :data-state="checked ? 'checked' : 'unchecked'"
      value="on"
      class="peer inline-flex h-[24px] w-[44px] shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=unchecked]:bg-input"
      @click="checked = !checked"
      :id="id"
    >
      <span
        :data-state="checked ? 'checked' : 'unchecked'"
        class="pointer-events-none block h-5 w-5 rounded-full bg-background shadow-lg ring-0 transition-transform data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0.25"
      >
      </span>
    </button>

    <label
      class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
      :for="id"
    >
      {{ label }}
    </label>
  </div>
</template>
