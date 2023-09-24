# useSaveSetings
Provides a reactive object that wraps save settings. Any changes made to this object will be immediately reflected in the `save-settings` key of the localStorage.
## Returns
A reactive object representing audio identification settings.
```
() => RemovableRef<{ fileType: string; shouldAsk: boolean; submitSavedFiles: boolean; saveDirectory: string; nameTemplate: string; }>
```
## Examples
```ts
const saveSettings = useSaveSetings();

// Updating the fileType in audio identification settings
saveSettings.value.fileType = 'wav';
```