import { useLocalStorage } from '@vueuse/core'
import {
  availableLocales,
  setI18nLanguage,
} from '../modules/i18n'

export function useLocale() {
  const { locale } = useI18n()
  if (!locale.value)
    locale.value = 'en'

  const currentLocal = useLocalStorage('locale', locale.value)

  if (currentLocal.value !== locale.value)
    currentLocal.value = locale.value

  watch(currentLocal, () => {
    setI18nLanguage(currentLocal.value)
    locale.value = currentLocal.value
  })

  return { availableLocales, currentLocal }
}
