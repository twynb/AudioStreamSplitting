import { driver as createDriver } from 'driver.js'

export const useDriverStore = defineStore('driver', () => {
  const driver = shallowRef(createDriver())
  return { driver }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useDriverStore, import.meta.hot))
