/**
 * Converts a duration in seconds to a formatted string representation in minutes and seconds.
 *
 * @param secs - The duration in seconds to convert.
 * @returns A formatted string representing the duration in minutes and seconds,
 */
export function useConvertSecToMin(secs: number) {
  const _secs = Math.floor(secs)
  const rest = _secs % 60
  const min = (_secs - rest) / 60
  return rest ? `${min}m ${rest}s` : `${min}m`
}
