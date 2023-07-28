export function useDrawWave() {
  const canvas = ref<HTMLCanvasElement>()

  const { isDark } = useDarkToggle()
  const drawWave = (stream: MediaStream) => {
    if (!canvas.value)
      return

    const audioContext = new window.AudioContext()
    const canvasContext = canvas.value?.getContext('2d')
    if (!canvasContext)
      return
    const analyser = audioContext.createAnalyser()
    analyser.fftSize = 1024
    const mediaStreamSource = audioContext.createMediaStreamSource(stream)
    mediaStreamSource.connect(analyser)

    const bufferLength = analyser.frequencyBinCount
    const dataArray = new Uint8Array(bufferLength)

    const draw = () => {
      if (!canvas.value)
        return
      analyser.getByteTimeDomainData(dataArray)
      canvasContext.clearRect(0, 0, canvas.value.width, canvas.value.height)

      canvasContext.lineWidth = 2
      canvasContext.strokeStyle = isDark.value ? 'hsl(210,40%,98%)' : 'hsl(222.2,47.4%,11.2%)'
      canvasContext.beginPath()

      const sliceWidth = canvas.value.width / bufferLength
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

      requestAnimationFrame(draw)
    }

    draw()
  }

  return { canvas, drawWave }
}
