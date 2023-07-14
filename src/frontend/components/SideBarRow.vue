<script setup lang="ts">
const props = defineProps<{
  icon: string
  text: string
  link?: string
}>()

const { isSidebarMinimized } = storeToRefs(useGlobalStyleStore())

const { push } = useRouter()
const route = useRoute()
</script>

<template>
  <li
    class="relative flex cursor-pointer items-center border-primary rounded-md p-4 text-primary transition-colors space-x-4 hover:bg-accent"
    :class="route.path === props.link ? 'bg-accent' : 'bg-background'"
    @click="link && push({ path: link })"
  >
    <span class="shrink-0" :class="icon" />
    <span v-if="!isSidebarMinimized" class="shrink-0">
      {{ text }}
    </span>

    <BaseBadge
      v-if="link === '/playground'" class="absolute" :class="[
        isSidebarMinimized ? '!w-4 !h-4 !text-xs right-1 top-1' : 'top-1/2 right-0 -translate-y-1/2',
      ]" content="1"
    />
  </li>
</template>
