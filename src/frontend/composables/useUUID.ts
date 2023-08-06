// https://github.com/vueuse/vueuse/issues/465#issuecomment-1163264282

export function useUUID() {
  const _pattern = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'

  // Replace each character in the pattern
  // leaving any non x|y character alone.
  return _pattern.replace(/[xy]/g, replacePattern)
}

function replacePattern(c: string) {
  // Random hexadecimal number
  const r = (Math.random() * 16) | 0

  // If 'x' return hexadecimal number,
  // if 'y' return [8-11] randomly
  const v = c === 'x' ? r : (r & 0x3) | 0x8
  return v.toString(16)
}
