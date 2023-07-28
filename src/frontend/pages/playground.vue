<script setup lang="ts">
const { isDark } = useDarkToggle()
const audio = ref<HTMLAudioElement>()
const recorder = shallowRef<MediaRecorder>()
const chunks = shallowRef<Blob[]>([])
const canvas = shallowRef<HTMLCanvasElement>()
const isRecording = ref(false)

async function handleRecord() {
  if (!navigator.mediaDevices.getUserMedia)
    return

  isRecording.value = true

  const handleStream = (stream: MediaStream) => {
    const audioContext = new window.AudioContext()
    const canvasContext = canvas.value?.getContext('2d')
    if (!canvasContext)
      return
    const analyser = audioContext.createAnalyser()
    analyser.fftSize = 2048
    const mediaStreamSource = audioContext.createMediaStreamSource(stream)
    mediaStreamSource.connect(analyser)

    const bufferLength = analyser.frequencyBinCount
    const dataArray = new Uint8Array(bufferLength)

    const drawWaveform = () => {
      if (!canvas.value)
        return
      analyser.getByteTimeDomainData(dataArray)
      canvasContext.clearRect(0, 0, canvas.value.width, canvas.value.height)

      canvasContext.lineWidth = 2
      canvasContext.strokeStyle = isDark.value ? 'hsl(210,40%,98%)' : 'hsl(222.2,47.4%,11.2%)'
      canvasContext.beginPath()

      const sliceWidth = canvas.value.width * 1.0 / bufferLength
      let x = 0

      for (let i = 0; i < bufferLength; i++) {
        const v = dataArray[i] / 128.0
        const y = v * canvas.value.height / 2

        if (i === 0)
          canvasContext.moveTo(x, y)

        else
          canvasContext.lineTo(x, y)

        x += sliceWidth
      }

      canvasContext.lineTo(canvas.value.width, canvas.value.height / 2)
      canvasContext.stroke()

      requestAnimationFrame(drawWaveform)
    }

    drawWaveform()

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
  canvas.value = undefined
  isRecording.value = false
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

      <canvas v-if="isRecording" ref="canvas" class="w-full" height="200" />
    </div>
  </ContentLayout>
</template>
