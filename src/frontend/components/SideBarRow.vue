<script setup lang="ts">
import { useGlobalStyle } from "../stores/useGloalStyle";

defineProps<{
  icon: string;
  text: string;
  link?: string
}>();

const { isSidebarMinimized } = storeToRefs(useGlobalStyle());

const { push } = useRouter()
</script>

<template>
  <li
    class="flex cursor-pointer items-center space-x-4 border-white p-4 transition-colors hover:(-ml-[3px] border-l-[3px] border-primary)"
    @click="link && push({ path: link })">
    <span :class="icon" class="dark:text-primary" />
    <span :class="[isSidebarMinimized ? 'hidden' : 'inline']">
      {{ text }}
    </span>
  </li>
</template>
