<script setup lang="ts">
const APP_NAME = import.meta.env.VITE_APP_NAME
const { t } = useI18n()
const { isSidebarMinimized } = storeToRefs(useGlobalStyleStore())
const { getProjects } = useDBStore()
const dashboardBadgeCount = computed(() => getProjects().filter(({ visited }) => visited !== true).length)
</script>

<template>
  <nav
    class="h-full flex flex-col gap-y-10 bg-primary-foreground p-6 transition-width duration-150 ease-in"
    :class="[isSidebarMinimized ? 'w-105px' : 'w-[280px]']"
  >
    <div
      class="brand flex cursor-pointer items-center gap-x-3"
    >
      <div
        class="logo ml-2 h-11 w-11 flex shrink-0 items-center justify-center rounded-xl bg-primary"
      >
        <BaseLogo class="text-primary-foreground" />
      </div>
      <div
        v-if="!isSidebarMinimized"
        class="shrink-0 text-lg font-medium"
      >
        {{ APP_NAME }}
      </div>
    </div>

    <ul class="space-y-6">
      <SideBarRow
        icon="i-carbon-dashboard"
        :text="t('sidebar.dashboard')"
        link="/"
        :badge-count="dashboardBadgeCount"
      />

      <SideBarRow
        icon="i-carbon-activity"
        :text="t('sidebar.record')"
        link="/record"
      />
    </ul>

    <ul class="mt-auto">
      <li
        class="flex justify-center"
        @click="isSidebarMinimized = !isSidebarMinimized"
        @keydown.enter.prevent="isSidebarMinimized = !isSidebarMinimized"
        @keydown.space.prevent="isSidebarMinimized = !isSidebarMinimized"
      >
        <BaseButton
          variant="ghost" icon-only
        >
          <span
            class="text-sm"
            :class="isSidebarMinimized ? 'i-carbon:side-panel-open-filled' : 'i-carbon:side-panel-close-filled'"
          />
        </BaseButton>
      </li>

      <BaseSeparator orientation="horizontal" />

      <SideBarRow
        icon="i-carbon-settings"
        :text="t('sidebar.settings')"
        link="/settings"
      />
    </ul>
  </nav>
</template>

<docs>
  Main sidebar of application
</docs>
