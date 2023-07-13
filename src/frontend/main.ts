import { createApp } from 'vue'
import type { App as AppType } from 'vue'
import App from './App.vue'

import './main.css'
import '@unocss/reset/tailwind.css'
import 'uno.css'

const app = createApp(App)
Object.values(import.meta.glob<{ install: (app: AppType) => void }>('./modules/*.ts', { eager: true }))
  .forEach((module) => {
    module.install(app)
  })

app.mount('#app')
