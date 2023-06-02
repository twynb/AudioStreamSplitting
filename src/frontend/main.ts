import { createI18n } from 'vue-i18n'
import App from './App.vue'
import './main.css'
import { setupAxios } from './includes/setup_axios'

setupAxios()

const app = createApp(App)

app.use(createPinia())
app.use(
  createI18n({
    legacy: false,
    locale: '',
    messages: {}
  })
)
app.mount('#app')
