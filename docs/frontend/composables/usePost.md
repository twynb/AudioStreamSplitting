# usePost
Execute a POST request and manage the response data, loading state, and errors.
## Parameters
| Name | Description |
|------|-------------|
|config|The configuration for the POST request.|
## Returns
An object containing the response data, loading state, error message, and an execution function.
```
<T>(config: PostConfig<T>) => { data: any; isFetching: any; error: any; execute: (body?: unknown) => void; }
```
## Examples
```ts
const { data, isFetching, error, execute } = useGet({
   url: '/api/example',
   body: { filePath: '/tmp/some.mp3' },
   onSuccess(data){
     //
    }
})
```