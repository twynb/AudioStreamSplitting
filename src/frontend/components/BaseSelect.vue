<script setup lang="ts">
import { onClickOutside } from '@vueuse/core'

interface Option { label: string; value: string }

const props = defineProps<{
  /**
   * Placeholder for select
   */
  placeholder?: string
  /**
   * Array of options for select
   */
  options: Option[]
  /**
   * Is select disabled
   */
  disabled?: boolean
}>()

const modelValue = defineModel({ default: '' })
const index = ref(props.options.findIndex(o => o.value === modelValue.value) ?? 0)
const isExpanded = ref(false)
const isMouseOverOpts = ref(false)
const button = ref<HTMLButtonElement>()
onClickOutside(button, () => isExpanded.value = false)

function handleChooseOption(v: string, i: number) {
  modelValue.value = v
  index.value = i
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
      :disabled="disabled"
      class="h-10 w-full flex items-center justify-between border border-input rounded-md bg-transparent px-3 py-2 text-sm ring-offset-background disabled:cursor-not-allowed placeholder:text-muted-foreground disabled:opacity-50 focus:ring-2 focus:ring-offset-2 focus:ring-ring"
      @click="isExpanded = !isExpanded"
    >
      <span style="pointer-events: none">
        <!-- @slot Label for option
          @binding {number} index current index
        -->
        <slot name="label" :index="index">
          {{ options[index]?.label }}
        </slot>
      </span>
      <span class="i-carbon-caret-down" />
    </button>

    <Transition
      enter-active-class="transition-opacity"
      leave-active-class="transition-opacity"
      enter-from-class="opacity-0"
      leave-to-class="opacity-0"
    >
      <ul
        v-if="isExpanded"
        class="absolute right-0 top-full z-2 mt-1 w-full border border-input rounded-md bg-primary-foreground p-1 text-sm ring-offset-background disabled:cursor-not-allowed disabled:opacity-50"
        @mouseover="isMouseOverOpts = true"
        @mouseleave="isMouseOverOpts = false"
      >
        <li
          v-for="{ label, value }, i in options" :key="label"
          tabindex="0"
          class="flex items-center gap-x-2 rounded-md px-3 py-2 hover:(bg-secondary text-secondary-foreground)"
          :class="[!isMouseOverOpts && modelValue === value ? 'bg-secondary text-secondary-foreground' : 'bg-primary-foreground']"
          role="button"
          @click="handleChooseOption(value, i)"
          @keydown.enter.prevent="handleChooseOption(value, i)"
          @keydown.space.prevent="handleChooseOption(value, i)"
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

<docs>
   ## Examples
  ```vue
  <BaseSelect :options=[{label: "English",value: "en"}]>
    <template #label>
      Custom Label
    </template>
  </BaseSelect>
  ```
</docs>
