# BaseSelect

| Name        | Description                 | Type              | Default |
| ----------- | --------------------------- | ----------------- | ------- |
| placeholder | Placeholder for select      | string (optional) |         |
| options     | Array of options for select | Option            |         |

## Slots

| Name  | Description      | Bindings |
| ----- | ---------------- | -------- |
| label | Label for option |          |

---

## Examples

```vue
<BaseSelect :options=[{label: "English",value: "en"}]>
  <template #label>
    Custom Label
  </template>
</BaseSelect>
```
