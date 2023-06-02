<script setup lang="ts">
const SideBar = defineAsyncComponent(() => import('./components/SideBar.vue'))
</script>

<template>
  <div class="relative h-full w-full overflow-hidden">
    <div class="absolute inset-0 flex h-full w-full">
      <SideBar class="shrink-0" />

      <Suspense>
        <div class="h-full w-full bg-light-gray-2 dark:bg-dark-shade p-6 pb-8">
          <RouterView />
        </div>
      </Suspense>
    </div>
  </div>
</template>


<style>
html,
body,
#app {
  height: 100%;
  margin: 0;
  padding: 0;
}

@font-face {
  font-family: 'Open Sans';
  src: local('Open Sans'), url(./assets/fonts/OpenSans.ttf) format('truetype');
}


body{
  overflow: hidden;
  font-family: 'Open Sans', sans-serif;
  @apply text-dark-gray dark:text-light-gray-2;
}

</style>
