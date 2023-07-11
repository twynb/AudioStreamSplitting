import { useLocalStorage } from '@vueuse/core'
import {
  availableLocales,
  loadLanguageAsync,
} from '../modules/i18n'

export function useLocale() {
  const { locale } = useI18n()

  const currentLocal = useLocalStorage('locale', locale.value)

  const toggleLocales = async (l: string) => {
    await loadLanguageAsync(l)
    locale.value = l
    currentLocal.value = l
  }

  return { toggleLocales, availableLocales, currentLocal }
}
