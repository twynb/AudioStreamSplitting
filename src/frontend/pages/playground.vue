<script setup lang="ts">
const { createNotification } = useNotificationStore()

function foo() {
  createNotification({
    title: 'Scheduled: something',
    content: 'Friday, February 10, 2023 at 5:57 PM',
  })
}
</script>

<template>
  <ContentLayout header="Playground">
    <BaseButton @click="foo">
      Test
    </BaseButton>
  </ContentLayout>
</template>
