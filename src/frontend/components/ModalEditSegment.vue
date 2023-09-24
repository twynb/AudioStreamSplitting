<script setup lang="ts">
import type { Metadata } from 'models/api'

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
}>()

const { t } = useI18n()
const index = ref(props.metaIndex)
const isMouseOverRow = ref(false)
</script>

<template>
  <BaseModal>
    <template #header>
      <h2 class="text-2xl">
        {{ t('song.change_metadata_for_segment', { index: segmentIndex + 1 }) }}
      </h2>
    </template>

    <template #body>
      <div class="max-h-400px max-w-1000px wh-full overflow-auto pb-5">
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
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="({ title, artist, album, year, albumartist, genre, isrc }, i) in metadata"
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
                class="sticky left-50px top-0 z-1 min-w-200px p-4 align-middle font-medium group-hover:bg-secondary"
                :class="!isMouseOverRow && index === i ? 'bg-secondary' : 'bg-primary-foreground'"
              >
                {{ title ?? t('song.unknown') }}
              </td>

              <td class="min-w-150px p-4 align-middle">
                {{ artist ?? t('song.unknown') }}
              </td>

              <td class="min-w-350px p-4 align-middle">
                {{ album ?? t('song.unknown') }}
              </td>

              <td class="min-w-100px p-4 align-middle">
                {{ year ?? t('song.unknown') }}
              </td>

              <td class="min-w-120px p-4 align-middle">
                {{ albumartist ?? t('song.unknown') }}
              </td>

              <td class="min-w-100px p-4 align-middle">
                {{ genre ?? t('song.unknown') }}
              </td>

              <td class="min-w-120px p-4 align-middle">
                {{ isrc ?? t('song.unknown') }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <p class="mt-6 text-center text-muted-foreground">
        {{ t('song.metadata_list_caption') }}
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
