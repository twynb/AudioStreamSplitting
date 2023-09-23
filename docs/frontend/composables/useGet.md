# useGet
Execute a GET request and manage the response data, loading state, and errors.
## Parameters
| Name | Description |
|------|-------------|
|config|The configuration for the GET request.|
## Returns
An object containing the response data, loading state, error message, and an execution function.
```
(config: GetConfig) => { data: any; isFetching: any; error: any; execute: () => void; }
```
## Examples
```ts
const { data, isFetching, error, execute } = useGet({
   url: '/api/example',
   onSuccess(data){
     //
   }
})
```