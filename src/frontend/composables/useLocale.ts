import { useLocalStorage } from '@vueuse/core'
import {
  availableLocales,
  setI18nLanguage,
} from '../modules/i18n'

/**
 * Manage the application's locale and localization settings.
 *
 * @returns An object containing available locales and the current locale.
 *
 * @example
 * ```ts
 * const { currentLocale } = useLocale()
 *
 * currentLocale.value            // en
 * document.documentElement.lang  // en
 *
 * currentLocale.value = 'de'
 * document.documentElement.lang  // de
 * ```
 */
export function useLocale() {
  const currentLocale = useLocalStorage('locale', 'en')
  const { locale } = useI18n()

  watch(currentLocale, () => {
    setI18nLanguage(currentLocale.value)
    locale.value = currentLocale.value
  }, { immediate: true })

  return { availableLocales, currentLocale }
}
