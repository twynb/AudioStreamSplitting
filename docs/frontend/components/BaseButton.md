# BaseButton

| Name     | Description                      | Type                                                                 | Default   |
| -------- | -------------------------------- | -------------------------------------------------------------------- | --------- |
| variant  | Variant for the button           | "primary", "secondary", "destructive", "outline", "ghost" (optional) | 'primary' |
| iconOnly | Content is only icon             | boolean (optional)                                                   | false     |
| to       | Target if button works as a link | string (optional)                                                    |           |

## Slots

| Name    | Description      | Bindings |
| ------- | ---------------- | -------- |
| default | Slot for content |          |

---

## Examples

```vue
<BaseButton variant="primary">Button</BaseButton>

<BaseButton variant="ghost" icon-only>x</BaseButton>
```
