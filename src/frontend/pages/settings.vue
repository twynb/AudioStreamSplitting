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

const { isDark } = useDarkToggle()
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

            <BaseSwitch v-model="isDark" />
          </div>
        </div>
      </div>
    </div>
  </ContentLayout>
</template>
