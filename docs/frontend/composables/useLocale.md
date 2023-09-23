# useLocale
Manage the application's locale and localization settings.
## Returns
An object containing available locales and the current locale.
```
() => { availableLocales: string[]; currentLocale: RemovableRef<string>; }
```
## Examples
```ts
const { currentLocale } = useLocale()

currentLocale.value            // en
document.documentElement.lang  // en

currentLocale.value = 'de'
document.documentElement.lang  // de
```