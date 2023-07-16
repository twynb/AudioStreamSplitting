<script setup lang="ts">
const { t } = useI18n()
const { isDark } = useDarkToggle()
const { isSidebarMinimized } = storeToRefs(useGlobalStyleStore())
</script>

<template>
  <div
    class="h-full flex flex-col gap-y-10 bg-background p-6 pb-8 transition-width"
    :class="[isSidebarMinimized ? 'w-105px items-center' : 'w-[280px]']"
  >
    <div
      class="brand flex cursor-pointer items-center gap-x-3"
      @click="isSidebarMinimized = !isSidebarMinimized"
    >
      <div
        class="logo h-11 w-11 flex shrink-0 items-center justify-center rounded-xl bg-primary"
      >
        <span
          class="i-carbon-play-filled-alt ml-0.5 text-xl text-primary-foreground"
        />
      </div>
      <div
        v-if="!isSidebarMinimized"
        class="shrink-0 text-lg font-medium"
      >
        LoremIpsum
      </div>
    </div>

    <ul class="space-y-6">
      <SideBarRow
        icon="i-carbon-dashboard"
        :text="t('sidebar.dashboard')"
        link="/"
      />

      <SideBarRow
        icon="i-carbon-chart-line-data"
        :text="t('sidebar.statistics')"
        link="/statistics"
      />

      <SideBarRow
        icon="i-carbon-3d-mpr-toggle"
        text="Playground"
        link="/playground"
      />
    </ul>

    <ul class="mt-auto space-y-2">
      <SideBarRow
        icon="i-carbon-settings"
        :text="t('sidebar.settings')"
        link="/settings"
      />

      <li
        class="py-3"
        :class="[
          isSidebarMinimized ? 'items-center px-0' : 'flex px-4 justify-between',
        ]"
      >
        <div class="flex gap-4">
          <span v-if="!isSidebarMinimized" :class="[isDark ? 'i-carbon-moon' : 'i-carbon-sun']" />

          <p v-if="!isSidebarMinimized">
            {{ t("sidebar.dark_mode") }}
          </p>
        </div>

        <BaseSwitch v-model="isDark" :class="[isSidebarMinimized ? 'ml-1' : '']">
          <template #knob>
            <div
              v-if="isSidebarMinimized"
              class="mt-0.5 text-sm text-sm text-xs"
              :class="[isDark ? 'i-carbon-moon' : 'i-carbon-sun']"
            />
          </template>
        </BaseSwitch>
      </li>
    </ul>
  </div>
</template>
