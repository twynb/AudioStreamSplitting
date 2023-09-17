<script setup lang="ts">
import WaveSurfer from 'wavesurfer.js'
import Regions from 'wavesurfer.js/plugins/regions'
import type { Project, ProjectFileSegment } from '../models/types'
import type { Metadata } from '../models/api'
import { getAudioStreamSplittingAPI } from '../models/api'
import ConfirmModal from './ConfirmModal.vue'
import EditSongModal from './EditSongModal.vue'

const props = defineProps<{ file: Project['files'][0] }>()

const emits = defineEmits<{
  (e: 'succeedProcess', v: ProjectFileSegment[]): void
  (e: 'updatePeaks', v: number[][]): void
  (e: 'changeMeta', songIndex: number, metaIndex: number): void
}>()

const { postAudioSplit, postAudioStore } = getAudioStreamSplittingAPI()
const { toast } = useToastStore()
const { t } = useI18n()
const { data } = await axios.post('/audio/get', { audioPath: props.file.filePath }, { responseType: 'blob' })
const url = URL.createObjectURL(data)
const isAudioLoading = ref(true)

const ws = shallowRef<WaveSurfer>()
const regions = shallowRef<Regions>()

const hash = useHash(props.file.filePath)

onMounted(() => {
  ws.value = WaveSurfer.create({
    container: `#waveform_${hash}`,
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

const isProcessing = ref(false)
async function handleProcess() {
  isProcessing.value = true
  try {
    let segments: ProjectFileSegment[]
    if (props.file.segments) {
      segments = props.file.segments
    }
    else {
      toast({ content: t('toast.long_process') })
      const { data } = await postAudioSplit({ filePath: props.file.filePath })

      if (!data.segments || !data.segments?.length)
        throw new Error('This audio cannot be split')

      data.segments = data.segments
        .map((s) => {
          const notNullOpts = s.metadataOptions?.filter(o => o.album || o.artist || o.title || o.year)
          const notDuplicatedOpts = [...new Set((notNullOpts ?? []).map(o => JSON.stringify(o)))]
            .map(o => JSON.parse(o))
          return { ...s, metadataOptions: notDuplicatedOpts }
        })

      segments = data.segments.map(s => ({ ...s, metaIndex: 0 }))

      emits('succeedProcess', segments)
    }

    addRegion(segments)
  }
  catch (e) {
    toast({ content: t('toast.cant_split'), variant: 'destructive' })
  }
  finally { isProcessing.value = false }
}

function addRegion(segments: ProjectFileSegment[]) {
  segments.forEach(({ duration, metadataOptions, offset, metaIndex }) => {
    if (!duration || !offset)
      return

    const meta = metadataOptions?.[metaIndex]

    const contentEl = document.createElement('div')
    if (meta) {
      contentEl.innerHTML = Object.entries(meta).map(([key, value]) =>
      `<span style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">
        ${key}: ${value}
      </span>`,
      ).join('\n')
    }
    else {
      contentEl.innerHTML = `
      <span style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">
        ${t('song.no_meta')}
      </span>`
    }

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

const isStoring = ref(false)
const currentStoringIndex = ref(-1)
const store = useEnvStore()
async function handleStore(
  { duration, offset, metadata }: { duration: number; offset: number; metadata: Metadata },
  songIndex: number,
) {
  const filePath = props.file.filePath
  const targetDirectory = store.lsEnv.SAVE_DIRECTORY
  if (!targetDirectory) {
    toast({ title: t('toast.title.no_save_directory'), content: t('toast.no_save_directory'), variant: 'destructive' })
    return
  }

  currentStoringIndex.value = songIndex
  isStoring.value = true

  try {
    await postAudioStore({ filePath, duration, offset, metadata, targetDirectory })
    toast({ title: metadata.title, content: t('toast.save_file_success', { target: targetDirectory }) })
  }
  catch (e) {
    toast({ content: t('toast.unkown_error'), variant: 'destructive' })
  }

  currentStoringIndex.value = -1
  isStoring.value = false
}

function handleEdit(songIndex: number) {
  let newMetaIndex = 0
  const { open, close } = useModal({
    component: ConfirmModal,
    attrs: {
      contentClass: 'max-w-50vw lg:max-w-[500px]',
      onCancel() { close() },
      onOk() {
        emits('changeMeta', songIndex, newMetaIndex)
        regions.value?.clearRegions()
        props.file.segments && addRegion(props.file.segments)
        close()
      },
    },
    slots: {
      default: {
        component: h(EditSongModal, {
          metadatas: props.file.segments?.[songIndex]?.metadataOptions ?? [],
          opt: `${props.file.segments?.[songIndex]?.metaIndex ?? 0}`,
          onChange(v) { newMetaIndex = v },
        }),
      },
    },
  })

  open()
}
</script>

<template>
  <div class="space-y-2">
    <p> {{ file.fileName }} </p>

    <div class="relative">
      <div :id="`waveform_${hash}`" class="waveform min-h-128px border rounded-md" />

      <div v-if="isAudioLoading" class="absolute-center">
        <BaseLoader />
      </div>
    </div>

    <p v-if="file.fileType === 'webm'" class="text-center text-sm text-muted-foreground">
      {{ t('song.no_webm') }}
    </p>

    <div class="flex-center py-2">
      <BaseButton
        :disabled="file.fileType === 'webm' || isProcessing || file.segments"
        @click="handleProcess"
      >
        <BaseLoader
          v-if="isProcessing"
          class="mr-2 border-primary-foreground !border-2"
          :size="15"
        />
        {{ t('button.process') }}
      </BaseButton>
    </div>

    <table class="w-full caption-bottom text-sm">
      <caption class="mt-4 text-sm text-muted-foreground">
        {{ t('song.list_caption') }}
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
        <tr
          v-for="({ duration, offset, metaIndex, metadataOptions }, index) in file.segments"
          :key="index" class="border-b border-b-border"
        >
          <td class="p-4 align-middle font-medium">
            {{ metadataOptions?.[metaIndex]?.title ?? 'unknown' }}
          </td>

          <td class="p-4 align-middle">
            {{ metadataOptions?.[metaIndex]?.artist ?? 'unknown' }}
          </td>

          <td class="p-4 align-middle">
            {{ metadataOptions?.[metaIndex]?.album ?? 'unknown' }}
          </td>

          <td class="p-4 align-middle">
            {{ metadataOptions?.[metaIndex]?.year ?? 'unknown' }}
          </td>

          <td class="p-4 align-middle">
            {{ useConvertSecToMin(duration ?? 0) }}
          </td>

          <td class="p-4 align-middle">
            <BaseButton
              icon-only variant="ghost"
              :disabled="file.segments && (file.segments[index].metadataOptions?.length ?? 0) <= 1"
              @click="handleEdit(index)"
            >
              <span class="i-carbon-edit" />
            </BaseButton>
          </td>

          <td class="p-4 align-middle">
            <BaseButton
              icon-only variant="ghost"
              :disabled="!duration || !offset || isStoring"
              @click="duration && offset && handleStore({
                duration,
                offset,
                metadata: metadataOptions?.[metaIndex] ?? { album: 'unknown', artist: 'unknown', title: 'unknown', year: 'unknown' },
              }, index)"
            >
              <BaseLoader
                v-if="currentStoringIndex === index && isStoring"
                class="border-primary !border-2"
                :size="15"
              />
              <span v-else class="i-carbon-download" />
            </BaseButton>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.waveform ::part(region-content){
  @apply: flex flex-col gap-y-0.5 p-2 pr-3 min-w-100px max-w-150px lg:max-w-200px xl:max-w-250px bg-primary-foreground/80 text-primary text-sm rounded-br-md !mt-0;
}
</style>
