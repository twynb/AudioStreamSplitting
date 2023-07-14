<script setup lang="ts">
const emits = defineEmits<{
  (e: 'close'): void
  (e: 'ok', data: Data): void
}>()

const { t } = useI18n()
const data = ref({
  name: '',
  description: '',
  files: [] as File[],
})
export type Data = typeof data.value
</script>

<template>
  <BaseModal :title="t('dashboard.project.create_new_project')" content-class="w-full max-w-65vw 2xl:max-w-50vw" @close-with-x="emits('close')">
    <template #body>
      <div class="grid grid-cols-2 gap-4">
        <div class="space-y-1">
          <BaseLabel for="name">
            Name
          </BaseLabel>
          <BaseInput id="name" v-model="data.name" name="name" />
        </div>

        <div class="space-y-1">
          <BaseLabel for="description">
            Description
          </BaseLabel>
          <BaseInput id="description" v-model="data.description" name="description" />
        </div>

        <div class="col-span-2 space-y-1">
          <BaseLabel for="file">
            Audio
          </BaseLabel>
          <BaseInputFile id="file" v-model="data.files" />
        </div>
      </div>
    </template>

    <template #footer>
      <div class="flex justify-end gap-x-2">
        <BaseButton variant="secondary" @click="emits('close')">
          {{ t('global.cancel') }}
        </BaseButton>

        <BaseButton @click="emits('ok', data)">
          {{ t('global.create') }}
        </BaseButton>
      </div>
    </template>
  </BaseModal>
</template>
