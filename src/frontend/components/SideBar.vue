<script setup lang="ts">
const SideBarRow = defineAsyncComponent(() => import("./SideBarRow.vue"));

const { t } = useI18n();
const {isDark,toggle} = useDarkToggle()
const { isSidebarMinimized } = storeToRefs(useGlobalStyle());
</script>

<template>
  <div class="flex h-full flex-col gap-y-10 bg-white p-6 pb-8 transition-width dark:bg-black"
    :class="[isSidebarMinimized ? 'w-[105px] items-center' : 'w-[280px]']">
    <div class="brand flex cursor-pointer items-center gap-x-3" @click="isSidebarMinimized = !isSidebarMinimized">
      <div class="logo flex h-11 w-11 items-center justify-center rounded-xl bg-black dark:bg-primary">
        <span class="i-carbon-flash-filled text-primary dark:text-black text-xl" />
      </div>
      <div class="text-lg font-medium" :class="[isSidebarMinimized ? 'hidden' : 'block']">
        Lorem Ipsum
      </div>
    </div>

    <ul class="menus space-y-6">
      <SideBarRow icon="i-carbon-dashboard" :text="t('sidebar.dashboard')" link="/" />

      <SideBarRow icon="i-carbon-document" :text="t('sidebar.current_project')" link="/current" />
    </ul>

    <ul class="settings mt-auto space-y-2">
      <SideBarRow icon="i-carbon-settings" :text="t('sidebar.settings')" link="/settings" />

      <li class="py-3" :class="[
        isSidebarMinimized
          ? ''
          : 'flex cursor-pointer items-center pl-4 pr-0',
      ]" @click="toggle()">
        <span class=" dark:text-primary"
          :class="[isSidebarMinimized ? 'hidden' : 'inline', isDark ? 'i-carbon-moon' : 'i-carbon-sun']" />
        <span class="ml-4" :class="[isSidebarMinimized ? 'hidden' : 'inline']">
          {{ t("sidebar.light_mode") }}
        </span>

        <div class="relative ml-auto h-8 w-14 rounded-2xl bg-primary dark:bg-dark-shade">
          <div
            class="absolute left-1 top-0.5 h-7 w-7 rounded-full bg-dark-gray dark:left-[calc(100%-33px)] dark:bg-primary flex items-center justify-center">
            <span v-if="isSidebarMinimized"
              :class="[isDark ? 'i-carbon-moon text-light-gray-2' : 'i-carbon-sun text-primary']" />
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>
