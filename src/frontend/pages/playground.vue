<script setup lang="ts">
const audio = ref<HTMLAudioElement>()
const recorder = shallowRef<MediaRecorder>()
const chunks = shallowRef<Blob[]>([])

async function handleRecord() {
  if (!navigator.mediaDevices.getUserMedia)
    return

  const handleStream = (stream: MediaStream) => {
    recorder.value = new MediaRecorder(stream)
    recorder.value.start()

    recorder.value.ondataavailable = (e: BlobEvent) => {
      if (e.data.size === 0)
        return

      chunks.value.push(e.data)
    }

    recorder.value.onstop = () => {
      const blob = new Blob(chunks.value, { type: 'audio/wav' })
      chunks.value = []
      recorder.value = undefined

      const url = URL.createObjectURL(blob)
      if (!audio.value)
        return
      audio.value.src = url
    }
  }

  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(handleStream)
    .catch((e) => { console.log(e) })
}

function handleStop() {
  recorder.value?.stop()
}
</script>

<template>
  <ContentLayout header="Playground (dev only)">
    <div class="border border-border rounded-sm bg-background p-6 space-x-10 focus:outline-none">
      <audio ref="audio" controls>
        <source src="" type="audio/wav">
      </audio>

      <BaseButton @click="handleRecord">
        Record
      </BaseButton>

      <BaseButton @click="handleStop">
        Stop
      </BaseButton>
    </div>
  </ContentLayout>
</template>
