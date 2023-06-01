<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { defineAsyncComponent } from 'vue'
import { useGlobalStyle } from './store/useGloalStyle'

const SideBar = defineAsyncComponent(() => import('./components/SideBar.vue'))
const MainComp = defineAsyncComponent(() => import('./components/MainComp.vue'))
</script>

<template>
  <div class="relative h-full w-full overflow-hidden">
    <div class="absolute inset-0 w-full h-full flex">
      <SideBar class="shrink-0" />

      <Suspense>
        <MainComp />
      </Suspense>
    </div>
  </div>
</template>
