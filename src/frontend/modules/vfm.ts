import { createVfm } from 'vue-final-modal'
import type { App } from 'vue'

export function install(app: App) {
  const vfm = createVfm()
  app.use(vfm)
}
