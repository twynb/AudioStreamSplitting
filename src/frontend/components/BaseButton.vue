<script setup lang="ts">
const props = withDefaults(defineProps<{
  variant: 'primary' | 'secondary' | 'destructive' | 'outline' | 'ghost' | 'icon'
}>(), {
  variant: 'primary',
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
      return 'border border-input bg-background hover:bg-accent hover:text-accent-foreground focus-visible:outline-none'
    case 'ghost':
      return 'hover:bg-accent hover:text-accent-foreground focus-visible:outline-none'
  }
})
</script>

<template>
  <button
    class="h-10 inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium ring-offset-background transition-colors disabled:pointer-events-none disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-ring"
    :class="[variantClass]"
  >
    <slot />
  </button>
</template>
