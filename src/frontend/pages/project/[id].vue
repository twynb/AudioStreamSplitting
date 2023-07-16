<script setup lang="ts">
const props = defineProps<{ id: string }>()
const router = useRouter()
const { getProjectById } = useDBStore()

const project = getProjectById(props.id)

if (!project)
  router.push('/')
</script>

<template>
  <ContentLayout v-if="project" :header="project.name">
    <pre>
      {{ project }}
    </pre>
  </ContentLayout>
</template>
