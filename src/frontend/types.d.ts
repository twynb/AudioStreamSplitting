interface Document {
  startViewTransition: (fn: () => void) => void
}

interface Project {
  id: string
  name: string
  description: string
  path:string,
  files: {
    fileName: string,
    filePath: string,
  }[]
  createAt: string
}

type TemplateRef = Element | ComponentPublicInstance | null

interface Toast {
  id: number
  title?: string
  content: string
  variant?: 'default' | 'destructive'
  duration?: number
}
