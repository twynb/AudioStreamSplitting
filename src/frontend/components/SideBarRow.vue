<script setup lang="ts">
import { useGlobalStyle } from '../stores/useGloalStyle'

const props = defineProps<{
  icon: string
  text: string
  link?: string
}>()

const { isSidebarMinimized } = storeToRefs(useGlobalStyle())

const { push } = useRouter()
const route = useRoute()
</script>

<template>
  <li
    class="flex cursor-pointer items-center border-primary rounded-md p-4 text-primary transition-colors space-x-4 hover:(bg-accent)"
    :class="route.path === props.link ? 'bg-accent' : 'bg-background'"
    @click="link && push({ path: link })"
  >
    <span class="shrink-0" :class="icon" />
    <span v-if="!isSidebarMinimized" class="shrink-0">
      {{ text }}
    </span>

    <BaseBadge v-if="link === '/playground' && !isSidebarMinimized" class="mt-0.5" content="1" />
  </li>
</template>
