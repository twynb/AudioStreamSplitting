<script setup lang="ts">
import WaveSurfer from 'wavesurfer.js'
import Regions from 'wavesurfer.js/plugins/regions'
import type { AxiosError } from 'axios'
import { isAxiosError } from 'axios'
import { useLocalStorage } from '@vueuse/core'
import type { Project, ProjectFileSegment } from '../models/types'
import type { Metadata, PostAudioSplitBodyPresetName } from '../models/api'
import { getAudioStreamSplittingAPI } from '../models/api'
import { SUPPORT_FILE_TYPES } from '../includes/constants'
import ConfirmModal from './ConfirmModal.vue'
import EditSongModal from './EditSongModal.vue'

const props = defineProps<{
  /**
   * File object passed from Project
   */
  file: Project['files'][0]
}>()

const emits = defineEmits<{
  /**
   * Emits an event when file is successfully processed.
   * @property {ProjectFileSegment[]} value Array of found segments
   */
  (e: 'succeedProcess', v: ProjectFileSegment[]): void
  /**
   * Emits an event when file's peaks are computed.
   * @property {ProjectFileSegment[]} value Array of peak values.
   */
  (e: 'updatePeaks', v: number[][]): void
  /**
   * Emits an event when meta of each segment is changed.
   * @property {number} songIndex Segment index in file.
   * @property {number} metaIndex Meta index in segment.
   */
  (e: 'changeMeta', songIndex: number, metaIndex: number): void
  (e: 'changePresetName', presetName: PostAudioSplitBodyPresetName): void
}>()

const { toast } = useToastStore()
const { t } = useI18n()
const router = useRouter()
const hash = useHash(props.file.filePath)
const saveSettings = useLocalStorage('save-settings', { fileType: 'mp3', shouldAsk: true })

const ws = shallowRef<WaveSurfer>()
const regions = shallowRef<Regions>()
const isAudioLoading = ref(true)
const { postAudioSplit, postAudioStore } = getAudioStreamSplittingAPI()

onMounted(async () => {
  try {
    const audioPath = props.file.filePath
    await axios.post('/audio/check_path', { audioPath })
    const { data } = await axios.post('/audio/get', { audioPath }, { responseType: 'blob' })
    const url = URL.createObjectURL(data)

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
  }
  catch (e) {
    router.push('/')
    toast({ content: t((e as AxiosError).response?.data as string), variant: 'destructive' })
  }
})

const presetNameOpts = [
  { value: 'EXTRA_STRICT', label: t('song.preset.extra_strict') },
  { value: 'STRICT', label: t('song.preset.strict') },
  { value: 'NORMAL', label: t('song.preset.normal') },
  { value: 'LENIENT', label: t('song.preset.lenient') },
  { value: 'EXTRA_LENIENT', label: t('song.preset.extra_lenient') },
]
const isProcessing = ref(false)
const presetName = ref(props.file.presetName ?? 'EXTRA_STRICT')
watch(presetName, () => emits('changePresetName', presetName.value))

