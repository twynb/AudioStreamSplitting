# useEnv
Provides a reactive object that wraps all environment variables needed for audio identification in the backend. Any changes made to this object will be immediately reflected in the `env` key of the localStorage.
## Returns
A reactive object representing the environment variables.
```
() => RemovableRef<{ SERVICE_ACOUSTID_API_KEY: any; SERVICE_ACOUSTID_USER_KEY: any; SERVICE_SHAZAM_API_KEY: any; }>
```
## Examples
```ts
const env = useEnv();

// Updating the SERVICE_API_KEY environment variable
env.SERVICE_API_KEY = 'somekey';
```