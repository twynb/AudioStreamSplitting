/**
 * Converts a duration in seconds to a formatted string representation in minutes and seconds.
 *
 * @param secs The duration in seconds to convert.
 * @param format The format to be converted.
 * @returns A formatted string representing the duration in minutes and seconds.
 *
 * @example
 * ```ts
 * useConvertSecToMin(135, 'Mm:Ss') // 2m 15s
 * useConvertSecToMin(135, 'mm:ss') // 02:15
 *
 * useConvertSecToMin(120, 'Mm:Ss') // 2m
 * useConvertSecToMin(120, 'mm:ss') // 02:00
 *
 * ```
 */
export function useConvertSecToMin(secs: number, format: 'Mm:Ss' | 'mm:ss') {
  const total = Math.floor(secs)
  const seconds = total % 60
  const minutes = (total - seconds) / 60
  const ret = (function () {
    switch (format) {
      case 'mm:ss':
        return seconds ? `${minutes}m ${seconds}s` : `${minutes}m`
      case 'Mm:Ss':
        return `${minutes >= 10 ? minutes : `0${minutes}`}:${seconds >= 10 ? seconds : `0${seconds}`}`
    }
  })()

  return ret
}