async function handleProcess() {
  isProcessing.value = true
  regions.value?.clearRegions()

  try {
    toast({ content: t('toast.long_process') })
    const { data } = await postAudioSplit({ filePath: props.file.filePath, presetName: presetName.value })

    if (!data.segments || !data.segments?.length)
      throw new Error('This audio cannot be split')

    data.segments = data.segments
      .map((s) => {
        const notNullOpts = s.metadataOptions?.filter(o => o.album || o.artist || o.title || o.year)
        const notDuplicatedOpts = [...new Set((notNullOpts ?? []).map(o => JSON.stringify(o)))]
          .map(o => JSON.parse(o))
        return { ...s, metadataOptions: notDuplicatedOpts }
      })

    const segments = data.segments.map(s => ({ ...s, metaIndex: 0 }))
    emits('succeedProcess', segments)
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
  { duration, offset, metadata, songIndex, fileType }: { duration: number; offset: number; metadata?: Metadata; songIndex: number; fileType: string },

) {
  const filePath = props.file.filePath
  const targetDirectory = store.lsEnv.SAVE_DIRECTORY
  if (!targetDirectory) {
    toast({ title: t('toast.title.no_save_directory'), content: t('toast.no_save_directory'), variant: 'destructive' })
    return
  }

  currentStoringIndex.value = songIndex
  isStoring.value = true

  const _metadata = metadata ?? { album: '', artist: '', title: 'unknown', year: '0' }

  try {
    await postAudioStore({ filePath, duration, offset, metadata: _metadata, targetDirectory, fileType })
    toast({
      title: `${_metadata.title}.${fileType}`,
      content: t('toast.save_file_success', { target: targetDirectory }),
    })
  }
  catch (e) {
    if (isAxiosError(e) && (e as AxiosError).response?.data)
      toast({ content: t((e as AxiosError).response?.data as string), variant: 'destructive' })
    else
      toast({ content: t('toast.unkown_error'), variant: 'destructive' })

    currentStoringIndex.value = -1
    isStoring.value = false
    throw e
  }

  currentStoringIndex.value = -1
  isStoring.value = false
}

const isStoringAll = ref(false)
const isSaveAllBtnDisabled = computed(() => !props.file.segments || !props.file.segments.length || isStoring.value || isStoringAll.value)
async function handleStoreAll(
  { fileType }: { fileType: string },
) {
  if (!props.file.segments)
    return

  isStoringAll.value = true
  for await (const [songIndex, { offset, duration, metadataOptions, metaIndex }] of props.file.segments.entries()) {
    if (!offset || !duration)
      return

    try {
      await handleStore({ offset, duration, songIndex, fileType, metadata: metadataOptions?.[metaIndex] })
    }
    catch (e) {
      isStoringAll.value = false
      break
    }
  }

  isStoringAll.value = false
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

    <div class="relative flex items-end justify-between pb-3 pt-1">
      <div class="space-y-1">
        <BaseLabel>{{ t('song.preset.index') }}</BaseLabel>
        <BaseSelect
          v-model="presetName"
          :disabled="isProcessing"
          :options="presetNameOpts"
          class="min-w-200px -ml-1"
        />
      </div>

      <BaseButton
        class="absolute bottom-3 left-1/2 -translate-x-1/2"
        :disabled="isAudioLoading || isProcessing"
        @click="handleProcess"
      >
        <BaseLoader
          v-if="isProcessing"
          class="mr-2 border-primary-foreground !border-2"
          :size="15"
        />
        {{ t('button.process') }}
      </BaseButton>

      <BaseMenuButton
        v-if="saveSettings.shouldAsk"
        variant="primary"
        :icon-only="false"
        menu-class="!top-[calc(100%+0.5rem)] w-full"
        :length="SUPPORT_FILE_TYPES.length"
        :disabled="isSaveAllBtnDisabled"
      >
        <template #button>
          <div class="flex items-center gap-2">
            {{ t('button.save_all') }}
            <BaseLoader
              v-if=" isStoringAll"
              class="border-primary-foreground !border-2"
              :size="15"
            />
            <span v-else class="i-carbon-download" />
          </div>
        </template>
        <template #content="{ index: ftIndex }">
          <li class="px-1">
            <BaseButton
              variant="ghost" class="w-full"
              @click="handleStoreAll({ fileType: SUPPORT_FILE_TYPES[ftIndex] })"
            >
              {{ `.${SUPPORT_FILE_TYPES[ftIndex]}` }}
            </BaseButton>
          </li>
        </template>
      </BaseMenuButton>

      <BaseButton
        v-else
        :disabled="isSaveAllBtnDisabled"
        @click="handleStoreAll({ fileType: saveSettings.fileType })"
      >
        <div class="flex items-center gap-2">
          {{ t('button.save_all') }}
          <BaseLoader
            v-if=" isStoringAll"
            class="border-primary-foreground !border-2"
            :size="15"
          />
          <span v-else class="i-carbon-download" />
        </div>
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

          <th class="h-12 px-4 text-right align-middle font-medium text-muted-foreground">
            {{ t('button.edit') }}
          </th>

          <th class="h-12 px-4 text-right align-middle font-medium text-muted-foreground">
            {{ t('button.save') }}
          </th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="({ duration, offset, metaIndex, metadataOptions }, songIndex) in file.segments"
          :key="songIndex" class="border-b border-b-border"
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

          <td class="p-4 text-right align-middle">
            <BaseButton
              icon-only variant="ghost"
              :disabled="file.segments && (file.segments[songIndex].metadataOptions?.length ?? 0) <= 1"
              @click="handleEdit(songIndex)"
            >
              <span class="i-carbon-edit" />
            </BaseButton>
          </td>

          <td class="p-4 text-right align-middle">
            <BaseMenuButton
              v-if="saveSettings.shouldAsk"
              :disabled="!duration || !offset || isStoring"
              :length="SUPPORT_FILE_TYPES.length"
            >
              <template #button>
                <BaseLoader
                  v-if="currentStoringIndex === songIndex && isStoring"
                  class="border-primary !border-2"
                  :size="15"
                />
                <span v-else class="i-carbon-download" />
              </template>
              <template #content="{ index: ftIndex }">
                <li class="px-1">
                  <BaseButton
                    variant="ghost"
                    @click="duration && offset && handleStore({
                      duration,
                      offset,
                      metadata: metadataOptions?.[metaIndex],
                      songIndex,
                      fileType: SUPPORT_FILE_TYPES[ftIndex],
                    })"
                  >
                    {{ `.${SUPPORT_FILE_TYPES[ftIndex]}` }}
                  </BaseButton>
                </li>
              </template>
            </BaseMenuButton>

            <BaseButton
              v-else
              variant="ghost"
              :disabled="!duration || !offset || isStoring"
              @click="duration && offset && handleStore({
                duration,
                offset,
                metadata: metadataOptions?.[metaIndex],
                songIndex,
                fileType: saveSettings.fileType,
              })"
            >
              <BaseLoader
                v-if="currentStoringIndex === songIndex && isStoring"
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
