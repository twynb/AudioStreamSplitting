import {
  availableLocales,
  loadLanguageAsync,
} from '../modules/i18n'

export function useLocale() {
  const { locale } = useI18n()

  const toggleLocales = async (l: string) => {
    await loadLanguageAsync(l)
    locale.value = l
  }

  return { toggleLocales, availableLocales }
}
