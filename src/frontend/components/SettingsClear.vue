<script setup lang="ts">
import ConfirmModal from './ConfirmModal.vue'

const { t } = useI18n()
const { deleteAllProjects } = useDBStore()

const { open, close } = useModal({
  component: ConfirmModal,
  attrs: {
    title: t('dialog.confirm.title'),
    onOk() { handleClearAll() },
    onCancel() { close() },
  },
  slots: {
    default: {
      component: h('p', null, t('settings.clear_all_confirm')),
    },
  },
})

async function handleClearAll() {
  await axios.get('/project/clear')
  deleteAllProjects()
  close()
}
</script>

<template>
  <div class="flex items-center justify-between">
    <h3>{{ t('settings.clear_heading') }}</h3>
    <BaseButton variant="destructive" @click="open">
      {{ t('button.clear') }}
    </BaseButton>
  </div>
</template>
