<script setup lang="ts">
import { useLocalStorage } from '@vueuse/core'

const { t } = useI18n()

const env = useLocalStorage<Record<string, string>>(
  'env',
  {
    SERVICE_ACOUSTID_API_KEY: import.meta.env.VITE_SERVICE_ACOUSTID_API_KEY,
    SERVICE_SHAZAM_API_KEY: import.meta.env.VITE_SERVICE_SHAZAM_API_KEY,
    OUTPUT_FILE_NAME_TEMPLATE: import.meta.env.VITE_OUTPUT_FILE_NAME_TEMPLATE,
  }, { mergeDefaults: true })

const { toast } = useToastStore()

async function setApiKey(key: string) {
  if (!env.value[key]) {
    toast({ content: t('toast.empty_field'), variant: 'destructive' })
    throw new Error('Please give in a valid value!')
  }

  try {
    await axios.post('/env/set', { key, value: env.value[key] })
    toast({ content: t('toast.changed_successfully') })
  }
  catch (e) {
    toast({ content: t('toast.unkown_error'), variant: 'destructive' })
  }
}
</script>

<template>
  <div>
    <h2 class="text-3xl">
      {{ t('settings.advanced') }}
    </h2>

    <BaseSeparator orientation="horizontal" />

    <div class="space-y-5">
      <div class="flex items-center justify-between">
        <BaseLabel class="!text-base" for="SERVICE_ACOUSTID_API_KEY">
          AcoustId API Key
        </BaseLabel>

        <div class="flex gap-x-3">
          <BaseTextArea id="SERVICE_ACOUSTID_API_KEY" v-model="env.SERVICE_ACOUSTID_API_KEY" class="min-h-80px" />

          <BaseButton @click="setApiKey('SERVICE_ACOUSTID_API_KEY')">
            {{ t('button.set') }}
          </BaseButton>
        </div>
      </div>

      <div class="flex items-center justify-between">
        <BaseLabel class="!text-base" for="SERVICE_SHAZAM_API_KEY">
          Shazam API Key
        </BaseLabel>

        <div class="flex gap-x-3">
          <BaseTextArea id="SERVICE_SHAZAM_API_KEY" v-model="env.SERVICE_SHAZAM_API_KEY" class="min-h-80px" />

          <BaseButton @click="setApiKey('SERVICE_SHAZAM_API_KEY')">
            {{ t('button.set') }}
          </BaseButton>
        </div>
      </div>

      <div class="flex items-center justify-between">
        <BaseLabel class="!text-base" for="OUTPUT_FILE_NAME_TEMPLATE">
          Output File Name
        </BaseLabel>

        <div class="flex gap-x-3">
          <BaseInput id="OUTPUT_FILE_NAME_TEMPLATE" v-model="env.OUTPUT_FILE_NAME_TEMPLATE" />

          <BaseButton @click="setApiKey('SERVICE_SHAZAM_API_KEY')">
            {{ t('button.set') }}
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>
