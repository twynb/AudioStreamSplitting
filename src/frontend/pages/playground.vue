<script setup lang="ts">
const audioSrc = ref('')
const recorder = shallowRef<MediaRecorder>()
const { canvas, drawWave } = useDrawWave()
const isRecording = ref(false)

function handleRecord() {
  if (!navigator.mediaDevices.getUserMedia)
    return

  isRecording.value = true

  const handleStream = (stream: MediaStream) => {
    drawWave(stream)

    const chunks: Blob[] = []
    recorder.value = new MediaRecorder(stream)
    recorder.value.start()

    recorder.value.ondataavailable = (e: BlobEvent) => {
      if (e.data.size === 0)
        return

      chunks.push(e.data)
    }

    recorder.value.onstop = () => {
      const blob = new Blob(chunks, { type: 'audio/wav' })
      recorder.value = undefined

      const url = URL.createObjectURL(blob)
      audioSrc.value = url
    }
  }

  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(handleStream)
    .catch((e) => { console.log(e) })
}

function handleStop() {
  recorder.value?.stop()
  canvas.value = undefined
  isRecording.value = false
}
</script>

<template>
  <ContentLayout header="Playground (dev only)">
    <div class="border border-border rounded-sm bg-background p-6 focus:outline-none">
      <audio v-if="audioSrc" controls>
        <source :src="audioSrc" type="audio/wav">
      </audio>

      <div class="space-x-10">
        <BaseButton @click="handleRecord">
          Record
        </BaseButton>

        <BaseButton @click="handleStop">
          Stop
        </BaseButton>
      </div>

      <canvas v-if="isRecording" ref="canvas" class="h-100px w-full" />

      <br><br>
      <BaseSlider />
    </div>
  </ContentLayout>
</template>
