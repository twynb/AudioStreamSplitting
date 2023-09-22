<script setup lang="ts">
import type { WaveSurferOptions } from 'wavesurfer.js'
import WaveSurfer from 'wavesurfer.js'
import RecordPlugin from 'wavesurfer.js/dist/plugins/record.js'
import type { Project } from 'models/types'
import ConfirmModal from '@components/ConfirmModal.vue'
import { getRecordSteps } from '../includes/driver'

const { createProject } = useDBStore()
const router = useRouter()
const { t } = useI18n()

const isFFMPEGInstall = ref(false)
onMounted(async () => {
  try {
    await axios.get('/project/check-ffmpeg')
    isFFMPEGInstall.value = true
  }
  catch (e) {
    const { open, close } = useModal({
      component: ConfirmModal,
      attrs: {
        title: t('dialog.confirm.warning'),
        content: t('record.no_ffmpeg'),
        preventClose: true,
        showCancel: false,
        okContent: t('button.back_to_dashboard'),
        onOk() {
          router.push('/')
          close()
        },

      },
    })
    open()
  }
})

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
const { driver, setConfig } = useDriver()

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
  if (driver.value.isActive())
    driver.value.moveNext()
}

async function handleStopRecord() {
  record.destroy()
  if (driver.value.isActive()) {
    driver.value.moveNext()
    return
  }
  await new Promise(resolve => setTimeout(() => resolve(undefined), 300))
  focusInputName()
}

function handleDelete() {
  ws.destroy()
  initialize()

  state.value = 'record'
  blob.value = undefined

  if (driver.value.isActive())
    driver.value.moveTo(0)
}

function focusInputName() {
  const input = document.querySelector('form#create_project_form')?.querySelector('input#record_name') as HTMLInputElement
  input && input.focus()
}

async function handleSave() {
  if (!blob.value)
    return

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
    url: '/project/create',
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

function handleDrive() {
  driver.value.drive()
  skipNextHiddenDriverElements()
}

function skipNextHiddenDriverElements() {
  let element = driver.value.getActiveElement()
  while ((element?.checkVisibility() ?? true) === false) {
    driver.value.moveNext()
    element = driver.value.getActiveElement()
  }
}

setConfig({
  onNextClick() {
    const index = driver.value.getActiveIndex()
    switch (index) {
      case 0:
        record.startRecording()
        record.startMic()
        break

      case 1:
        record.destroy()
        break
      case 4:
        setTimeout(focusInputName, 400)
    }

    driver.value.moveNext()
  },
  onPrevClick() {
    const index = driver.value.getActiveIndex()
    if (index === 2) {
      handleDelete()
      return
    }

    driver.value.movePrevious()
  },
  steps: getRecordSteps(),
  showProgress: true,
})

onUnmounted(() => {
  record.destroy()
  ws.destroy()
  url.value && URL.revokeObjectURL(url.value)
})
</script>

<template>
  <BaseLayout :header=" t('sidebar.record')">
    <template #header>
      <div class="flex items-center gap-x-3">
        <h1 class="text-4xl">
          {{ t('sidebar.record') }}
        </h1>

        <BaseButton icon-only variant="ghost" title="Help" @click="handleDrive">
          <span class="i-carbon:help-filled text-lg" />
        </BaseButton>
      </div>
    </template>

    <template #default>
      <div class="space-y-4">
        <div id="waveform" class="border rounded-md" />

        <div v-show="state === 'record'" class="flex items-center justify-center gap-x-8">
          <BaseButton v-show="isRecording" id="stop_record_btn" icon-only variant="ghost" @click="handleStopRecord">
            <span class="i-carbon-stop-filled-alt text-xl" />
          </BaseButton>

          <BaseButton v-show="!isRecording" id="start_record_btn" icon-only variant="ghost" @click="handleRecord">
            <span class="i-carbon-circle-filled text-xl" />
          </BaseButton>
        </div>

        <div v-show="state === 'play'" class="flex items-center justify-center gap-x-8">
          <BaseButton id="download_record_btn" icon-only variant="ghost" class="mr-auto" @click="handleSave">
            <span class="i-carbon-download" />
          </BaseButton>

          <div id="media_control_btns" class="flex items-center justify-center gap-x-8">
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
          </div>

          <BaseButton id="delete_record_btn" icon-only variant="ghost" class="ml-auto" @click="handleDelete">
            <span class="i-carbon-trash-can" />
          </BaseButton>
        </div>

        <Transition
          enter-active-class="transition-all ease duration-300"
          leave-active-class="transition-all ease duration-300" enter-from-class="opacity-0 -translate-y-50px"
          leave-to-class="opacity-0 -translate-y-50px"
        >
          <template v-if="state === 'play'">
            <div class="flex justify-center !mt-10">
              <form id="create_project_form" class="max-w-400px w-full flex flex-col border border-border rounded-md p-5" @submit.prevent="handleSubmit">
                <div class="mb-3 space-y-1">
                  <BaseLabel for="record_name" :has-error="!!submitError.name">
                    {{ t('dialog.create_project.project_name') }}
                  </BaseLabel>
                  <BaseInput id="record_name" v-model="submitInfo.name" name="record_name" />
                  <p v-if="submitError.name" class="text-sm text-destructive">
                    {{ submitError.name }}
                  </p>
                </div>

                <div class="mb-6 space-y-1">
                  <BaseLabel for="record_name">
                    {{ t('dialog.create_project.project_description') }}
                  </BaseLabel>
                  <BaseInput id="record_description" v-model="submitInfo.description" name="record_description" />
                </div>
                <BaseButton type="submit">
                  {{ t('button.create_new_project') }}
                </BaseButton>
              </form>
            </div>
          </template>
        </Transition>
      </div>
    </template>
  </BaseLayout>
</template>
