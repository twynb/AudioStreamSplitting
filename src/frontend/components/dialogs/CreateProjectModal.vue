<script setup lang="ts">
import { useFileDialog } from '@vueuse/core'

const emits = defineEmits<{
  (e: 'close'): void
  (e: 'ok', data: Data): void
}>()

const { t } = useI18n()
const { getProjects } = useDBStore()
const { driver } = storeToRefs(useDriverStore())
onMounted(() => {
  const input = document.querySelector('form#create_project_form')?.querySelector('input#name') as HTMLInputElement
  input && input.focus()
})

const data = ref({
  name: '',
  description: '',
  files: [] as File[],
})
export type Data = typeof data.value

const errors = ref({
  name: '',
  file: '',
})

const isDragOver = ref(false)

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

function handleSubmit() {
  if (data.value.name && data.value.files.length) {
    errors.value = { file: '', name: '' }
    emits('ok', data.value)
  }

  errors.value.name = data.value.name ? '' : 'No name is given'
  if (getProjects().find(p => p.name === data.value.name))
    errors.value.name = `${data.value.name} is already existed. Please choose an other name.`
  if (errors.value.name && driver.value.isActive()) {
    driver.value.moveTo(1)
    return
  }

  errors.value.file = data.value.files.length ? '' : 'No file is uploaded. Please upload at least one file to create project.'
  if (errors.value.file && driver.value.isActive())
    driver.value.moveTo(3)
}
</script>

<template>
  <BaseModal :title="t('dialog.create_project.title')" content-class="w-full max-w-65vw 2xl:max-w-50vw">
    <template #body>
      <form id="create_project_form" class="space-y-4" @submit.prevent="handleSubmit">
        <div class="flex gap-x-4">
          <div id="create_project_name" class="grow space-y-1">
            <BaseLabel for="name" :has-error="!!errors.name">
              {{ t('dialog.create_project.project_name') }}
            </BaseLabel>
            <BaseInput id="name" v-model="data.name" name="name" />
            <BaseError :error="errors.name" />
          </div>

          <div id="create_project_description" class="grow space-y-1">
            <BaseLabel for="description">
              {{ t('dialog.create_project.project_description') }}
            </BaseLabel>
            <BaseInput id="description" v-model="data.description" name="description" />
          </div>
        </div>

        <div id="create_project_files" class="space-y-1">
          <BaseLabel :has-error="!!errors.file" @click="open()">
            {{ t('dialog.create_project.project_upload') }}
          </BaseLabel>

          <div
            tabindex="0"
            class="group h-150px flex flex-center flex-col cursor-pointer border-2 rounded-md border-dashed transition-border-color"
            :class="[isDragOver ? 'border-accent-foreground/70' : 'border-border hover:border-accent-foreground/70']"
            @click="open()"
            @keydown.enter.prevent="open()"
            @keydown.space.prevent="open()"
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
              {{ t('dialog.create_project.drop_message') }}
            </p>

            <p class="mt-2 text-xs text-primary/40">
              {{ t('dialog.create_project.support_files') }}
            </p>
          </div>

          <BaseError :error="errors.file" />
        </div>

        <table id="create_project_files_list" class="w-full caption-bottom text-sm">
          <caption class="mt-4 text-sm text-muted-foreground">
            {{ t('dialog.create_project.list_uploaded_file') }}
          </caption>
          <thead>
            <tr class="border-b border-b-border">
              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
                {{ t('dialog.create_project.project_description') }}
              </th>

              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
                {{ t('dialog.create_project.file_size') }}
              </th>

              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
                {{ t('dialog.create_project.file_last_modified') }}
              </th>

              <th />
            </tr>
          </thead>
          <tbody>
            <tr v-for="{ name, size, lastModified } in data.files" :key="name" class="border-b border-b-border">
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
      </form>
    </template>

    <template #footer>
      <div class="flex justify-end gap-x-2">
        <BaseButton variant="secondary" @click="emits('close')">
          {{ t('button.cancel') }}
        </BaseButton>

        <BaseButton id="create_project_create_btn" type="submit" form="create_project_form">
          {{ t('button.create') }}
        </BaseButton>
      </div>
    </template>
  </BaseModal>
</template>
