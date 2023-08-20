<script setup lang="ts">
import ConfirmModal from './dialogs/ConfirmModal.vue'

const { t } = useI18n()
const { deleteAllProjects } = useDBStore()

const { open, close } = useModal({
  component: ConfirmModal,
  attrs: {
    title: t('dialog.confirm.title'),
    content: 'Do you realy want to delete all projects.',
    onOk() { handleClearAll() },
    onCancel() { close() },
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
    <h3>Clear all projects</h3>
    <BaseButton variant="destructive" @click="open">
      Clear
    </BaseButton>
  </div>
</template>
