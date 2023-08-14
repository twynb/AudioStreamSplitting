<script setup lang="ts">
import type { WaveSurferOptions } from 'wavesurfer.js'
import WaveSurfer from 'wavesurfer.js'
import RecordPlugin from 'wavesurfer.js/dist/plugins/record.js'

const { createProject } = useDBStore()
const router = useRouter()

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
  record.on('record-start', () => isRecording.value = true)
  record.on('record-end', (_blob) => {
    ws.destroy()
    record.destroy()

    isRecording.value = false
    state.value = 'play'

    blob.value = _blob
    url.value = URL.createObjectURL(blob.value)

    ws = WaveSurfer.create({ ...wsConfig, url: url.value })
    ws.on('play', () => isPlaying.value = true)
    ws.on('pause', () => isPlaying.value = false)
    ws.on('interaction', () => ws.playPause())
    ws.on('finish', () => ws.setTime(0))
  })
}

function handleRecord() {
  record.startRecording()
  record.startMic()
}

function handleDelete() {
  ws.destroy()
  initialize()

  state.value = 'record'
  blob.value = undefined
}
async function handleSave() {
  if (!blob.value)
    return

  // @ts-expect-error showSaveFilePicker is still in experimental
  const newHandle = await window.showSaveFilePicker({
    suggestedName: 'record.webm',
    types: [{
      description: 'WebM file',
      accept: { 'audio/webm': ['.webm'] },
    }],
  })

  const writableStream = await newHandle.createWritable()
  await writableStream.write(blob.value)
  await writableStream.close()
}

/**
 * Submit
*/

const submitInfo = ref({ name: '', description: '' })
const submitError = ref({ name: '' })

function handleSubmit() {
  if (!blob.value)
    return

  if (!submitInfo.value.name) {
    submitError.value.name = 'Please give a name'
    return
  }

  const file = new File([blob.value], 'record.webm', { type: 'audio/webm' })

  const { execute } = usePost<Project>({
    url: '/create_project',
    axiosConfig: { headers: { 'Content-Type': 'multipart/form-data' } },
    onSuccess(project) {
      createProject(project)
      router.push(`/project/${project.id}`)
    },
  })

  const formData = new FormData()
  formData.append('name', submitInfo.value.name)
  formData.append('description', submitInfo.value.description)
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
          <BaseButton v-if="isRecording" icon-only variant="ghost" @click="record.destroy()">
            <span class="i-carbon-stop-filled-alt text-xl" />
          </BaseButton>

          <BaseButton v-else icon-only variant="ghost" @click="handleRecord">
            <span class="i-carbon-circle-filled text-xl" />
          </BaseButton>
        </template>

        <template v-else-if="state === 'play'">
          <BaseButton icon-only variant="ghost" class="mr-auto" @click="handleSave">
            <span class="i-carbon-download" />
          </BaseButton>

          <BaseButton icon-only variant="ghost" @click="ws.skip(-5)">
            <span class="i-carbon-rewind-5 text-lg" />
          </BaseButton>

          <BaseButton v-if="isPlaying" icon-only variant="ghost" @click="ws.pause()">
            <span class="i-carbon-pause-filled text-xl" />
          </BaseButton>

          <BaseButton v-else icon-only variant="ghost" @click="ws.play()">
            <span class="i-carbon-play-filled-alt text-xl" />
          </BaseButton>

          <BaseButton icon-only variant="ghost" @click="ws.skip((5))">
            <span class="i-carbon-forward-5 text-lg" />
          </BaseButton>

          <BaseButton icon-only variant="ghost" class="ml-auto" @click="handleDelete">
            <span class="i-carbon-trash-can" />
          </BaseButton>
        </template>
      </div>

      <Transition
        enter-active-class="transition-all ease duration-300"
        leave-active-class="transition-all ease duration-300" enter-from-class="opacity-0 -translate-y-50px"
        leave-to-class="opacity-0 -translate-y-50px"
      >
        <template v-if="state === 'play'">
          <div class="flex justify-center !mt-10">
            <div class="max-w-400px w-full flex flex-col border border-border rounded-md p-5">
              <div class="mb-3 space-y-1">
                <BaseLabel for="record_name" :has-error="!!submitError.name">
                  Name
                </BaseLabel>
                <BaseInput id="record_name" v-model="submitInfo.name" name="record_name" />
                <p v-if="submitError.name" class="text-sm text-destructive">
                  {{ submitError.name }}
                </p>
              </div>

              <div class="mb-6 space-y-1">
                <BaseLabel for="record_name">
                  Description
                </BaseLabel>
                <BaseInput id="record_description" v-model="submitInfo.description" name="record_description" />
              </div>
              <BaseButton @click="handleSubmit">
                Create new project
              </BaseButton>
            </div>
          </div>
        </template>
      </Transition>
    </div>
  </ContentLayout>
</template>
