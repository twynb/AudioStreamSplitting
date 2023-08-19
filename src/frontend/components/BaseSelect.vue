<script setup lang="ts">
import { onClickOutside } from '@vueuse/core'

defineProps<{
  placeholder?: string
  options: {
    label: string
    value: string
  }[]
}>()

const modelValue = defineModel({ default: '' })
const isExpanded = ref(false)
const isMouseOverOpts = ref(false)
const button = ref<HTMLButtonElement>()
onClickOutside(button, () => isExpanded.value = false)

function handleChooseOption(v: string) {
  modelValue.value = v
  isExpanded.value = false
  button.value?.focus()
}
</script>

<template>
  <div class="relative">
    <button
      ref="button"
      type="button"
      role="combobox"
      :aria-expanded="isExpanded"
      class="h-10 w-full flex items-center justify-between border border-input rounded-md bg-transparent px-3 py-2 text-sm ring-offset-background disabled:cursor-not-allowed placeholder:text-muted-foreground disabled:opacity-50 focus:ring-2 focus:ring-offset-2 focus:ring-ring"
      @click="isExpanded = !isExpanded"
    >
      <span style="pointer-events: none">
        <slot name="label">
          {{ modelValue ?? placeholder }}
        </slot>
      </span>
      <span class="i-carbon-caret-down" />
    </button>

    <!-- <select v-model="modelValue" class="absolute h-1px w-1px overflow-hidden border-none p-0 -m-1px" aria-hidden="true" tabindex="-1" style="clip: rect(0px, 0px, 0px, 0px);">
      <option value="" />
      <option v-for="{ label, value } in options" :key="value" :value="value">
        {{ label }}
      </option>
    </select> -->

    <Transition
      enter-active-class="transition-opacity"
      leave-active-class="transition-opacity"
      enter-from-class="opacity-0"
      leave-to-class="opacity-0"
    >
      <ul
        v-if="isExpanded"
        class="absolute right-0 top-full z-2 mt-1 w-full border border-input rounded-md bg-background p-1 text-sm ring-offset-background disabled:cursor-not-allowed disabled:opacity-50"
        @mouseover="isMouseOverOpts = true"
        @mouseleave="isMouseOverOpts = false"
      >
        <li
          v-for="{ label, value } in options" :key="label"
          tabindex="0"
          class="flex items-center gap-x-2 rounded-md px-3 py-2 hover:(bg-secondary text-secondary-foreground)"
          :class="[!isMouseOverOpts && modelValue === value ? 'bg-secondary text-secondary-foreground' : 'bg-background']"
          role="button"
          @click="handleChooseOption(value)"
          @keydown.enter.prevent="handleChooseOption(value)"
          @keydown.space.prevent="handleChooseOption(value)"
          @keydown.escape.prevent="isExpanded = false"
        >
          <span
            class="i-carbon-checkmark text-xs"
            :class="[modelValue === value ? 'visible' : 'invisible']"
          />

          <span>{{ label }}</span>
        </li>
      </ul>
    </Transition>
  </div>
</template>
