const random = (min: number, max: number) => Math.random() * (max - min) + min
/**
 * Generate a random RGBA color string with 50% opacity.
 *
 * @returns A random RGBA color string in the format "rgba(r, g, b, 0.5)".
 */
export function useRandomColor() {
  return `rgba(${random(0, 255)}, ${random(0, 255)}, ${random(0, 255)}, 0.5)`
}
