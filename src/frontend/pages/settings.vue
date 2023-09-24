<script setup lang="ts">
const { t } = useI18n()
</script>

<template>
  <BaseLayout :header="t('sidebar.settings')">
    <div class="pb-30 lg:max-w-80% space-y-12">
      <SettingsGeneral />

      <SettingsSave />

      <SettingsAdvanced />
    </div>
  </BaseLayout>
</template>
