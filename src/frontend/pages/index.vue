<script setup lang="ts">
import NewProjectModal from '@components/dialogs/NewProjectModal.vue'

const { t } = useI18n()

const { open } = useModal({
  component: NewProjectModal,
})

const items = [
  {
    name: 'Possibly',
    description: 'porch express enter silk packon walk specific',
    duration: 1024,
    expectedCount: 8,
    foundCount: 6,
    createAt: '08/19/2109',
  },
  {
    name: 'Meet',
    description: 'element perhaps sheep imagine image birth',
    duration: 896,
    expectedCount: 6,
    foundCount: 6,
    createAt: '11/12/2098',
  },
  {
    name: 'Gently',
    description: 'guide bark specific touch mistake element',
    duration: 512,
    expectedCount: 3,
    foundCount: 2,
    createAt: '06/27/2091',
  },
  {
    name: 'Mental',
    description: 'whistle bit plan safety lonely acres policeman',
    duration: 1280,
    expectedCount: 8,
    foundCount: 2,
    createAt: '01/16/2032',
  },
  {
    name: 'Tonguemental',
    description: 'belt policeman with downach picture hope',
    duration: 1440,
    expectedCount: 10,
    foundCount: 5,
    createAt: '02/18/2092',
  },
]
export type Item = typeof items[0]
</script>

<template>
  <ContentLayout :header="t('sidebar.dashboard')">
    <div class="scroll grid grid-cols-2 gap-4">
      <div class="col-span-2 flex-center cursor-pointer border border-border rounded-sm p-3 hover:border-accent-foreground" @click="open">
        <div class="flex flex-col items-center gap-y-1 font-medium">
          {{ t('dashboard.project.new') }}
          <span class="i-carbon-add text-lg" />
        </div>
      </div>

      <DashboardItem v-for="(item, index) in items" :key="index" :item="item" />
    </div>
  </ContentLayout>
</template>
