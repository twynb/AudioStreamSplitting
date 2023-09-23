import { useDark, useToggle } from '@vueuse/core'

/**
 * Toggles between light and dark modes.
 *
 * @returns An object with `isDark` (current mode) and `toggle` (toggle function).
 *
 * @example
 * ```ts
 * const {isDark, toggle} = useDark()
 *
 * isDark.value // false
 * toggle()
 * isDark.value // true
 *
 * ```
 */
export function useDarkToggle() {
  const isDark = useDark()
  const toggle = useToggle(isDark)

  return { isDark, toggle }
}
