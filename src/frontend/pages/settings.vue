<script setup lang="ts">
import { LangMap } from '../constants'

const { t } = useI18n()
const { toggleLocales } = useLocale()

const currentLocal = ref('en')

watch(currentLocal, async () => {
  await toggleLocales(currentLocal.value)
})

const localOpts = Object.entries(LangMap).map(([key, value]) => {
  return {
    label: value,
    value: key,
  }
})
</script>

<template>
  <ContentLayout :header="t('sidebar.settings')">
    <div>
      <BaseSelect
        v-model="currentLocal"
        :placeholder="t('settings.languagues.placeholder')"
        :options="localOpts"
        class="w-180px"
      >
        <template #label>
          {{ localOpts.filter(({ value }) => value === currentLocal)[0].label }}
        </template>
      </BaseSelect>
    </div>
  </ContentLayout>
</template>
