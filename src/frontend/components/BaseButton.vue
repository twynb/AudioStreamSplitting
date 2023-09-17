<script setup lang="ts">
const props = withDefaults(defineProps<{
  /**
   * Variant for the button
   */
  variant?: 'primary' | 'secondary' | 'destructive' | 'outline' | 'ghost'
  /**
   * Content is only icon
   */
  iconOnly?: boolean
  /**
   * Target if button works as a link
   */
  to?: string
}>(), {
  variant: 'primary',
  iconOnly: false,
})

const variantClass = computed(() => {
  switch (props.variant) {
    case 'primary':
      return 'bg-primary text-primary-foreground hover:bg-primary/90'
    case 'secondary':
      return 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
    case 'destructive':
      return 'bg-destructive text-destructive-foreground hover:bg-destructive/90'
    case 'outline':
      return 'border border-input bg-primary-foreground hover:bg-accent hover:text-accent-foreground focus-visible:outline-none'
    case 'ghost':
      return 'hover:bg-accent hover:text-accent-foreground focus-visible:outline-none'
  }
})
</script>

<template>
  <component
    :is="to ? 'a' : 'button'"
    :href="to"
    class="h-10 inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium ring-offset-background transition-colors disabled:pointer-events-none disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-ring"
    :class="[variantClass, { 'aspect-square !p-0': iconOnly }]"
  >
    <!-- @slot Slot for content -->
    <slot />
  </component>
</template>

<docs>
  ## Examples

  ```vue
  <BaseButton variant="primary">Button</BaseButton>

  <BaseButton variant="ghost" icon-only>x</BaseButton>
  ```
</docs>
