<script setup lang="ts">
import { ModalsContainer } from 'vue-final-modal'
import { handleAppInit } from './includes/utils'

handleAppInit()
</script>

<template>
  <div class="relative wh-full overflow-hidden">
    <div class="absolute inset-0 wh-full flex divide-x-1 divide-border">
      <SideBar class="shrink-0" />

      <Suspense>
        <div class="wh-full overflow-x-hidden overflow-y-scroll bg-primary-foreground p-6 pb-8">
          <RouterView />
        </div>
      </Suspense>
    </div>

    <ModalsContainer />

    <ToastContainer />
  </div>
</template>
