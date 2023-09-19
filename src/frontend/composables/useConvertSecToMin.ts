export function useConvertSecToMin(secs: number) {
  const _secs = Math.floor(secs)
  const rest = _secs % 60
  const min = (_secs - rest) / 60
  return rest ? `${min}m ${rest}s` : `${min}m`
}
