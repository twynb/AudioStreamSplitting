<script setup lang="ts">
import { SUPPORT_FILE_TYPES } from '../includes/constants'

const { t } = useI18n()
const settings = useSaveSetings()
</script>

<template>
  <div>
    <h2 class="text-3xl">
      {{ t('settings.save.index') }}
    </h2>

    <BaseSeparator orientation="horizontal" />

    <div class="space-y-6">
      <div class="flex items-start justify-between">
        <div class="space-y-1">
          <h3 :class="{ 'text-muted-foreground': settings.shouldAsk }">
            {{ t('settings.save.file_type') }}
          </h3>
          <p class="text-sm text-muted-foreground">
            {{ t('settings.save.hint.file_type') }}
          </p>
        </div>

        <BaseSelect
          v-model="settings.fileType" class="min-w-100px"
          :options="SUPPORT_FILE_TYPES.map(t => ({ label: t, value: t }))"
          :disabled="settings.shouldAsk"
        />
      </div>

      <div class="flex items-start justify-between">
        <div class="space-y-1">
          <h3>{{ t('settings.save.ask_file_type') }}</h3>
          <p class="text-sm text-muted-foreground">
            {{ t('settings.save.hint.ask_file_type') }}
          </p>
        </div>

        <BaseSwitch v-model="settings.shouldAsk" />
      </div>

      <div class="flex items-start justify-between">
        <div class="space-y-1">
          <h3>{{ t('settings.save.submit_saved_files') }}</h3>
          <p class="text-sm text-muted-foreground">
            {{ t('settings.save.hint.submit_saved_files') }}
          </p>
        </div>

        <BaseSwitch v-model="settings.submitSavedFiles" />
      </div>

      <div class="flex items-start justify-between">
        <div class="space-y-1">
          <BaseLabel class="!text-base" for="SAVE_DIRECTORY">
            {{ t('settings.save.save_directory') }}
          </BaseLabel>
          <p class="text-sm text-muted-foreground">
            {{ t('settings.save.hint.save_directory') }}
          </p>
        </div>

        <BaseInput id="SAVE_DIRECTORY" v-model="settings.saveDirectory" class="max-w-400px" />
      </div>

      <div class="flex items-start justify-between">
        <div class="space-y-1">
          <BaseLabel class="!text-base" for="OUTPUT_FILE_NAME_TEMPLATE">
            {{ t('settings.save.output_file_name') }}
          </BaseLabel>
          <p class="text-sm text-muted-foreground">
            {{ t('settings.save.hint.output_file_name') }}
          </p>
        </div>

        <BaseInput id="OUTPUT_FILE_NAME_TEMPLATE" v-model="settings.nameTemplate" class="max-w-400px" />
      </div>
    </div>
  </div>
</template>
