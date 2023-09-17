export function useConvertSecToMin(secs: number) {
  const rest = Math.round(secs % 60)
  const min = Math.floor(secs / 60)
  return rest ? `${min}m ${rest}s` : `${min}m`
}
