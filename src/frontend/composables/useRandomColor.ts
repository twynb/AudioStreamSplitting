const random = (min: number, max: number) => Math.random() * (max - min) + min
export function useRandomColor() {
  return `rgba(${random(0, 255)}, ${random(0, 255)}, ${random(0, 255)}, 0.5)`
}
