<script setup lang="ts">
const files = defineModel<File[]>({ default: [] })

function onFileChanged(event: Event) {
  const result: File[] = []

  const { files: _files } = event.target as HTMLInputElement
  if (!_files)
    return

  for (let i = 0; i < _files.length; i++) {
    const file = _files.item(i)
    file && result.push(file)
  }

  files.value = result
}
</script>

<template>
  <input
    class="h-10 w-full flex border border-input rounded-md bg-background px-3 py-2 text-sm ring-offset-background disabled:cursor-not-allowed file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-primary placeholder:text-muted-foreground disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-ring" type="file" multiple accept="audio/mp3" @change="onFileChanged"
  >
</template>
