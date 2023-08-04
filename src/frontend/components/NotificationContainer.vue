<script setup lang="ts">
const { getNotifications } = useNotificationStore()
</script>

<template>
  <TransitionGroup
    tag="ul"
    class="fixed bottom-0 right-0 z-[100] flex flex-col gap-2 p-4" tabindex="-1"
    move-class="transition-all duration-300 ease-in-out"
    enter-active-class="transition-all duration-300 ease-in-out"
    leave-active-class="absolute transition-all duration-300 ease-in-out"
    enter-from-class="opacity-0 translate-x-40px"
    leave-to-class="opacity-0 translate-x-40px"
  >
    <Notification v-for="(n, index) in getNotifications()" :key="index" :noti="n" />
  </TransitionGroup>
</template>
