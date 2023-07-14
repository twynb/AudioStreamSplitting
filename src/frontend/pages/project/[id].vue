<script setup lang="ts">
const props = defineProps<{ id: string }>()
const router = useRouter()
const { getItemById } = useDBStore()

const item = getItemById(props.id)

if (!item)
  router.push('/')
</script>

<template>
  <ContentLayout v-if="item" :header="item.name">
    <pre>
      {{ item }}
    </pre>
  </ContentLayout>
</template>
