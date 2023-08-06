<script setup lang="ts">
import type { WaveSurferOptions } from 'wavesurfer.js'
import WaveSurfer from 'wavesurfer.js'
import RecordPlugin from 'wavesurfer.js/dist/plugins/record.js'

let ws: WaveSurfer
let record: RecordPlugin
const wsConfig: WaveSurferOptions = {
  container: '#waveform',
  waveColor: 'rgb(173, 250, 29)',
  progressColor: '#8EAC50',
  barRadius: 5,
  barWidth: 5,
  barGap: 2,
  cursorWidth: 3,
}
const state = ref<'record' | 'play'>('record')
const isRecording = ref(false)
const isPlaying = ref(false)
const blob = shallowRef<Blob>()
const url = ref('')

onMounted(() => initialize())
function initialize() {
  ws = WaveSurfer.create({ ...wsConfig })

  record = ws.registerPlugin(RecordPlugin.create())
  record.on('record-end', (_blob) => {
    ws.destroy()

    blob.value = _blob
    url.value = URL.createObjectURL(blob.value)
    ws = WaveSurfer.create({ ...wsConfig, url: url.value })

    ws.on('interaction', () => {
      isPlaying.value = true
      ws.playPause()
    })
    ws.on('finish', () => {
      ws.setTime(0)
      isPlaying.value = false
    })
  })
}

function handleRecord() {
  isRecording.value = true
  record.startMic()
  record.startRecording()
}

function handleStop() {
  isRecording.value = false
  state.value = 'play'
  record.stopRecording()
  record.stopMic()
}

function handlePlay() {
  isPlaying.value = true
  ws.play()
}

function handlePause() {
  isPlaying.value = false
  ws.pause()
}

function handleRewind() {
  ws.setTime(Math.min(ws.getCurrentTime() - 5, 0))
}

function handleForward() {
  ws.setTime(Math.max(ws.getCurrentTime() + 5, ws.getDuration()))
}

function handleDelete() {
  ws.destroy()
  initialize()

  isPlaying.value = false
  isRecording.value = false
  state.value = 'record'
  blob.value = undefined
}

function handleSubmit() {
  if (!blob.value)
    return

  const file = new File([blob.value], `record.${blob.value.type}`, { type: blob.value.type })

  const { execute } = usePost<ProjectResponse>({
    url: '/info',
    axiosConfig: { headers: { 'Content-Type': 'multipart/form-data' } },
    onSuccess({ name, description, files }) {
      console.log(name, description, files)
    },
  })

  const formData = new FormData()
  formData.append('name', 'record_name')
  formData.append('description', 'record_description')
  formData.append('file', file)
  execute(formData)
}

onUnmounted(() => {
  record.destroy()
  ws.destroy()
  url.value && URL.revokeObjectURL(url.value)
})
</script>

<template>
  <ContentLayout header="Record">
    <div class="space-y-2">
      <div id="waveform" class="border rounded-md" />

      <div class="flex items-center justify-center gap-x-8">
        <template v-if="state === 'record'">
          <BaseButton v-if="isRecording" icon-only variant="ghost" @click="handleStop">
            <span class="i-carbon-stop-filled-alt text-xl" />
          </BaseButton>

          <BaseButton v-else icon-only variant="ghost" @click="handleRecord">
            <span class="i-carbon-circle-filled text-xl" />
          </BaseButton>
        </template>

        <template v-else-if="state === 'play'">
          <BaseButton :disabled="!url" icon-only variant="ghost" class="mr-auto" :to="url" :download="`record_${useDateFormat(new Date(), 'HH:mm:ss_DD/MM/YYYY')}`">
            <span class="i-carbon-download" />
          </BaseButton>

          <BaseButton icon-only variant="ghost" @click="handleRewind">
            <span class="i-carbon-rewind-5 text-lg" />
          </BaseButton>

          <BaseButton v-if="isPlaying" icon-only variant="ghost" @click="handlePause">
            <span class="i-carbon-pause-filled text-xl" />
          </BaseButton>

          <BaseButton v-else icon-only variant="ghost" @click="handlePlay">
            <span class="i-carbon-play-filled-alt text-xl" />
          </BaseButton>

          <BaseButton icon-only variant="ghost" @click="handleForward">
            <span class="i-carbon-forward-5 text-lg" />
          </BaseButton>

          <BaseButton icon-only variant="ghost" class="ml-auto" @click="handleDelete">
            <span class="i-carbon-trash-can" />
          </BaseButton>
        </template>
      </div>

      <template v-if="state === 'play'">
        <p class="text-red">
          Currently audio is recorded with type .webm, which cannot be proceeded with librosa
        </p>
        <BaseButton @click="handleSubmit">
          Submit
        </BaseButton>
      </template>
    </div>
  </ContentLayout>
</template>
