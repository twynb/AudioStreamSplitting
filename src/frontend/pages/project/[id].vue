<script setup lang="ts">
import WaveSurfer from 'wavesurfer.js'

const props = defineProps<{ id: string }>()

const { getProjectById } = useDBStore()
const project = getProjectById(props.id)
const router = useRouter()

if (!project)
  router.push('/')
else
  project.visited = true

const { data } = await axios.post('/audio/get', { audioPath: project?.files[0].filePath }, { responseType: 'blob' })
const url = URL.createObjectURL(data)
const isAudioLoading = ref(true)

onMounted(() => {
  const ws = WaveSurfer.create({
    container: '#waveform',
    waveColor: 'rgb(173, 250, 29)',
    progressColor: '#8EAC50',
    barRadius: 5,
    barWidth: 5,
    barGap: 2,
    cursorWidth: 3,
    url,
  })
  ws.on('interaction', () => ws.playPause())
  ws.on('ready', () => isAudioLoading.value = false)
})

const { execute, isFetching } = usePost<ProcessAudioFile>({
  url: '/audio/process',
  onSuccess(data) {
    if (project && data) {
      const fileIndex = project.files.findIndex(({ filePath }) => filePath === data.filePath)
      if (fileIndex === -1)
        return

      project.files[fileIndex].info = data.info
    }
  },
})
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

    <div class="relative">
      <div id="waveform" class="border rounded-md" />
      <div v-if="isAudioLoading" class="absolute-center">
        <BaseLoader />
      </div>
    </div>

    <table class="w-full text-sm">
      <thead>
        <tr class="border-b border-b-border">
          <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
            Song name
          </th>

          <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
            Song path
          </th>

          <th class="h-12 px-4 text-center align-middle font-medium text-muted-foreground">
            State
          </th>

          <th />
        </tr>
      </thead>
      <tbody>
        <tr v-for="{ fileName, filePath, info } in project.files" :key="fileName" class="border-b border-b-border">
          <td class="p-4 align-middle font-medium">
            {{ fileName }}
          </td>

          <td class="p-4 align-middle">
            {{ filePath }}
          </td>

          <td class="text-center align-middle">
            <span v-if="info" class="i-carbon:checkmark-filled" />
            <span v-else class="i-carbon:subtract-alt" />
          </td>

          <td />

          <td class="cursor-pointer pr-4 text-right align-middle transition-color">
            <BaseButton :disabled="isFetching" @click="execute({ filePath })">
              <span
                v-if="isFetching"
                class="i-carbon-close mr-1 animate-spin"
              />
              Process
            </BaseButton>
          </td>
        </tr>
      </tbody>
    </table>

    <pre>
      {{ project }}
    </pre>
  </ContentLayout>
</template>
