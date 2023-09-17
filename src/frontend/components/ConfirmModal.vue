<script setup lang="ts">
withDefaults(defineProps<{
  /**
   * Title of the modal.
   */
  title?: string
  /**
   * CSS class for the modal's content.
   */
  contentClass?: string
  /**
   * Text content of the "OK" button.
   */
  okContent?: string
  /**
   * Text content of the "Cancel" button.
   */
  cancelContent?: string
  /**
   * Controls the visibility of the "OK" button.
   */
  showOk?: boolean
  /**
   * Controls the visibility of the "Cancel" button.
   */
  showCancel?: boolean
  /**
   * Prevents the component from being closed.
   */
  preventClose?: boolean
}>(),
{
  title: 'Confirm', showCancel: true, showOk: true, preventClose: false,
})

const emits = defineEmits<{
  /**
   * Emits an event 'ok' when the "OK" action is triggered.
   */
  (e: 'ok'): void
  /**
   * Emits an event 'cancel' when the "Cancel" action is triggered.
   */
  (e: 'cancel'): void
}>()

const { t } = useI18n()
</script>

<template>
  <BaseModal :title="title" :content-class="`w-full max-w-30vw ${contentClass}`" :prevent-close="preventClose">
    <template #body>
      <!-- @slot Slot for content -->
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
