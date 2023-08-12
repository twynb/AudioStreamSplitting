<script setup lang="ts">
import { LangMap } from '../constants'

const { t } = useI18n()
const { currentLocal } = useLocale()

const localOpts = Object.entries(LangMap).map(([key, value]) => {
  return {
    label: value,
    value: key,
  }
})

const { isDark, toggle } = useDarkToggle()

function handleToggleDark() {
  if (!document.startViewTransition)
    toggle()

  document.startViewTransition(() => toggle())
}
</script>

<template>
  <ContentLayout :header="t('sidebar.settings')">
    <div class="max-w-80% space-y-10">
      <div>
        <h2 class="text-3xl">
          {{ t('settings.general.index') }}
        </h2>

        <BaseSeparator orientation="horizontal" />

        <div class="space-y-5">
          <div class="flex items-center justify-between">
            <h3>
              {{ t('settings.general.language') }}
            </h3>

            <BaseSelect
              v-model="currentLocal"
              :options="localOpts"
              class="w-200px"
            >
              <template #label>
                {{ LangMap[currentLocal] ?? '' }}
              </template>
            </BaseSelect>
          </div>

          <SettingsClear />
        </div>
      </div>

      <div>
        <h2 class="text-3xl">
          {{ t('settings.appearance.index') }}
        </h2>

        <BaseSeparator orientation="horizontal" />

        <div class="space-y-5">
          <div class="flex items-center justify-between">
            <h3>
              {{ t('settings.appearance.darkmode') }}
            </h3>

            <BaseSwitch v-model="isDark" :on-switch="handleToggleDark" />
          </div>
        </div>
      </div>
    </div>
  </ContentLayout>
</template>

<style>
::view-transition-group(root) {
  animation-duration: 1s;
}
::view-transition-new(root),
::view-transition-old(root) {
  mix-blend-mode: normal;
}

::view-transition-new(root) {
  animation-name: reveal-light;
}

::view-transition-old(root),
.dark::view-transition-old(root) {
  animation: none;
}
.dark::view-transition-new(root) {
  animation-name: reveal-dark;
}

@keyframes reveal-dark {
  from {
    clip-path: polygon(-30% 0, -30% 0, -15% 100%, -10% 115%);
  }
  to {
    clip-path: polygon(-30% 0, 130% 0, 115% 100%, -10% 115%);
  }
}

@keyframes reveal-light {
  from {
    clip-path: polygon(130% 0, 130% 0, 115% 100%, 110% 115%);
  }
  to {
    clip-path: polygon(130% 0, -30% 0, -15% 100%, 110% 115%);
  }
}
</style>
