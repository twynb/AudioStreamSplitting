<script setup lang="ts">
import WaveSurfer from 'wavesurfer.js'

const props = defineProps<{
  file: Project['files'][0]
}>()

const emits = defineEmits<{
  (e: 'succeedProcess', v: ProcessAudioFile): void
  (e: 'updatePeaks', v: { filePath: string; peaks: number[][] }): void

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
    peaks: props.file.peaks,
  })
  ws.on('interaction', () => ws.playPause())
  ws.on('ready', () => {
    isWsLoaded.value = true
    isAudioLoading.value = false
    emits('updatePeaks', { peaks: ws.exportPeaks(), filePath: props.file.filePath })
  })
}

const { execute, isFetching } = usePost<ProcessAudioFile>({
  url: '/audio/process',
  onSuccess(data) {
    emits('succeedProcess', data)
  },
})

onMounted(() => {
  if (props.file.peaks)
    handleLoadWaveform()
})
</script>

<template>
  <div class="space-y-2">
    <div class="flex items-center gap-x-2">
      <span class="text-xs" :class="file.info ? 'i-carbon:checkmark-filled' : 'i-carbon:subtract-alt'" />
      <p class="text-sm">
        {{ file.fileName }}
      </p>
    </div>

    <div class="relative">
      <div :id="`waveform_${file.name}`" class="min-h-128px border rounded-md" />

      <div v-if="!isWsLoaded" class="absolute-center">
        <BaseLoader v-if="isAudioLoading" />

        <BaseButton v-else variant="outline" class="text-xs" @click="handleLoadWaveform">
          <span class="mr-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 256 256">
              <path fill="currentColor" d="M54 96v64a6 6 0 0 1-12 0V96a6 6 0 0 1 12 0Zm34-70a6 6 0 0 0-6 6v192a6 6 0 0 0 12 0V32a6 6 0 0 0-6-6Zm40 32a6 6 0 0 0-6 6v128a6 6 0 0 0 12 0V64a6 6 0 0 0-6-6Zm40 32a6 6 0 0 0-6 6v64a6 6 0 0 0 12 0V96a6 6 0 0 0-6-6Zm40-16a6 6 0 0 0-6 6v96a6 6 0 0 0 12 0V80a6 6 0 0 0-6-6Z" />
            </svg>
          </span>
          Load Waveform
        </BaseButton>
      </div>
    </div>

    <p v-if="file.fileType === 'webm'" class="text-center text-sm text-muted-foreground">
      .wav cannot be processed at the moment!
    </p>

    <BaseButton
      :disabled="file.fileType === 'webm' || isFetching"
      @click="execute({ filePath: file.filePath })"
    >
      <BaseLoader
        v-if="isFetching"
        class="mr-2 border-primary-foreground !border-2"
        :size="15"
      />
      Process
    </BaseButton>

    <pre>
      {{ file.info }}
    </pre>
  </div>
</template>
