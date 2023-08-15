<script setup lang="ts">
const props = defineProps<{
  icon: string
  text: string
  link?: string
  badgeCount?: number
}>()

const { isSidebarMinimized } = storeToRefs(useGlobalStyleStore())

const { push } = useRouter()
const route = useRoute()
</script>

<template>
  <li
    class="relative min-h-3.5rem flex cursor-pointer items-center border-primary rounded-md p-4 text-primary transition-colors space-x-4 hover:bg-accent"
    tabindex="1"
    :class="route.path === props.link ? 'bg-accent' : 'bg-background'"
    :title="text"
    @click="link && push({ path: link })"
    @keydown.enter.prevent="link && push({ path: link })"
    @keydown.space.prevent="link && push({ path: link })"
  >
    <span class="shrink-0 text-lg" :class="icon" />

    <Transition
      enter-active-class="transition-opacity duration-200"
      leave-active-class="transition-opacity duration-200"
      enter-from-class="opacity-0"
      leave-to-class="opacity-0"
    >
      <span v-if="!isSidebarMinimized" class="shrink-0">
        {{ text }}
      </span>
    </Transition>

    <BaseBadge
      v-if="badgeCount" class="absolute transition-all" :class="[
        isSidebarMinimized ? '!text-xs right-1 top-1' : 'top-1/2 right-4 -translate-y-1/2',
      ]"
    >
      {{ badgeCount }}
    </BaseBadge>
  </li>
</template>
