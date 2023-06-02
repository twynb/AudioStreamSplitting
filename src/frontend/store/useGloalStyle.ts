import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useGlobalStyle = defineStore('global_style', () => {
  const isSidebarMinimized = ref(false)

  return {
    isSidebarMinimized
  }
})
