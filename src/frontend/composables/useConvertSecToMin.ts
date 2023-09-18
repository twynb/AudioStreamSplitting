export function useConvertSecToMin(secs: number) {
  const rest = Math.round((secs % 60))
  const min = Math.round((secs - rest) / 60)
  return rest ? `${min}m ${rest}s` : `${min}m`
}
