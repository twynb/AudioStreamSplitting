<script setup lang="ts">
import type { Project } from 'models/types'

const props = defineProps<{ id: string }>()

const { getProjectById } = useDBStore()
const project = getProjectById(props.id)
const router = useRouter()

if (!project)
  router.push('/')
else
  project.visited = true

function updateFileProperty<TKey extends keyof Project['files'][0]>(fileIndex: number, key: TKey, v: Project['files'][0][TKey]) {
  if (!project)
    return

  project.files[fileIndex][key] = v
}

function handleChangeMeta(fileIndex: number, songIndex: number, metaIndex: number) {
  if (!project)
    return
  const segment = project.files[fileIndex].segments?.[songIndex]
  if (!segment)
    return
  const newMeta = segment.metadataOptions?.[metaIndex]
  if (newMeta)
    segment.metaIndex = metaIndex
}

function handleUpdateFileSegmentPeaks(fileIndex: number, songIndex: number, peaks: number[][]) {
  if (!project)
    return
  const segment = project.files[fileIndex].segments?.[songIndex]
  if (!segment)
    return
  segment.peaks = peaks
}
</script>

<template>
  <BaseLayout v-if="project" :header="project.name">
    <template #header>
      <div class="flex items-center justify-between">
        <h1 class="text-4xl font-semibold">
          {{ project.name }}
        </h1>

        <BaseButton icon-only variant="ghost" @click="router.push('/')">
          <span class="i-carbon-close" />
        </BaseButton>
      </div>
    </template>

    <template #default>
      <div class="pb-16 space-y-10">
        <ProjectItem
          v-for="file, fileIndex in project.files" :key="file.filePath"
          :file="file"
          @succeed-process="(v) => updateFileProperty(fileIndex, 'segments', v)"
          @update-file-peaks="(v) => updateFileProperty(fileIndex, 'peaks', v)"
          @update-segment-peaks="(songIndex, peaks) => handleUpdateFileSegmentPeaks(fileIndex, songIndex, peaks)"
          @change-meta="(songIndex, metaIndex) => handleChangeMeta(fileIndex, songIndex, metaIndex)"
          @change-preset-name="(v) => updateFileProperty(fileIndex, 'presetName', v)"
        />
      </div>
    </template>
  </BaseLayout>
</template>
