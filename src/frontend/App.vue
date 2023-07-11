<script setup lang="ts">
const SideBar = defineAsyncComponent(() => import('./components/SideBar.vue'))

const { toggleLocales, currentLocal } = useLocale()
toggleLocales(currentLocal.value)
</script>

<template>
  <div class="relative wh-full overflow-hidden">
    <div class="absolute inset-0 wh-full flex divide-x-1 divide-border">
      <SideBar class="shrink-0" />

      <Suspense>
        <div class="wh-full bg-background p-6 pb-8">
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
  user-select: none;
  font-family: 'Open Sans', sans-serif;
  @apply text-primary;
}
</style>
