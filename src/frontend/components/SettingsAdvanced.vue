<script setup lang="ts">
type EnvKey = keyof typeof currentEnv.value

const { t } = useI18n()
const { toast } = useToastStore()

const currentEnv = useEnv()
const env = ref({ ...currentEnv.value })

async function setApiKey(key: EnvKey) {
  const value = env.value[key]

  if (!value) {
    toast({ content: t('toast.empty_field'), variant: 'destructive' })
    throw new Error('Please give in a valid value!')
  }

  try {
    await axios.post('/env/set', { key, value })
    currentEnv.value[key] = value
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
      {{ t('settings.advanced.index') }}
    </h2>

    <BaseSeparator orientation="horizontal" />

    <div class="space-y-6">
      <div class="flex items-start justify-between">
        <div class="max-w-1/3 xl:max-w-1/2 space-y-1">
          <BaseLabel class="!text-base" for="SERVICE_ACOUSTID_API_KEY">
            {{ t('settings.advanced.acoustid_api_key') }}
          </BaseLabel>

          <p class="text-balance text-sm text-muted-foreground">
            {{ t('settings.advanced.hint.acoustid_api_key') }}
          </p>
        </div>

        <div class="min-w-400px flex gap-x-3">
          <BaseInput id="SERVICE_ACOUSTID_API_KEY" v-model="env.SERVICE_ACOUSTID_API_KEY" type="password" />

          <BaseButton @click="setApiKey('SERVICE_ACOUSTID_API_KEY')">
            {{ t('button.set') }}
          </BaseButton>
        </div>
      </div>

      <div class="flex items-start justify-between">
        <div class="max-w-1/3 xl:max-w-1/2 space-y-1">
          <BaseLabel class="!text-base" for="SERVICE_ACOUSTID_USER_KEY">
            {{ t('settings.advanced.acoustid_user_key') }}
          </BaseLabel>
          <p class="text-balance text-sm text-muted-foreground">
            {{ t('settings.advanced.hint.acoustid_user_key') }}
          </p>
        </div>

        <div class="min-w-400px flex gap-x-3">
          <BaseInput id="SERVICE_ACOUSTID_USER_KEY" v-model="env.SERVICE_ACOUSTID_USER_KEY" type="password" />

          <BaseButton @click="setApiKey('SERVICE_ACOUSTID_USER_KEY')">
            {{ t('button.set') }}
          </BaseButton>
        </div>
      </div>

      <div class="flex items-start justify-between">
        <div class="max-w-1/3 xl:max-w-1/2 space-y-1">
          <BaseLabel class="!text-base" for="SERVICE_SHAZAM_API_KEY">
            {{ t('settings.advanced.shazam_api_key') }}
          </BaseLabel>
          <p class="text-balance text-sm text-muted-foreground">
            {{ t('settings.advanced.hint.shazam_api_key') }}
          </p>
        </div>

        <div class="min-w-400px flex gap-x-3">
          <BaseInput id="SERVICE_SHAZAM_API_KEY" v-model="env.SERVICE_SHAZAM_API_KEY" type="password" />

          <BaseButton @click="setApiKey('SERVICE_SHAZAM_API_KEY')">
            {{ t('button.set') }}
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<docs>
  Advanced section in settings page
</docs>
