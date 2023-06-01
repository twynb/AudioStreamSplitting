<script setup lang="ts">
import SideBar from './components/SideBar.vue'
import MainComp from './components/MainComp.vue'
</script>

<template>
  <div class="relative min-h-[800px] min-w-[1200px] overflow-hidden">
    <div class="absolute inset-0 w-full h-full flex">
      <SideBar class="w-[270px] shrink-0" />

      <Suspense>
        <MainComp />
      </Suspense>
    </div>
  </div>
</template>

<style>
@font-face {
  font-family: 'Open Sans';
  src: local('Open Sans'), url(./assets/fonts/OpenSans.ttf) format('truetype');
}

body {
  overflow: hidden;
  font-family: 'Open Sans', sans-serif;
  @apply text-dark-gray dark:text-light-gray-2;
}
</style>
