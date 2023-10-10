interface Document {
  startViewTransition: (fn: () => void) => void
}

interface Window {
  showSaveFilePicker: (config?: any) => any
}

type TemplateRef = Element | ComponentPublicInstance | null

interface Toast {
  id: number
  title?: string
  content: string
  variant?: 'default' | 'destructive'
  duration?: number
}
