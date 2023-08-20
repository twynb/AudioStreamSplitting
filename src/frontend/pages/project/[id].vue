<script setup lang="ts">
const props = defineProps<{ id: string }>()

const { getProjectById } = useDBStore()
const project = getProjectById(props.id)
const router = useRouter()

if (!project)
  router.push('/')
else
  project.visited = true

function updateFileProperty<TKey extends keyof Project['files'][0]>(filePath: string, key: TKey, v: Project['files'][0][TKey]) {
  if (!project)
    return
  const fileIndex = project.files.findIndex(p => p.filePath === filePath)
  if (fileIndex === -1)
    return

  project.files[fileIndex][key] = v
}
</script>

<template>
  <ContentLayout v-if="project" :header="project.name">
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

    <template #default>
      <div class="space-y-10">
        <ProjectItem
          v-for="file in project.files" :key="file.filePath"
          :file="file"
          @succeed-process="({ filePath, info }) => updateFileProperty(filePath, 'info', info)"
          @update-peaks="({ filePath, peaks }) => updateFileProperty(filePath, 'peaks', peaks)"
        />
      </div>
    </template>
  </ContentLayout>
</template>
