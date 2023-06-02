<script setup lang="ts">
const SideBar = defineAsyncComponent(() => import('./components/SideBar.vue'))
const MainComp = defineAsyncComponent(() => import('./components/MainComp.vue'))
</script>

<template>
  <div class="relative h-full w-full overflow-hidden">
    <div class="absolute inset-0 flex h-full w-full">
      <SideBar class="shrink-0" />

      <Suspense>
        <MainComp />
      </Suspense>
    </div>
  </div>
</template>
