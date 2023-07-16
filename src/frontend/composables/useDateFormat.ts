import type { DateLike } from '@vueuse/core'
import { useDateFormat as formatter } from '@vueuse/core'

type PredefinedFormats = 'DD/MM/YYYY'

export function useDateFormat(date: DateLike, format: PredefinedFormats | Omit<string, PredefinedFormats>) {
  return formatter(date, format as string).value
}
