<script setup lang="ts">
import { useLocalStorage } from '@vueuse/core'

const env = useLocalStorage(
  'env',
  {
    SERVICE_ACOUSTID_API_KEY: '',
  })

onMounted(() => getApiKey())
const { toast } = useToastStore()

async function getApiKey() {
  if (env.value.SERVICE_ACOUSTID_API_KEY)
    return
  const { data } = await axios.get<{ value: string }>('/env/get', { params: { key: 'SERVICE_ACOUSTID_API_KEY' } })
  env.value.SERVICE_ACOUSTID_API_KEY = data.value
}

async function setApiKey() {
  if (!env.value.SERVICE_ACOUSTID_API_KEY)
    return

  await axios.post('/env/set', {
    key: 'SERVICE_ACOUSTID_API_KEY',
    value: env.value.SERVICE_ACOUSTID_API_KEY,
  })
}

async function handleSetApiKey() {
  try {
    await setApiKey()
    await getApiKey()
    toast({ content: 'Changed successfully!' })
  }
  catch (e) {
    toast({ content: 'Something wrong happend!' })
  }
}
</script>

<template>
  <div>
    <h2 class="text-3xl">
      Advanced
    </h2>

    <BaseSeparator orientation="horizontal" />

    <div class="space-y-5">
      <div class="flex items-center justify-between">
        <h3>
          API Key
        </h3>

        <div class="max-w-11rem flex">
          <BaseInput v-model="env.SERVICE_ACOUSTID_API_KEY" class="rounded-br-none rounded-tr-none" />
          <BaseButton icon-only class="rounded-bl-none rounded-tl-none" @click="handleSetApiKey">
            Set
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>
