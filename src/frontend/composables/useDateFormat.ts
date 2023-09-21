import type { DateLike } from '@vueuse/core'
import { useDateFormat as formatter } from '@vueuse/core'

type PredefinedFormats = 'DD/MM/YYYY'

/**
 * Format a date-like object into a predefined or custom format.
 *
 * @param date - The date-like object to format.
 * @param format - The date format, either a predefined format ('DD/MM/YYYY')
 *                or a custom format string.
 *
 * @returns The formatted date as a string.
 */
export function useDateFormat(date: DateLike, format: PredefinedFormats | Omit<string, PredefinedFormats>) {
  return formatter(date, format as string).value
}
