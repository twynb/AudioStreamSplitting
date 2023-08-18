<script setup lang="ts">
import WaveSurfer from 'wavesurfer.js'

const props = defineProps<{
  file: Project['files'][0]
}>()

const emits = defineEmits<{
  (e: 'succeedProcess', v: ProcessAudioFile): void
}>()

const { data } = await axios.post('/audio/get', { audioPath: props.file.filePath }, { responseType: 'blob' })
const url = URL.createObjectURL(data)
const isAudioLoading = ref(false)
const isWsLoaded = ref(false)

function handleLoadWaveform() {
  isAudioLoading.value = true

  const ws = WaveSurfer.create({
    container: `#waveform_${props.file.name}`,
    waveColor: 'rgb(173, 250, 29)',
    progressColor: '#8EAC50',
    barRadius: 5,
    barWidth: 5,
    barGap: 2,
    cursorWidth: 3,
    url,
  })
  ws.on('interaction', () => ws.playPause())
  ws.on('ready', () => {
    isWsLoaded.value = true
    isAudioLoading.value = false
  })
}

const { execute, isFetching } = usePost<ProcessAudioFile>({
  url: '/audio/process',
  onSuccess(data) {
    emits('succeedProcess', data)
  },
})
</script>

<template>
  <div>
    <div class="relative">
      <div :id="`waveform_${file.name}`" class="min-h-128px border rounded-md" />

      <div v-if="!isWsLoaded" class="absolute-center">
        <BaseLoader v-if="isAudioLoading" />

        <BaseButton v-else variant="outline" class="text-xs" @click="handleLoadWaveform">
          Load Waveform
        </BaseButton>
      </div>
    </div>

    <table class="w-full caption-bottom text-sm">
      <caption class="mt-4 text-sm text-muted-foreground">
        .wav cannot be processed at the moment!
      </caption>
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
        <tr class="border-b border-b-border">
          <td class="p-4 align-middle font-medium">
            {{ file.fileName }}
          </td>

          <td class="p-4 align-middle">
            {{ file.filePath }}
          </td>

          <td class="text-center align-middle">
            <span v-if="file.info" class="i-carbon:checkmark-filled" />
            <span v-else class="i-carbon:subtract-alt" />
          </td>

          <td />

          <td class="cursor-pointer pr-4 text-right align-middle transition-color">
            <BaseButton :disabled="file.fileType === 'webm' || isFetching" @click="execute({ filePath: file.filePath })">
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
      {{ file }}
    </pre>

    <BaseSeparator orientation="horizontal" class="mb-10" />
  </div>
</template>
