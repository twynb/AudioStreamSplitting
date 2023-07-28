<script setup lang="ts">
const props = defineProps<{ id: string }>()
const router = useRouter()
const { getProjectById } = useDBStore()

const project = getProjectById(props.id)

if (!project)
  router.push('/')
</script>

<template>
  <ContentLayout v-if="project">
    <template #header>
      <div class="flex items-center justify-between gap-x-3">
        <h1 class="text-4xl">
          {{ project.name }}
        </h1>

        <BaseButton icon-only variant="ghost" @click="router.push('/')">
          <span class="i-carbon-close" />
        </BaseButton>
      </div>
    </template>

    <pre>
      {{ project }}
    </pre>
  </ContentLayout>
</template>
