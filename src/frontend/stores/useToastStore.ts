import { TOAST_DURATION } from '../constants'

export const useToastStore = defineStore('toast', () => {
  const toasts = ref<Toast[]>([])
  const id = ref(0)

  function getToasts() {
    return toasts.value
  }

  function toast(n: Omit<Toast, 'id'>) {
    const toastId = id.value
    id.value++
    toasts.value.push({ id: toastId, ...n })

    setTimeout(() => removeToast(toastId), TOAST_DURATION)
  }

  function removeToast(id: number) {
    toasts.value = toasts.value.filter(n => n.id !== id)
  }

  return {
    getToasts,
    toast,
    removeToast,
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useToastStore, import.meta.hot))
