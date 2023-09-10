<script setup lang="ts">
const { title = 'Confirm' } = defineProps<{
  title?: string
  contentClass?: string
}>()

const emits = defineEmits<{
  (e: 'ok'): void
  (e: 'cancel'): void
}>()

const { t } = useI18n()
</script>

<template>
  <BaseModal :title="title" :content-class="`w-full max-w-30vw ${contentClass}`">
    <template #body>
      <slot />
    </template>

    <template #footer>
      <div class="flex justify-end gap-x-2">
        <BaseButton variant="secondary" @click="emits('cancel')">
          {{ t('button.cancel') }}
        </BaseButton>

        <BaseButton @click="emits('ok')">
          {{ t('button.confirm') }}
        </BaseButton>
      </div>
    </template>
  </BaseModal>
</template>
