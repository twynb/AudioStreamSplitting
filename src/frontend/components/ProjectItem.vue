<script setup lang="ts">
import WaveSurfer from 'wavesurfer.js'
import Regions from 'wavesurfer.js/plugins/regions'
import type { Project } from '../models/types'
import type { PostAudioSplit200SegmentsItem } from '../models/api'
import { getAudioStreamSplittingAPI } from '../models/api'

const props = defineProps<{ file: Project['files'][0] }>()

const emits = defineEmits<{
  (e: 'succeedProcess', v: PostAudioSplit200SegmentsItem[]): void
  (e: 'updatePeaks', v: number[][]): void
}>()

const { postAudioSplit, postAudioGetSegment } = getAudioStreamSplittingAPI()
const { toast } = useToastStore()
const { t } = useI18n()
const { data } = await axios.post('/audio/get', { audioPath: props.file.filePath }, { responseType: 'blob' })
const url = URL.createObjectURL(data)
const isAudioLoading = ref(true)

const ws = shallowRef<WaveSurfer>()
const regions = shallowRef<Regions>()

onMounted(() => {
  ws.value = WaveSurfer.create({
    container: '#waveform',
    waveColor: 'rgb(173, 250, 29)',
    progressColor: '#8EAC50',
    barRadius: 5,
    barWidth: 5,
    barGap: 2,
    cursorWidth: 3,
    url,
    peaks: props.file.peaks,
  })

  regions.value = ws.value.registerPlugin(Regions.create())

  ws.value.on('interaction', () => ws.value && ws.value.playPause())
  ws.value.on('ready', () => {
    isAudioLoading.value = false
    emits('updatePeaks', ws.value ? ws.value.exportPeaks() : [])
    props.file.segments && addRegion(props.file.segments)
  })
})

const isFetching = ref(false)
async function handleProcess() {
  isFetching.value = true
  try {
    let segments: PostAudioSplit200SegmentsItem[]
    if (props.file.segments) {
      segments = props.file.segments
    }
    else {
      const { data } = await postAudioSplit({ filePath: props.file.filePath })

      if (!data.segments || !data.segments?.length) {
        toast({ content: 'This audio cannot be splitted' })
        throw new Error('This audio cannot be splitted')
      }

      segments = data.segments
      emits('succeedProcess', segments)
    }

    addRegion(segments)
  }
  catch (e) { console.log(e) }
  finally { isFetching.value = false }
}

function addRegion(segments: PostAudioSplit200SegmentsItem[]) {
  segments.forEach(({ duration, metadataOptions, offset }) => {
    if (!duration || !metadataOptions || !offset)
      return

    const opts = metadataOptions.map(o => ({
      ...o, title: o.title ?? 'unknown', artist: o.artist ?? 'unknown',
    }))

    const contentEl = document.createElement('div')
    contentEl.innerHTML = Object.entries(opts[0]).map(([key, value]) =>
        `<span
          class="${key}"
          style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden;"
        >
          ${key}: ${value}
        </span>`,
    ).join('\n')

    regions.value && regions.value.addRegion({
      start: offset,
      end: offset + duration,
      content: contentEl,
      color: useRandomColor(),
      drag: false,
      resize: false,
    })
  })
}

async function handleSave({ duration, offset, name }: { duration: number; offset: number; name: string }) {
  const newHandle = await window.showSaveFilePicker({
    suggestedName: `${name.replaceAll(' ', '_')}.wav`,
    types: [{
      description: 'WAV file',
      accept: { 'audio/wav': ['.wave'] },
    }],
  })

  const { data: blob } = await postAudioGetSegment({
    filePath: props.file.filePath,
    duration,
    offset,
  })

  if (!blob)
    return

  const writableStream = await newHandle.createWritable()
  await writableStream.write(blob)
  await writableStream.close()
}
</script>

<template>
  <div class="space-y-2">
    <div class="flex items-center gap-x-2">
      <span class="text-sm" :class="file.segments ? 'i-carbon:checkmark-filled' : 'i-carbon:subtract-alt'" />
      <p> {{ file.fileName }} </p>
    </div>

    <div class="relative">
      <div id="waveform" class="min-h-128px border rounded-md" />

      <div v-if="isAudioLoading" class="absolute-center">
        <BaseLoader />
      </div>
    </div>

    <p v-if="file.fileType === 'webm'" class="text-center text-sm text-muted-foreground">
      .wav cannot be processed at the moment!
    </p>

    <div class="flex-center">
      <BaseButton
        :disabled="file.fileType === 'webm' || isFetching || file.segments"
        @click="handleProcess"
      >
        <BaseLoader
          v-if="isFetching"
          class="mr-2 border-primary-foreground !border-2"
          :size="15"
        />
        Process
      </BaseButton>
    </div>

    <table id="create_project_files_list" class="w-full caption-bottom text-sm">
      <caption class="mt-4 text-sm text-muted-foreground">
        A list of found songs
      </caption>
      <thead>
        <tr class="border-b border-b-border">
          <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
            {{ t('song.title') }}
          </th>

          <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
            {{ t('song.artist') }}
          </th>

          <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
            {{ t('song.album') }}
          </th>

          <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
            {{ t('song.year') }}
          </th>

          <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
            {{ t('song.duration') }}
          </th>

          <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
            {{ t('button.edit') }}
          </th>

          <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
            {{ t('button.save') }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="({ duration, metadataOptions, offset }, index) in file.segments" :key="index" class="border-b border-b-border">
          <template v-if="metadataOptions">
            <td class="p-4 align-middle font-medium">
              {{ metadataOptions[0].title ?? 'unknown' }}
            </td>

            <td class="p-4 align-middle">
              {{ metadataOptions[0].artist ?? 'unknown' }}
            </td>

            <td class="p-4 align-middle">
              {{ metadataOptions[0].album ?? 'unknown' }}
            </td>

            <td class="p-4 align-middle">
              {{ metadataOptions[0].year ?? 'unknown' }}
            </td>

            <td class="p-4 align-middle">
              {{ useConvertSecToMin(duration ?? 0) }}
            </td>

            <td class="p-4 align-middle">
              <BaseButton icon-only variant="ghost">
                <span class="i-carbon-edit" />
              </BaseButton>
            </td>

            <td class="p-4 align-middle">
              <BaseButton
                :disabled="!duration || !offset" icon-only variant="ghost" @click="duration && offset && handleSave({
                  duration,
                  offset,
                  name: metadataOptions[0].title,
                })"
              >
                <span class="i-carbon-download" />
              </BaseButton>
            </td>
          </template>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
#waveform ::part(region-content){
  @apply: flex flex-col gap-y-0.5 p-2 pr-3 min-w-100px max-w-150px lg:max-w-200px xl:max-w-250px bg-primary-foreground/80 text-primary text-sm rounded-br-md;
}
</style>
