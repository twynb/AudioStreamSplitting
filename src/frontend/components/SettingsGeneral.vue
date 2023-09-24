<script setup lang="ts">
import { LangMap } from '../includes/constants'

const { t } = useI18n()

const { currentLocale } = useLocale()
const localOpts = Object.entries(LangMap).map(([key, value]) => ({ label: value, value: key }))

const { isDark } = useDarkToggle()
</script>

<template>
  <div>
    <h2 class="text-3xl">
      {{ t('settings.general.index') }}
    </h2>

    <BaseSeparator orientation="horizontal" />

    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <div class="max-w-1/2 space-y-1">
          <h3>{{ t('settings.general.language') }}</h3>
          <p class="text-balance text-sm text-muted-foreground">
            {{ t('settings.general.hint.language') }}
          </p>
        </div>

        <BaseSelect
          v-model="currentLocale"
          :options="localOpts"
          class="w-200px"
        />
      </div>

      <div class="flex items-center justify-between">
        <div class="max-w-1/2 space-y-1">
          <h3>{{ t('settings.general.darkmode') }}</h3>
          <p class="text-balance text-sm text-muted-foreground">
            {{ t('settings.general.hint.darkmode') }}
          </p>
        </div>

        <BaseSwitch v-model="isDark" />
      </div>
    </div>
  </div>
</template>
