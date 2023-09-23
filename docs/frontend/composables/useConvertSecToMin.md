# useConvertSecToMin
Converts a duration in seconds to a formatted string representation in minutes and seconds.
## Parameters
| Name | Description |
|------|-------------|
|secs|The duration in seconds to convert.|
## Returns
A formatted string representing the duration in minutes and seconds.
```
(secs: number) => string
```
## Examples
```ts
useConvertSecToMin(135) // 2m 15s

useConvertSecToMin(120) // 2m

```