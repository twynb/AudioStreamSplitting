export function useConvertSecToMin(secs: number) {
  const rest = (secs % 60)
  const min = (secs - rest) / 60
  return rest ? `${min}m ${rest}s` : `${min}m`
}
