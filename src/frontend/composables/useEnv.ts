import { useLocalStorage } from '@vueuse/core'
import { DEFAULT_ENV } from '../includes/constants'

/**
 * Provides a reactive object that wraps all environment variables needed for audio identification in the backend. Any changes made to this object will be immediately reflected in the `env` key of the localStorage.
 *
 * @returns A reactive object representing the environment variables.
 *
 * @example
 * ```ts
 * const env = useEnv();
 *
 * // Updating the SERVICE_API_KEY environment variable
 * env.SERVICE_API_KEY = 'somekey';
 * ```
 */
export function useEnv() {
  return useLocalStorage('env', DEFAULT_ENV)
}
