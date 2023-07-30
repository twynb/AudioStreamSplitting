<script setup lang="ts">
import WaveSurfer from 'wavesurfer.js'
import RecordPlugin from 'wavesurfer.js/dist/plugins/record.js'

let ws: WaveSurfer
let record: RecordPlugin
const state = ref<'record' | 'play'>('record')
const isRecording = ref(false)
const isPlaying = ref(false)
const downloadConfig = ref({
  url: '',
  name: '',
})

onMounted(() => {
  ws = WaveSurfer.create({
    container: '#waveform',
    waveColor: 'rgb(173, 250, 29)',
    progressColor: '#8EAC50',
    barRadius: 9999,
    barWidth: 3,
    barGap: 1,
  })

  ws.on('interaction', () => {
    isPlaying.value = true
    ws.play()
  })
  ws.on('finish', () => {
    ws.setTime(0)
    isPlaying.value = false
  })

  record = ws.registerPlugin(RecordPlugin.create())
})

function handleRecord() {
  if (ws.isPlaying())
    ws.pause()

  if (record.isRecording())
    record.stopRecording()

  isRecording.value = true
  record.startRecording()
}

function handleStop() {
  isRecording.value = false
  state.value = 'play'
  record.stopRecording()

  setTimeout(() => {
    downloadConfig.value = {
      url: record.getRecordedUrl(),
      name: `record_${useDateFormat(new Date(), 'HH:mm:ss_DD/MM/YYYY')}`,
    }
  }, 100)
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
  ws.empty()
  isPlaying.value = false
  isRecording.value = false
  state.value = 'record'
  downloadConfig.value = { name: '', url: '' }
}

function handleSubmit() {
  axios.get(record.getRecordedUrl(), { responseType: 'blob', baseURL: '' })
    .then(({ data }) => {
      const file = new File([data], data.name, { type: data.type })

      const { execute: executePost } = usePost<ProjectResponse>({
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
      executePost(formData)
    })
}

onUnmounted(() => {
  record.destroy()
  ws.destroy()
})
</script>

<template>
  <ContentLayout header="Record">
    <div class="space-y-2">
      <div id="waveform" class="border rounded-md" />

      <div class="flex items-center justify-center gap-x-8">
        <template v-if="state === 'record'">
          <BaseButton v-if="isRecording" icon-only variant="ghost" @click="handleStop">
            <span class="i-carbon-stop-filled-alt text-2xl" />
          </BaseButton>

          <BaseButton v-else icon-only variant="ghost" @click="handleRecord">
            <span class="i-carbon-circle-filled text-2xl" />
          </BaseButton>
        </template>

        <template v-else-if="state === 'play'">
          <BaseButton :disabled="!downloadConfig.url" icon-only variant="ghost" class="mr-auto" :to="downloadConfig.url" :download="downloadConfig.name">
            <span class="i-carbon-download text-lg" />
          </BaseButton>

          <BaseButton icon-only variant="ghost" @click="handleRewind">
            <span class="i-carbon-rewind-5 text-xl" />
          </BaseButton>

          <BaseButton v-if="isPlaying" icon-only variant="ghost" @click="handlePause">
            <span class="i-carbon-pause-filled text-2xl" />
          </BaseButton>

          <BaseButton v-else icon-only variant="ghost" @click="handlePlay">
            <span class="i-carbon-play-filled-alt text-2xl" />
          </BaseButton>

          <BaseButton icon-only variant="ghost" @click="handleForward">
            <span class="i-carbon-forward-5 text-xl" />
          </BaseButton>

          <BaseButton icon-only variant="ghost" class="ml-auto" @click="handleDelete">
            <span class="i-carbon-trash-can text-lg" />
          </BaseButton>
        </template>
      </div>

      <BaseButton @click="handleSubmit">
        Submit
      </BaseButton>
    </div>
  </ContentLayout>
</template>
