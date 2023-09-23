<script setup lang="ts">
import { useLocalStorage } from '@vueuse/core'

type EnvKey = keyof typeof env.value

const { t } = useI18n()
const { defaultEnv, lsEnv } = storeToRefs(useEnvStore())

const env = ref(defaultEnv.value)
Object.entries(lsEnv.value).forEach(([key, value]) => {
  if (value)
    env.value[key as EnvKey] = value
})

const { toast } = useToastStore()
const saveSettings = useLocalStorage('save-settings', { fileType: 'mp3', shouldAsk: true, submitSavedFiles: false })

async function setApiKey(key: EnvKey) {
  const value = env.value[key]

  if (!value) {
    toast({ content: t('toast.empty_field'), variant: 'destructive' })
    throw new Error('Please give in a valid value!')
  }

  try {
    await axios.post('/env/set', { key, value })
    lsEnv.value[key] = value
    // TODO Just a workaround. Figure out why useLocalStorage is not working
    localStorage.setItem('env', JSON.stringify(lsEnv.value))
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
          {{ t('settings.acoustid_api_key') }}
        </BaseLabel>

        <div class="min-w-400px flex gap-x-3">
          <BaseInput id="SERVICE_ACOUSTID_API_KEY" v-model="env.SERVICE_ACOUSTID_API_KEY" type="password" />

          <BaseButton @click="setApiKey('SERVICE_ACOUSTID_API_KEY')">
            {{ t('button.set') }}
          </BaseButton>
        </div>
      </div>

      <div class="flex items-center justify-between">
        <BaseLabel class="!text-base" for="SERVICE_ACOUSTID_USER_KEY">
          {{ t('settings.acoustid_user_key') }}
        </BaseLabel>

        <div class="min-w-400px flex gap-x-3">
          <BaseInput id="SERVICE_ACOUSTID_USER_KEY" v-model="env.SERVICE_ACOUSTID_USER_KEY" type="password" />

          <BaseButton @click="setApiKey('SERVICE_ACOUSTID_USER_KEY')">
            {{ t('button.set') }}
          </BaseButton>
        </div>
      </div>

      <div class="flex items-center justify-between">
        <BaseLabel class="!text-base" for="SERVICE_SHAZAM_API_KEY">
          {{ t('settings.shazam_api_key') }}
        </BaseLabel>

        <div class="min-w-400px flex gap-x-3">
          <BaseInput id="SERVICE_SHAZAM_API_KEY" v-model="env.SERVICE_SHAZAM_API_KEY" type="password" />

          <BaseButton @click="setApiKey('SERVICE_SHAZAM_API_KEY')">
            {{ t('button.set') }}
          </BaseButton>
        </div>
      </div>

      <div class="flex items-center justify-between">
        <BaseLabel class="!text-base" for="OUTPUT_FILE_NAME_TEMPLATE">
          {{ t('settings.save_directory') }}
        </BaseLabel>

        <div class="min-w-400px flex gap-x-3">
          <BaseInput id="SAVE_DIRECTORY" v-model="env.SAVE_DIRECTORY" />

          <BaseButton @click="setApiKey('SAVE_DIRECTORY')">
            {{ t('button.set') }}
          </BaseButton>
        </div>
      </div>

      <div class="flex items-center justify-between">
        <BaseLabel class="!text-base" for="OUTPUT_FILE_NAME_TEMPLATE">
          {{ t('settings.output_file_name') }}
        </BaseLabel>

        <div class="min-w-400px flex gap-x-3">
          <BaseInput id="OUTPUT_FILE_NAME_TEMPLATE" v-model="env.OUTPUT_FILE_NAME_TEMPLATE" />

          <BaseButton @click="setApiKey('OUTPUT_FILE_NAME_TEMPLATE')">
            {{ t('button.set') }}
          </BaseButton>
        </div>
      </div>

      <div class="flex items-center justify-between">
        <h3>{{ t('settings.submit_saved_files') }}</h3>

        <BaseSwitch v-model="saveSettings.submitSavedFiles" />
      </div>
    </div>
  </div>
</template>

<docs>
  Advanced section in settings page
</docs>
