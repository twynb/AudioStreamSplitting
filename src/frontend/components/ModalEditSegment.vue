<script setup lang="ts">
import type { Metadata } from 'models/api'
import WaveSurfer from 'wavesurfer.js'

const props = defineProps<{
  /**
   * Index of segment
   */
  segmentIndex: number
  /**
   * Current metaIndex of segment
   */
  metaIndex: number
  /**
   * Array of found metadata of segment
   */
  metadata: Metadata[]
  /**
   * Url for editing segment
   */
  url: string
  /**
   * Computed peaks for segment
   */
  peaks?: number[][]
}>()

const emits = defineEmits<{
  /**
   * Emits an event 'ok' when the "OK" action is triggered.
   * @property {number} metaIndex new value for metaIndex
   */
  (e: 'ok', metaIndex: number): void
  /**
   * Emits an event 'cancel' when the "Cancel" action is triggered.
   */
  (e: 'cancel'): void
  /**
   * Emits an event when file's peaks are computed.
   * @property {number[]} value Array of peak values.
   */
  (e: 'updatePeaks', value: number[][]): void
}>()

const { isDark } = useDarkToggle()
const { t } = useI18n()

const ws = shallowRef<WaveSurfer>()
const index = ref(props.metaIndex)

const _metadata = ref(props.metadata)
const currentProcess = ref(0)
const currentTime = ref(0)
const duration = ref(1)

const isMouseOverRow = ref(false)
const isAudioLoading = ref(true)
const isPlaying = ref(false)
const isInteractingWithSlider = ref(false)

const formatedCurrentTime = computed(() => useConvertSecToMin(currentTime.value, 'mm:ss'))
const formatedDuration = computed(() => useConvertSecToMin(duration.value, 'mm:ss'))

onMounted(() => {
  ws.value = WaveSurfer.create({
    container: '#waveform',
    waveColor: isDark.value ? 'hsl(81, 96%, 55%)' : 'hsl(81, 96%, 45%)',
    progressColor: isDark.value ? 'hsl(79, 36%, 50%)' : 'hsl(79, 36%, 42%)',
    barRadius: 5,
    barWidth: 5,
    barGap: 2,
    cursorWidth: 3,
    url: props.url,
    peaks: props.peaks,
    dragToSeek: true,
  })

  ws.value.on('ready', () => {
    isAudioLoading.value = false
    duration.value = ws.value?.getDuration() ?? 1
    emits ('updatePeaks', ws.value?.exportPeaks() ?? [])
  })
  ws.value.on('timeupdate', (t) => {
    if (isInteractingWithSlider.value)
      return

    currentTime.value = t
    currentProcess.value = currentTime.value * 100 / duration.value
  })

  watch(currentProcess, () => {
    if (!isInteractingWithSlider.value)
      return

    ws.value?.seekTo(currentProcess.value / 100)
  })
  ws.value.on('finish', () => isPlaying.value = false)
})

function handlePlayPause() {
  isPlaying.value = !isPlaying.value
  if (isPlaying.value)
    ws.value?.play()
  else ws.value?.pause()
}

function handleDeleteMetadata(i: number) {
  if (index.value === i)
    index.value = 0
  _metadata.value.splice(i, 1)
}

function handleUpdateMetadata(i: number, key: keyof typeof _metadata.value[0], event: Event) {
  const el = event.currentTarget as HTMLElement
  _metadata.value[i][key] = el.textContent ?? ''
}
</script>

