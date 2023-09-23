# useDriver
Provides access to the Driver.js instance and configuration for guided tours.
## Returns
An object containing the Driver.js instance and a function to set its configuration.
```
() => { driver: any; setConfig: (config: Omit<Config, "stagePadding" | "stageRadius">) => void; }
```
## Examples
```ts
const {driver, setConfig} = useDriver()

setConfig({})
driver.value.doSomething()
```