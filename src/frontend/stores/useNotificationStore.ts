import { NOTIFICATION_DURAION } from '../constants'

export const useNotificationStore = defineStore('notification', () => {
  const notifications = ref<AppNotification[]>([])

  function getNotifications() {
    return notifications.value
  }

  function createNotification(n: Omit<AppNotification, 'id' | 'timeoutId'>) {
    const id = useUUID()
    notifications.value.unshift({ id, ...n })

    setTimeout(() => removeNotification(id), NOTIFICATION_DURAION)
  }

  function removeNotification(id: string) {
    notifications.value = notifications.value.filter(n => n.id !== id)
  }

  return {
    getNotifications,
    createNotification,
    removeNotification,
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useNotificationStore, import.meta.hot))
