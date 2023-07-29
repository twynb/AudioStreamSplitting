<script setup lang="ts">
const audioRef = ref<HTMLAudioElement>()
const { drawWave, WaveCanvas } = useDrawWave()
const isRecording = ref(false)
const recorder = shallowRef<MediaRecorder>()

async function handleRecord() {
  if (!navigator.mediaDevices.getUserMedia)
    return

  isRecording.value = true

  let stream: MediaStream
  try {
    stream = await navigator.mediaDevices.getUserMedia({ audio: true })
  }
  catch (err) {
    throw new Error(`Error accessing the microphone: ${(err as Error).message}`)
  }

  drawWave(stream)

  const chunks: Blob[] = []
  recorder.value = new MediaRecorder(stream)

  recorder.value.ondataavailable = (e) => {
    e.data.size > 0 && chunks.push(e.data)
  }

  recorder.value.onstop = () => {
    const blob = new Blob(chunks, { type: 'audio/wav' })
    const url = URL.createObjectURL(blob)
    if (!audioRef.value)
      return
    audioRef.value.src = url
    audioRef.value.load()

    // URL.revokeObjectURL(url)
  }
  recorder.value.start()
}

function handleStop() {
  recorder.value?.stop()
  isRecording.value = false
}

async function handlePlay() {
  if (!audioRef.value)
    return

  console.log(audioRef.value.duration)
}
</script>

<template>
  <ContentLayout header="Playground (dev only)">
    <div class="border border-border rounded-sm bg-background p-6 focus:outline-none">
      <!-- <audio ref="audioRef" class="invisible h-0" controls> -->
      <audio ref="audioRef" src="" class="" controls />

      <div class="space-x-10">
        <BaseButton @click="handleRecord">
          Record
        </BaseButton>

        <BaseButton @click="handleStop">
          Stop
        </BaseButton>
      </div>

      <br><br>

      <BaseButton @click="handlePlay">
        Play
      </BaseButton>

      <BaseSlider />

      <br><br>
      <WaveCanvas v-if="isRecording" class="h-100px w-full" />
    </div>
  </ContentLayout>
</template>
