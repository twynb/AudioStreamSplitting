<script setup lang="ts">
import { onClickOutside } from '@vueuse/core'
import BaseButton from './BaseButton.vue'

type BaseButtonProps = (InstanceType<typeof BaseButton>)['$props']

withDefaults(defineProps<{
  /**
   * Length of menu items
   */
  length: number
  /**
   * Is button disabled
   */
  disabled?: boolean
  /**
   * Variant for the button
   */
  variant?: BaseButtonProps['variant']
  /**
   * Content is only icon
   */
  iconOnly?: BaseButtonProps['iconOnly']
  /**
   * Class for menu
   */
  menuClass?: string
}>(), { variant: 'ghost', iconOnly: true })

const emits = defineEmits<{
  /**
   * Triggers when menu is open
   * @property {boolean} state current state of menu
   */
  (e: 'toggleMenu', state: boolean): void
}>()

const isMenuOpen = ref(false)
watch(isMenuOpen, () => emits('toggleMenu', isMenuOpen.value))
const button = ref<HTMLButtonElement>()
onClickOutside(button, () => isMenuOpen.value = false)
</script>

<template>
  <div class="relative flex justify-end">
    <BaseButton
      ref="button" :variant="variant" :icon-only="iconOnly" :disabled="disabled"
      @click.stop="isMenuOpen = true"
      @keydown.enter.stop="isMenuOpen = true"
      @keydown.space.stop="isMenuOpen = true"
      @keydown.escape.stop="isMenuOpen = false"
    >
      <slot name="button" />
    </BaseButton>

    <Transition
      enter-active-class="transition-all origin-top-right"
      leave-active-class="transition-all origin-top-right"
      enter-from-class="opacity-0 scale-90"
      leave-to-class="opacity-0 scale-90"
    >
      <ul
        v-if="isMenuOpen"
        tabindex="0"
        class="absolute right-0 top-0 border border-border rounded-sm bg-primary-foreground py-1"
        :class="[menuClass, isMenuOpen ? 'z-2' : 'z-0']"
      >
        <li v-for="_, i in length" :key="i" class="px-1">
          <!-- @slot Slot for content
              @binding {number} index index of the menu item
            -->
          <slot name="content" :index="i" />
        </li>
      </ul>
    </Transition>
  </div>
</template>
