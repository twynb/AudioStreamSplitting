<script setup lang="ts">
import { onClickOutside } from '@vueuse/core'

defineProps<{
  /**
   * Length of menu items
   */
  length: number
  /**
   * Is button disabled
   */
  disabled?: boolean
}>()
const isMenuOpen = ref(false)
const button = ref<HTMLButtonElement>()
onClickOutside(button, () => isMenuOpen.value = false)
</script>

<template>
  <div class="relative flex justify-end">
    <BaseButton
      ref="button" variant="ghost" icon-only :disabled="disabled"
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
      <div
        v-if="isMenuOpen"
        tabindex="0"
        class="absolute right-0 top-0 z-1 border border-border rounded-sm bg-primary-foreground py-1"
      >
        <ul>
          <li v-for="_, i in length" :key="i" class="px-1">
            <!-- @slot Slot for content
              @binding {number} index index of the menu item
            -->
            <slot name="content" :index="i" />
          </li>
        </ul>
      </div>
    </Transition>
  </div>
</template>
