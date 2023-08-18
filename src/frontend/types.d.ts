interface Document {
  startViewTransition: (fn: () => void) => void
}

interface Project {
  id: string
  name: string
  description: string
  path: string,
  visited?: boolean
  files: {
    name: string,
    fileType: string,
    fileName: string,
    filePath: string,
    peaks?: number[][]
    info: {
      duration: number,
      numChannels: number,
      numSamples: number,
      sampleRate: number
    }
  }[]
  createAt: string
}

type ProcessAudioFile = Pick<Project['files'][0], 'filePath' | 'info'>

type TemplateRef = Element | ComponentPublicInstance | null

interface Toast {
  id: number
  title?: string
  content: string
  variant?: 'default' | 'destructive'
  duration?: number
}
