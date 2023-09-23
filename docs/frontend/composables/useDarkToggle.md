# useDarkToggle
Toggles between light and dark modes.
## Returns
An object with `isDark` (current mode) and `toggle` (toggle function).
```
() => { isDark: WritableComputedRef<boolean>; toggle: (value?: boolean) => boolean; }
```
## Examples
```ts
const {isDark, toggle} = useDark()

isDark.value // false
toggle()
isDark.value // true

```