import App from './App.vue'
import './main.css'
import { setupAxios } from './includes/setup_axios'
import { installI18n } from '@/modules/i18n'
import { installPinia } from '@/modules/pinia'

setupAxios()
const app = createApp(App)
installI18n(app)
installPinia(app)
app.mount('#app')
