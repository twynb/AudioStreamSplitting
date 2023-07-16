<script setup lang="ts">
</script>

<template>
  <div
    class="group pointer-events-none relative h-full flex flex-col border border-border rounded-sm p-3 hover:border-accent-foreground"
  >
    <header class="space-y-1">
      <div class="flex items-center justify-between">
        <BaseSkeleton class="h-24px w-80px" />

        <BaseButton variant="ghost" icon-only>
          <span class="i-carbon-overflow-menu-vertical" />
        </BaseButton>
      </div>
      <BaseSkeleton class="h-24px w-300px" />
    </header>

    <div class="my-5">
      <BaseSkeleton class="h-16px w-full" />
    </div>

    <BaseSkeleton class="h-19px w-200px" />
  </div>
</template>
