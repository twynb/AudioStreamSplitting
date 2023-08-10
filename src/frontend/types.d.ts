interface Document{
  startViewTransition: (fn:()=> void) => void
}

interface ProjectFile{
  name:string
  format:string
  duration: number
  size: number
  numChannels: number
  numSamples:number
}

interface ProjectResponse{
  name: string
  description: string
  files: ProjectFile[]
}

interface Project extends ProjectResponse{
  id: string
  expectedCount: number
  foundCount: number
  createAt: string
}

type TemplateRef = Element | ComponentPublicInstance | null

interface Toast{
  id: number
  title?: string
  content: string
  variant?: 'default' | 'destructive'
  duration?: number
}
