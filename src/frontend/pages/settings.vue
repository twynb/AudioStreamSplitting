<script setup lang="ts">
import { LangMap } from '../constants'

const { t } = useI18n()
const { availableLocales, toggleLocales } = useLocale()

const currentLocal = ref('en')

watch(currentLocal, async () => {
  await toggleLocales(currentLocal.value)
})

const localOpts = Object.entries(LangMap).map(([key, value]) => {
  if (!availableLocales.includes(key))
    return null

  return {
    label: value,
    value: key,
  }
})

</script>

<template>
  <ContentLayout
    :header="t('sidebar.settings')"
  >
    <div>
      <label class="block" for="lang">Language</label>
      <select class="" id="lang" v-model="currentLocal" name="lang">
        <option v-for="opt in localOpts" :key="opt?.value" :value="opt?.value">
          {{ opt?.label }}
        </option>
      </select>
    </div>
  </ContentLayout>
</template>