<template>
  <BaseModal>
    <template #header>
      <h2 class="text-2xl">
        {{ t('song.change_metadata_for_segment', { index: segmentIndex + 1 }) }}
      </h2>
    </template>

    <template #body>
      <div>
        <div class="relative">
          <div id="waveform" class="min-h-128px border rounded-md" />

          <div v-if="isAudioLoading" class="absolute-center">
            <BaseLoader />
          </div>
        </div>

        <div class="mt-5" @mouseover="isInteractingWithSlider = true" @mouseleave="isInteractingWithSlider = false">
          <BaseSlider v-model="currentProcess" />
        </div>

        <div class="mt-3 flex items-start justify-between">
          <span class="min-w-25px text-sm">{{ formatedCurrentTime }}</span>
          <BaseButton icon-only variant="ghost" @click="handlePlayPause">
            <span v-if="isPlaying" class="i-carbon:pause-filled text-xl" />
            <span v-else class="i-carbon:play-filled-alt text-xl" />
          </BaseButton>
          <span class="min-w-25px text-sm">{{ formatedDuration }}</span>
        </div>
      </div>

      <div class="max-h-400px max-w-1300px wh-full overflow-auto py-5">
        <table class="w-full caption-bottom text-sm">
          <thead class="sticky left-0 right-0 top-0 z-2 bg-primary-foreground">
            <tr class="border-b border-b-border">
              <th class="sticky left-0 top-0 z-1 h-12 bg-primary-foreground px-4 text-left align-middle font-medium text-muted-foreground">
                  &nbsp;
              </th>

              <th class="sticky sticky left-50px left-53px top-0 top-0 z-1 z-1 h-12 bg-primary-foreground px-4 text-left align-middle font-medium text-muted-foreground">
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
                {{ t('song.albumartist') }}
              </th>

              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
                {{ t('song.genre') }}
              </th>

              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
                {{ t('song.isrc') }}
              </th>

              <th class="sticky right-0 top-0 z-1 h-12 bg-primary-foreground px-4 text-right align-middle font-medium text-muted-foreground">
                {{ t('button.delete') }}
              </th>
            </tr>
          </thead>

          <tbody :key="_metadata.length">
            <tr
              v-for="({ title, artist, album, year, albumartist, genre, isrc }, i) in _metadata"
              :key="i" class="group cursor-pointer border-b border-b-border hover:bg-secondary"
              :class="!isMouseOverRow && index === i ? 'bg-secondary' : 'bg-primary-foreground'"
              @mouseover="isMouseOverRow = true"
              @mouseleave="isMouseOverRow = false"
              @click="index = i"
            >
              <td
                class="sticky left-0 top-0 z-1 px-4 align-middle group-hover:bg-secondary"
                :class="!isMouseOverRow && index === i ? 'bg-secondary' : 'bg-primary-foreground'"
              >
                <span v-if="i === index" class="i-carbon:checkmark mt-1" />
              </td>

              <td
                class="sticky left-50px top-0 z-1 min-w-200px p-4 align-middle font-medium outline-none group-hover:bg-secondary focus:text-neon"
                :class="!isMouseOverRow && index === i ? 'bg-secondary' : 'bg-primary-foreground'"
                contenteditable
                @input="(e) => handleUpdateMetadata(i, 'title', e)"
              >
                {{ title ?? t('song.unknown') }}
              </td>

              <td
                class="min-w-150px p-4 align-middle outline-none focus:text-neon"
                contenteditable
                @input="(e) => handleUpdateMetadata(i, 'artist', e)"
              >
                {{ artist ?? t('song.unknown') }}
              </td>

              <td
                class="min-w-350px p-4 align-middle outline-none focus:text-neon"
                contenteditable
                @input="(e) => handleUpdateMetadata(i, 'album', e)"
              >
                {{ album ?? t('song.unknown') }}
              </td>

              <td
                class="min-w-100px p-4 align-middle outline-none focus:text-neon"
                contenteditable
                @input="(e) => handleUpdateMetadata(i, 'year', e)"
              >
                {{ year ?? t('song.unknown') }}
              </td>

              <td
                class="min-w-120px p-4 align-middle outline-none focus:text-neon"
                contenteditable
                @input="(e) => handleUpdateMetadata(i, 'albumartist', e)"
              >
                {{ albumartist ?? t('song.unknown') }}
              </td>

              <td
                class="min-w-100px p-4 align-middle outline-none focus:text-neon"
                contenteditable
                @input="(e) => handleUpdateMetadata(i, 'genre', e)"
              >
                {{ genre ?? t('song.unknown') }}
              </td>

              <td
                class="min-w-120px p-4 align-middle outline-none focus:text-neon"
                contenteditable
                @input="(e) => handleUpdateMetadata(i, 'isrc', e)"
              >
                {{ isrc ?? t('song.unknown') }}
              </td>

              <td
                class="sticky right-0 top-0 z-1 px-4 align-middle group-hover:bg-secondary"
                :class="!isMouseOverRow && index === i ? 'bg-secondary' : 'bg-primary-foreground'"
              >
                <BaseButton
                  variant="ghost" icon-only
                  :disabled="_metadata.length <= 1"
                  @click.stop="handleDeleteMetadata(i)"
                >
                  <span class="i-carbon:trash-can" />
                </BaseButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="flex justify-center">
        <BaseButton @click=" _metadata.push({ ..._metadata[index] })">
          <span class="i-carbon:add mr-1" /> {{ t('button.new') }}
        </BaseButton>
      </div>

      <p class="mt-5 text-center text-muted-foreground">
        {{ t('song.metadata_list_caption', { count: _metadata.length }) }}
      </p>
    </template>

    <template #footer>
      <div class="flex justify-end gap-x-2">
        <BaseButton variant="secondary" @click="emits('cancel')">
          {{ t('button.cancel') }}
        </BaseButton>

        <BaseButton @click="emits('ok', index)">
          {{ t('button.change') }}
        </BaseButton>
      </div>
    </template>
  </BaseModal>
</template>
