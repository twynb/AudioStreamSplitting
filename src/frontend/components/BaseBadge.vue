<template>
  <div class="pointer-events-none aspect-square h-4 w-4 flex-center select-none border border-transparent rounded-full bg-primary text-center text-xs font-semibold text-primary-foreground">
    <!-- @slot Slot for content -->
    <slot />
  </div>
</template>

<docs>
  ## Examples

  ```vue
  <BaseBadge>1</BaseBadge>
  ```
</docs>
