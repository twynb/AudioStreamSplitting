import { TOAST_DURATION } from '../constants'

export const useToastStore = defineStore('toast', () => {
  const toasts = ref<Toast[]>([])
  const id = ref(0)

  function getToasts() {
    return toasts.value
  }

  function toast(t: Omit<Toast, 'id'>) {
    const newToast: Toast = {
      id: id.value,
      duration: TOAST_DURATION,
      variant: 'default',
      ...t,
    }

    id.value++
    toasts.value.push({ ...newToast })

    setTimeout(() => removeToast(newToast.id), newToast.duration)
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
