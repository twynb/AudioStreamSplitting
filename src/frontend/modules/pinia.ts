import type { App } from 'vue'

export const installPinia = (app: App) => {
  const pinia = createPinia()
  app.use(pinia)
}
