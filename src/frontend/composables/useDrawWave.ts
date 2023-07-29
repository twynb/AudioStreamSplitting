export function useDrawWave() {
  const canvasRef = ref<HTMLCanvasElement>()

  const { isDark } = useDarkToggle()

  const WaveCanvas = defineComponent({
    render() {
      return h('canvas', { ref: canvasRef })
    },
  })

  const drawWave = (stream: MediaStream) => {
    if (!canvasRef.value)
      return

    const audioContext = new window.AudioContext()
    const canvasContext = canvasRef.value?.getContext('2d')
    if (!canvasContext)
      return
    const analyser = audioContext.createAnalyser()
    analyser.fftSize = 1024
    const mediaStreamSource = audioContext.createMediaStreamSource(stream)
    mediaStreamSource.connect(analyser)

    const bufferLength = analyser.frequencyBinCount
    const dataArray = new Uint8Array(bufferLength)

    const draw = () => {
      if (!canvasRef.value)
        return
      analyser.getByteTimeDomainData(dataArray)
      canvasContext.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height)

      canvasContext.lineWidth = 2
      canvasContext.strokeStyle = isDark.value ? 'hsl(210,40%,98%)' : 'hsl(222.2,47.4%,11.2%)'
      canvasContext.beginPath()

      const sliceWidth = canvasRef.value.width / bufferLength
      let x = 0

      for (let i = 0; i < bufferLength; i++) {
        const v = dataArray[i] / 128.0
        const y = v * canvasRef.value.height / 2

        if (i === 0)
          canvasContext.moveTo(x, y)

        else
          canvasContext.lineTo(x, y)

        x += sliceWidth
      }

      canvasContext.lineTo(canvasRef.value.width, canvasRef.value.height / 2)
      canvasContext.stroke()

      requestAnimationFrame(draw)
    }

    draw()
  }

  return { canvasRef, drawWave, WaveCanvas }
}
