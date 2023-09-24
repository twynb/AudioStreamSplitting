import { useLocalStorage } from '@vueuse/core'
import { DEFAULT_ENV } from '../includes/constants'

export function useEnv() {
  return useLocalStorage('env', DEFAULT_ENV)
}
