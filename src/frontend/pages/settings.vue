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
          General
        </h2>

        <BaseSeparator orientation="horizontal" />

        <div class="space-y-5">
          <div class="flex items-center justify-between">
            <h3>
              Languague
            </h3>

            <BaseSelect
              v-model="currentLocal"
              :placeholder="t('settings.languagues.placeholder')"
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
          Appearance
        </h2>

        <BaseSeparator orientation="horizontal" />

        <div class="space-y-5">
          <div class="flex items-center justify-between">
            <h3>
              Dark Mode
            </h3>

            <BaseSwitch v-model="isDark" />
          </div>
        </div>
      </div>
    </div>
  </ContentLayout>
</template>
