# useDateFormat
Format a date-like object into a predefined or custom format.
## Parameters
| Name | Description |
|------|-------------|
|date|The date-like object to format.|
|format|The date format, either a predefined format ('DD/MM/YYYY') or a custom format string.|
## Returns
The formatted date as a string.
```
(date: DateLike, format: "DD/MM/YYYY" | Omit<string, "DD/MM/YYYY">) => string
```
## Examples
```ts
useDateFormat(new Date(), 'DD/MM/YYYY') // 22/09/2023

useDateFormat(new Date(), 'dddd DD/MM') // Friday 22/09
```