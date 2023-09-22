import { useDark, useToggle } from '@vueuse/core'

/**
 * Toggles between light and dark modes.
 *
 * @returns An object with `isDark` (current mode) and `toggle` (toggle function).
 */
export function useDarkToggle() {
  const isDark = useDark()
  const toggle = useToggle(isDark)

  return { isDark, toggle }
}
