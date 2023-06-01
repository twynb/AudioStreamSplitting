import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import './main.css'
import { setupAxios } from './includes/setup_axios'

setupAxios()

const app = createApp(App)
app.use(createPinia())

app.mount('#app')
