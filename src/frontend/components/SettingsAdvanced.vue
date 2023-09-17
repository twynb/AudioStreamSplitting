<script setup lang="ts">
type EnvKey = keyof typeof env.value

const { t } = useI18n()
const { defaultEnv, lsEnv } = storeToRefs(useEnvStore())

const env = ref(defaultEnv.value)
Object.entries(lsEnv.value).forEach(([key, value]) => {
  if (value)
    env.value[key as EnvKey] = value
})

const { toast } = useToastStore()

async function setApiKey(key: EnvKey) {
  const value = env.value[key]

  if (!value) {
    toast({ content: t('toast.empty_field'), variant: 'destructive' })
    throw new Error('Please give in a valid value!')
  }

  try {
    await axios.post('/env/set', { key, value })
    lsEnv.value[key] = value
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
          <BaseTextArea id="SERVICE_ACOUSTID_API_KEY" v-model="env.SERVICE_ACOUSTID_API_KEY" />

          <BaseButton @click="setApiKey('SERVICE_ACOUSTID_API_KEY')">
            {{ t('button.set') }}
          </BaseButton>
        </div>
      </div>

      <div class="flex items-center justify-between">
        <BaseLabel class="!text-base" for="SERVICE_SHAZAM_API_KEY">
          {{ t('settings.shazam_api_key') }}
        </BaseLabel>

        <div class="min-w-400px flex gap-x-3">
          <BaseTextArea id="SERVICE_SHAZAM_API_KEY" v-model="env.SERVICE_SHAZAM_API_KEY" />

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
    </div>
  </div>
</template>
