<script setup lang="ts">
import { useLocalStorage } from '@vueuse/core'
import { LangMap, SUPPORT_FILE_TYPES } from '../includes/constants'

const { t } = useI18n()

const { currentLocal } = useLocale()
const localOpts = Object.entries(LangMap).map(([key, value]) => ({ label: value, value: key }))

const preferredFileType = useLocalStorage('preferred-file-type', { fileType: 'mp3', enable: false })
</script>

<template>
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
        />
      </div>

      <div class="flex items-center justify-between">
        <h3>
          {{ t('settings.general.preferred_file_type') }}
        </h3>

        <div class="h-40px flex items-center gap-x-3">
          <BaseSelect v-if="preferredFileType.enable" v-model="preferredFileType.fileType" class="min-w-100px" :options="SUPPORT_FILE_TYPES.map(t => ({ label: t, value: t }))" />

          <BaseSwitch v-model="preferredFileType.enable" />
        </div>
      </div>
    </div>
  </div>
</template>
