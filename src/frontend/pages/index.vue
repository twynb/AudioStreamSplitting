<script setup lang="ts">
import CreateProjectModal from '@components/dialogs/CreateProjectModal.vue'

const { t } = useI18n()

const items = ref([
  {
    id: '03c482a8-bad0-4e94-b5a2-070580d1fd93',
    name: 'Possibly',
    description: 'porch express enter silk packon walk specific',
    duration: 1024,
    expectedCount: 8,
    foundCount: 6,
    createAt: '08/19/2109',
  },
  {
    id: '60023849-8d18-418e-9eca-1fb66678ccd8',
    name: 'Meet',
    description: 'element perhaps sheep imagine image birth',
    duration: 896,
    expectedCount: 6,
    foundCount: 6,
    createAt: '11/12/2098',
  },
  {
    id: '0fefa8bb-69c4-419b-8a2f-d3ddb8baa59a',
    name: 'Gently',
    description: 'guide bark specific touch mistake element',
    duration: 512,
    expectedCount: 3,
    foundCount: 2,
    createAt: '06/27/2091',
  },
])
export type Item = typeof items.value[0]

const { open, close } = useModal({
  component: CreateProjectModal,
  attrs: {
    onClose() { close() },
    onOk({ description, files, name }) {
      items.value.unshift({
        id: useUUID(),
        name,
        description,
        duration: 123,
        expectedCount: 5,
        foundCount: 0,
        createAt: useDateFormat(new Date(), 'DD/MM/YYYY'),
      })
      close()
    },
  },
})

function handleEditItem(itemId: string) {
  console.log('EDIT: ', itemId)
}

function handleDeleteItem(itemId: string) {
  items.value = items.value.filter(({ id }) => id !== itemId)
}
</script>

<template>
  <ContentLayout :header="t('sidebar.dashboard')">
    <div class="scroll grid grid-cols-2 gap-4">
      <div class="col-span-2 flex-center cursor-pointer border border-border rounded-sm p-3 hover:border-accent-foreground" @click="open">
        <div class="flex flex-col items-center gap-y-1 font-medium">
          {{ t('global.new') }}
          <span class="i-carbon-add text-lg" />
        </div>
      </div>

      <DashboardItem
        v-for="(item, index) in items"
        :key="index" :item="item"
        @edit="handleEditItem"
        @delete="handleDeleteItem"
      />
    </div>
  </ContentLayout>
</template>
