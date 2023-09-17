<script setup lang="ts">
const { title = 'Confirm', showCancel = true, showOk = true, preventClose = false } = defineProps<{
  title?: string
  contentClass?: string
  okContent?: string
  cancelContent?: string
  showOk?: boolean
  showCancel?: boolean
  preventClose?: boolean
}>()

const emits = defineEmits<{ (e: 'ok'): void; (e: 'cancel'): void }>()

const { t } = useI18n()
</script>

<template>
  <BaseModal :title="title" :content-class="`w-full max-w-30vw ${contentClass}`" :prevent-close="preventClose">
    <template #body>
      <slot />
    </template>

    <template #footer>
      <div class="flex justify-end gap-x-2">
        <BaseButton v-if="showCancel" variant="secondary" @click="emits('cancel')">
          {{ cancelContent ?? t('button.cancel') }}
        </BaseButton>

        <BaseButton v-if="showOk" @click="emits('ok')">
          {{ okContent ?? t('button.confirm') }}
        </BaseButton>
      </div>
    </template>
  </BaseModal>
</template>
