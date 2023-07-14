<script setup lang="ts">
import CreateProjectModal from '@components/dialogs/CreateProjectModal.vue'

const { items } = storeToRefs(useDBStore())
const { t } = useI18n()

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

const router = useRouter()
function handleEditItem(itemId: string) {
  router.push(`/project/${itemId}`)
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
        v-for="item in items"
        :key="item.id" :item="item"
        @click="handleEditItem(item.id)"
        @edit="handleEditItem"
        @delete="handleDeleteItem"
      />
    </div>
  </ContentLayout>
</template>
