import { createApp } from 'vue'
import App from './App.vue'
import './main.css'
import { setupAxios } from './includes/setup_axios'

setupAxios()
createApp(App).mount('#app')
