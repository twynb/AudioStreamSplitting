<script setup lang="ts">
const { t } = useI18n()
</script>

<template>
  <ContentLayout :header="t('sidebar.settings')">
    <div class="max-w-80% space-y-10">
      <SettingsGeneral />

      <SettingsAppearance />

      <SettingsAdvanced />
    </div>
  </ContentLayout>
</template>
