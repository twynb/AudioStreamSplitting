import type { App } from 'vue'
import type { Locale } from 'vue-i18n'
import { createI18n } from 'vue-i18n'

import en from '../locales/en.json'
import de from '../locales/de.json'
import fr from '../locales/fr.json'
import es from '../locales/es.json'

const messages = { en, de, fr, es }

const i18n = createI18n({
  legacy: false,
  locale: '',
  messages,
})

export const availableLocales = Object.keys(messages)

export function setI18nLanguage(lang: Locale) {
  i18n.global.locale.value = lang as any
  if (typeof document !== 'undefined')
    document.querySelector('html')?.setAttribute('lang', lang)
  return lang
}

export function install(app: App) {
  app.use(i18n)
  setI18nLanguage('en')
}
