import { createApp } from 'vue'
import App from './App.vue'
import './main.css'
import { setupAxios } from './includes/setup_axios'

setupAxios()

const app = createApp(App)

app.mount('#app')
