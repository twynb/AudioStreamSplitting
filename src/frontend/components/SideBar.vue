<script setup lang="ts">
import { defineAsyncComponent, ref } from 'vue'
import { useDark, useToggle } from '@vueuse/core'
import { useGlobalStyle } from '../store/useGloalStyle'
import { storeToRefs } from 'pinia'

const SideBarRow = defineAsyncComponent(() => import('./SideBarRow.vue'))
const IconBell = defineAsyncComponent(() => import('./icons/IconBell.vue'))
const IconFile = defineAsyncComponent(() => import('./icons/IconFile.vue'))
const IconHouse = defineAsyncComponent(() => import('./icons/IconHouse.vue'))
const IconLanguage = defineAsyncComponent(() => import('./icons/IconLanguage.vue'))
const IconSun = defineAsyncComponent(() => import('./icons/IconSun.vue'))
const IconMoon = defineAsyncComponent(() => import('./icons/IconMoon.vue'))
const IconMusicNote = defineAsyncComponent(() => import('./icons/IconMusicNote.vue'))

const tree = [
  {
    text: 'Dashboard',
    icon: IconHouse,
  },
  {
    text: 'Current Project',
    icon: IconFile,
  },
  {
    text: 'Notifications',
    icon: IconBell,
  },
]

const isDark = useDark()
const toggleDark = useToggle(isDark)

const { isSidebarMinimized } = storeToRefs(useGlobalStyle())
</script>

<template>
  <div class="h-full p-6 pb-8 flex flex-col gap-y-10 bg-white dark:bg-black transition-[width]" :class="[isSidebarMinimized ? 'w-[105px] items-center' : 'w-[270px]']">
    <div @click="isSidebarMinimized = !isSidebarMinimized" class="brand cursor-pointer flex items-center gap-x-3">
      <div class="logo w-11 h-11 rounded-xl bg-black dark:bg-primary flex items-center justify-center">
        <IconMusicNote height="28" width="28" class="dark:text-black text-primary" />
      </div>
      <div class="text-lg font-medium" :class="[isSidebarMinimized ? 'hidden' : 'block']">Lorem Ipsum</div>
    </div>

    <ul class="menus space-y-6">
      <SideBarRow :icon="icon" :text="text" v-for="({ icon, text }, index) in tree" :key="index" />
    </ul>

    <ul class="settings mt-auto space-y-2">
      <SideBarRow :icon="IconLanguage" text="Languages" />

      <li @click="toggleDark()" class="py-3" :class="[isSidebarMinimized ? '' : 'pl-4 pr-0 flex items-center cursor-pointer']">
        <component class="dark:text-primary" :class="[isSidebarMinimized ? 'hidden' : 'inline']" :is="IconSun" />
        <span class="ml-4" :class="[isSidebarMinimized ? 'hidden' : 'inline']"> Light mode </span>
        <div class="relative ml-auto w-14 h-8 rounded-2xl bg-primary dark:bg-dark-shade">
          <div class="absolute left-1 top-0.5 dark:left-[calc(100%-33px)] w-7 h-7 rounded-full bg-dark-gray dark:bg-primary">
            <component width="22" height="22" class="text-primary dark:text-dark-shade ml-[3px] mt-[3px]" :is="isDark ? IconSun : IconMoon" />
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>
