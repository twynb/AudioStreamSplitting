import { useLocalStorage } from '@vueuse/core'

export const useGlobalStyle = defineStore('global_style', () => {
  const isSidebarMinimized = useLocalStorage('is_sidebar_minimized', false)

  return {
    isSidebarMinimized,
  }
})
