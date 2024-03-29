// https://gist.github.com/jlevy/c246006675becc446360a798e2b2d781
/**
 * Generate a hash value for a given string.
 *
 * @param str The input string to hash.
 * @returns A hashed representation of the input string.
 *
 * @example
 * ```ts
 * useHash('somerandomstring') // 19viky0
 * ```
 */
export function useHash(str: string) {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i)
    hash = (hash << 5) - hash + char
    hash &= hash // Convert to 32bit integer
  }
  return new Uint32Array([hash])[0].toString(36)
}
