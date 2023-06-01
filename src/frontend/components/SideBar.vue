<script setup lang="ts">
import { defineAsyncComponent } from 'vue'
import { useDark, useToggle } from '@vueuse/core'
import { storeToRefs } from 'pinia'
import { useGlobalStyle } from '../store/useGloalStyle'

const SideBarRow = defineAsyncComponent(() => import('./SideBarRow.vue'))
const IconBell = defineAsyncComponent(() => import('./icons/IconBell.vue'))
const IconFile = defineAsyncComponent(() => import('./icons/IconFile.vue'))
const IconHouse = defineAsyncComponent(() => import('./icons/IconHouse.vue'))
const IconLanguage = defineAsyncComponent(
  () => import('./icons/IconLanguage.vue'),
)
const IconSun = defineAsyncComponent(() => import('./icons/IconSun.vue'))
const IconMoon = defineAsyncComponent(() => import('./icons/IconMoon.vue'))
const IconMusicNote = defineAsyncComponent(
  () => import('./icons/IconMusicNote.vue'),
)

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
  <div
    class="flex h-full flex-col gap-y-10 bg-white p-6 pb-8 transition-[width] dark:bg-black"
    :class="[isSidebarMinimized ? 'w-[105px] items-center' : 'w-[270px]']"
  >
    <div
      class="brand flex cursor-pointer items-center gap-x-3"
      @click="isSidebarMinimized = !isSidebarMinimized"
    >
      <div
        class="logo flex h-11 w-11 items-center justify-center rounded-xl bg-black dark:bg-primary"
      >
        <IconMusicNote
          height="28"
          width="28"
          class="text-primary dark:text-black"
        />
      </div>
      <div
        class="text-lg font-medium"
        :class="[isSidebarMinimized ? 'hidden' : 'block']"
      >
        Lorem Ipsum
      </div>
    </div>

    <ul class="menus space-y-6">
      <SideBarRow
        v-for="({ icon, text }, index) in tree"
        :key="index"
        :icon="icon"
        :text="text"
      />
    </ul>

    <ul class="settings mt-auto space-y-2">
      <SideBarRow :icon="IconLanguage" text="Languages" />

      <li
        class="py-3"
        :class="[
          isSidebarMinimized
            ? ''
            : 'flex cursor-pointer items-center pl-4 pr-0',
        ]"
        @click="toggleDark()"
      >
        <component
          :is="IconSun"
          class="dark:text-primary"
          :class="[isSidebarMinimized ? 'hidden' : 'inline']"
        />
        <span class="ml-4" :class="[isSidebarMinimized ? 'hidden' : 'inline']">
          Light mode
        </span>
        <div
          class="relative ml-auto h-8 w-14 rounded-2xl bg-primary dark:bg-dark-shade"
        >
          <div
            class="absolute left-1 top-0.5 h-7 w-7 rounded-full bg-dark-gray dark:left-[calc(100%-33px)] dark:bg-primary"
          >
            <component
              :is="isDark ? IconSun : IconMoon"
              width="22"
              height="22"
              class="ml-[3px] mt-[3px] text-primary dark:text-dark-shade"
            />
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>
