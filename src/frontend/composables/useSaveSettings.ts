import { useLocalStorage } from '@vueuse/core'
import { DEFAULT_SAVE_SETTINGS } from '../includes/constants'

/**
 * Provides a reactive object that wraps save settings. Any changes made to this object will be immediately reflected in the `save-settings` key of the localStorage.
 *
 * @returns A reactive object representing audio identification settings.
 *
 * @example
 * ```ts
 * const saveSettings = useSaveSetings();
 *
 * // Updating the fileType in audio identification settings
 * saveSettings.value.fileType = 'wav';
 * ```
 */
export function useSaveSetings() {
  return useLocalStorage('save-settings', DEFAULT_SAVE_SETTINGS)
}
