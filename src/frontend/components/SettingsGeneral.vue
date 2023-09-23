<script setup lang="ts">
import { useLocalStorage } from '@vueuse/core'
import { LangMap, SUPPORT_FILE_TYPES } from '../includes/constants'

const { t } = useI18n()

const { currentLocale } = useLocale()
const localOpts = Object.entries(LangMap).map(([key, value]) => ({ label: value, value: key }))

const saveSettings = useLocalStorage('save-settings', { fileType: 'mp3', shouldAsk: true, submitSavedFiles: false })
</script>

<template>
  <div>
    <h2 class="text-3xl">
      {{ t('settings.general.index') }}
    </h2>

    <BaseSeparator orientation="horizontal" />

    <div class="space-y-5">
      <div class="flex items-center justify-between">
        <h3>{{ t('settings.general.language') }}</h3>

        <BaseSelect
          v-model="currentLocale"
          :options="localOpts"
          class="w-200px"
        />
      </div>

      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <h3 :class="{ 'text-muted-foreground': saveSettings.shouldAsk }">
            {{ t('settings.general.save_file_type') }}
          </h3>

          <BaseSelect v-model="saveSettings.fileType" class="min-w-100px" :options="SUPPORT_FILE_TYPES.map(t => ({ label: t, value: t }))" :disabled="saveSettings.shouldAsk" />
        </div>

        <div class="flex items-center justify-between">
          <h3>{{ t('settings.general.ask_file_type') }}</h3>

          <BaseSwitch v-model="saveSettings.shouldAsk" />
        </div>
      </div>
    </div>
  </div>
</template>
