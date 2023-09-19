import { createApp } from 'vue'
import type { App as AppType } from 'vue'
import axios from 'axios'
import App from './App.vue'

import './main.css'
import '@unocss/reset/tailwind.css'
import 'uno.css'
import 'driver.js/dist/driver.css'

axios.defaults.baseURL = 'http://localhost:55555/api'

const app = createApp(App)
Object.values(
  import.meta.glob<{ install: (app: AppType) => void }>('./modules/*.ts', { eager: true }),
).forEach(({ install }) => install(app))

app.mount('#app')
