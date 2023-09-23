# useDocTitle
Set the document's title with an optional prefix.
## Parameters
| Name | Description |
|------|-------------|
|title|The title to set.|
|prefix|An optional prefix to prepend to the title.|
## Returns

```
(title: string, prefix?: string) => void
```
## Examples
```ts
useDocTitle('New Title')
document.title // DefaultPrefix New Title

useDocTitle('New Title', 'MyPrefix')
document.title // MyPrefix New Title
```