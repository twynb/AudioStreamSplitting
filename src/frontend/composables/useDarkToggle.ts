import { useDark, useToggle } from '@vueuse/core'

export function useDarkToggle() {
  const isDark = useDark()
  const toggle = useToggle(isDark)

  return { isDark, toggle }
}
