<script setup lang="ts">
const SideBarRow = defineAsyncComponent(() => import('./SideBarRow.vue'))

const { t } = useI18n()
const { isDark, toggle } = useDarkToggle()
const { isSidebarMinimized } = storeToRefs(useGlobalStyle())
</script>

<template>
  <div
    class="h-full flex flex-col gap-y-10 bg-background p-6 pb-8 transition-width"
    :class="[isSidebarMinimized ? 'w-[105px] items-center' : 'w-[280px]']"
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
        class="shrink-0 text-lg font-medium"
        :class="[isSidebarMinimized ? 'hidden' : 'block']"
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
          isSidebarMinimized
            ? ''
            : 'flex cursor-pointer items-center pl-4 pr-0',
        ]"
        @click="toggle()"
      >
        <span
          :class="[
            isSidebarMinimized ? 'hidden' : 'inline',
            isDark ? 'i-carbon-moon' : 'i-carbon-sun',
          ]"
        />
        <span class="ml-4" :class="[isSidebarMinimized ? 'hidden' : 'inline']">
          {{ t("sidebar.dark_mode") }}
        </span>

        <div
          class="relative ml-auto h-8 w-14 cursor-pointer rounded-2xl bg-primary"
        >
          <div
            class="absolute left-1 top-1 h-6 w-6 flex-center rounded-full bg-primary-foreground transition-transform dark:(translate-x-25px)"
          >
            <span
              v-if="isSidebarMinimized"
              class="text-sm text-primary"
              :class="[isDark ? 'i-carbon-moon' : 'i-carbon-sun']"
            />
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>
