import { useLocalStorage } from '@vueuse/core'
import { DEFAULT_SAVE_SETTINGS } from '../includes/constants'

export function useSaveSetings() {
  return useLocalStorage('save-settings', DEFAULT_SAVE_SETTINGS)
}
