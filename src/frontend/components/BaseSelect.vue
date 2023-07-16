<script setup lang="ts">
import { onClickOutside } from '@vueuse/core'

defineProps<{
  placeholder: string
  options: {
    label: string
    value: string
  }[]
}>()

const modelValue = defineModel({ default: '' })
const isExpanded = ref(false)

function handleItemClick(value: string) {
  modelValue.value = value
  isExpanded.value = false
}

const button = ref<HTMLButtonElement>()
onClickOutside(button, () => isExpanded.value = false)
</script>

<template>
  <div>
    <button
      ref="button"
      type="button"
      role="combobox"
      :aria-expanded="isExpanded"
      class="h-10 w-full flex items-center justify-between border border-input rounded-md bg-transparent px-3 py-2 text-sm ring-offset-background disabled:cursor-not-allowed placeholder:text-muted-foreground disabled:opacity-50 focus:outline-none"
      @click="isExpanded = !isExpanded"
    >
      <span style="pointer-events: none">
        <slot name="label">
          {{ modelValue ?? placeholder }}
        </slot>
      </span>
      <span class="i-carbon-caret-down" />
    </button>

    <Transition
      enter-active-class="transition-all origin-top-right"
      leave-active-class="transition-all origin-top-right"
      enter-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-90"
    >
      <ul
        v-if="isExpanded"
        class="mt-1 border border-input rounded-md bg-transparent p-1 text-sm ring-offset-background disabled:cursor-not-allowed divide-y-1 divide-border disabled:opacity-50"
      >
        <li
          v-for="{ label, value } in options" :key="label"
          class="flex items-center gap-x-2 rounded-md px-3 py-2 hover:(bg-secondary text-secondary-foreground)"
          :class="{ 'bg-secondary text-secondary-foreground': modelValue === value }"
          role="button"
          @click="handleItemClick(value)"
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
