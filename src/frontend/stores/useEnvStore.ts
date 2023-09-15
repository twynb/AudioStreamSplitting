import { useLocalStorage } from '@vueuse/core'

export const useEnvStore = defineStore('env', () => {
  const defaultEnv = shallowRef({
    SERVICE_ACOUSTID_API_KEY: import.meta.env.VITE_SERVICE_ACOUSTID_API_KEY,
    SERVICE_SHAZAM_API_KEY: import.meta.env.VITE_SERVICE_SHAZAM_API_KEY,
    OUTPUT_FILE_NAME_TEMPLATE: import.meta.env.VITE_OUTPUT_FILE_NAME_TEMPLATE,
    SAVE_DIRECTORY: import.meta.env.VITE_SAVE_DIRECTORY,
  })

  const lsEnv = useLocalStorage('env', defaultEnv)

  return { defaultEnv, lsEnv }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useEnvStore, import.meta.hot))
