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
    class="relative min-h-3.5rem flex cursor-pointer items-center border-primary rounded-md p-4 text-primary transition-colors space-x-4 hover:bg-accent"
    :class="route.path === props.link ? 'bg-accent' : 'bg-background'"
    :title="text"
    @click="link && push({ path: link })"
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
      v-if="link === '/playground'" class="absolute transition-all" :class="[
        isSidebarMinimized ? '!w-4 !h-4 !text-xs right-1 top-1' : 'top-1/2 right-4 -translate-y-1/2',
      ]" content="1"
    />
  </li>
</template>
