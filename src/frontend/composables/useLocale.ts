import { useLocalStorage } from '@vueuse/core'
import {
  availableLocales,
  loadLanguageAsync,
} from '../modules/i18n'

export function useLocale() {
  const { locale } = useI18n()
  if (!locale.value)
    locale.value = 'en'

  const currentLocal = useLocalStorage('locale', locale.value)

  const toggleLocales = async (l: string) => {
    await loadLanguageAsync(l)
    locale.value = l
    currentLocal.value = l
  }

  watch(currentLocal, async () => {
    await toggleLocales(currentLocal.value)
  })

  return { toggleLocales, availableLocales, currentLocal }
}
