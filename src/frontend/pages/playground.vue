<script setup lang="ts">
import { useFileDialog } from '@vueuse/core'

const { t } = useI18n()

const data = ref({
  name: '',
  description: '',
  files: [] as File[],
})

const { files, open, onChange } = useFileDialog({
  accept: '.mp3, .wav',
  multiple: true,
})

onChange(() => {
  if (!files.value)
    return

  const result: File[] = []
  for (let i = 0; i < files.value.length; i++) {
    const file = files.value.item(i)
    file && isFileValid(file.type) && result.push(file)
  }

  data.value.files = result
})

const isDragOver = ref(false)

function isFileValid(type: string) {
  const splittedType = type.split('/').length > 1 ? type.split('/') : ['', '']

  const fileType = splittedType[0]
  if (fileType !== 'audio')
    return false

  const fileExt = splittedType[1]
  if (!['mpeg', 'wav'].includes(fileExt))
    return false

  return true
}

function handleDeleteUploadedFile(name: string) {
  data.value.files = data.value.files.filter(file => file.name !== name)
}

function handleDrop(event: DragEvent) {
  isDragOver.value = false

  const file = event.dataTransfer?.files.item(0)

  if (!file)
    return

  if (!isFileValid(file.type))
    return

  if (data.value.files.find(f => f.name === file.name))
    return

  data.value.files.push(file)
}
</script>

<template>
  <ContentLayout header="Playground (dev only)">
    <div class="border border-border rounded-sm bg-background p-6 focus:outline-none">
      <div class="grid grid-cols-2 gap-4">
        <div class="space-y-1">
          <BaseLabel for="name">
            {{ t('global.name') }}
          </BaseLabel>
          <BaseInput id="name" v-model="data.name" name="name" />
        </div>

        <div class="space-y-1">
          <BaseLabel for="description">
            {{ t('global.description') }}
          </BaseLabel>
          <BaseInput id="description" v-model="data.description" name="description" />
        </div>

        <div class="col-span-2 space-y-1">
          <BaseLabel @click="open()">
            {{ t('global.upload') }}
          </BaseLabel>

          <div
            class="group h-200px flex flex-center flex-col cursor-pointer border-2 rounded-md border-dashed transition-border-color"
            :class="[isDragOver ? 'border-accent-foreground/70' : 'border-border hover:border-accent-foreground/70']"
            @click="open()"
            @dragenter="isDragOver = true"
            @dragover="isDragOver = true"
            @dragleave="isDragOver = false"
            @dragenter.prevent
            @dragover.prevent
            @drop.prevent="handleDrop"
          >
            <span
              class="i-carbon-upload text-3xl transition-color"
              :class="[isDragOver ? 'text-primary' : 'text-primary/40 group-hover:text-primary']"
            />

            <p
              class="mt-2 transition-color"
              :class="[isDragOver ? 'text-primary' : 'text-primary/80 group-hover:text-primary']"
            >
              {{ t('dashboard.project.drag_and_drop_or_browse') }}
            </p>

            <p class="mt-2 text-xs text-primary/40">
              {{ t('dashboard.project.support_mp3_and_wav_files') }}
            </p>
          </div>
        </div>

        <div class="overflow col-span-2 space-y-1">
          <table class="w-full caption-bottom text-sm">
            <caption class="mt-4 text-sm text-muted-foreground">
              {{ t('dashboard.project.a_list_of_your_uploaded_files') }}
            </caption>
            <thead>
              <tr class="border-b">
                <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
                  {{ t('global.name') }}
                </th>

                <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
                  {{ t('global.size') }}
                </th>

                <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
                  {{ t('global.last_modified') }}
                </th>

                <th />
              </tr>
            </thead>
            <tbody>
              <tr v-for="{ name, size, lastModified } in data.files" :key="name" class="border-b">
                <td class="p-4 align-middle font-medium">
                  {{ name }}
                </td>

                <td class="p-4 align-middle">
                  {{ (size / 1_000_000).toPrecision(3) }} MB
                </td>

                <td class="p-4 text-left align-middle">
                  {{ useDateFormat(lastModified, 'DD/MM/YYYY') }}
                </td>

                <td class="cursor-pointer pr-4 text-right align-middle transition-color hover:text-destructive" @click="handleDeleteUploadedFile(name)">
                  <span class="i-carbon-close -mb-1" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </ContentLayout>
</template>
