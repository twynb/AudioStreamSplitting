import type { AxiosRequestConfig } from 'axios'

interface PostConfig<T> {
  url: string
  body?: unknown
  axiosConfig?: AxiosRequestConfig
  onSuccess?: (data: T) => void
}

/**
 * Execute a POST request and manage the response data, loading state, and errors.
 *
 * @param config - The configuration for the POST request.
 * @returns An object containing the response data, loading state, error message, and an execution function.
 */
export function usePost<T>(config: PostConfig<T>) {
  const data = ref<T>()
  const isFetching = ref(false)
  const error = ref('')

  const execute = (body?: unknown) => {
    isFetching.value = true
    axios.post(config.url, config.body ?? body, config.axiosConfig).then((res) => {
      data.value = res.data
      config.onSuccess && data.value && config.onSuccess(data.value)
    }).catch((e) => {
      error.value = e
    }).finally(() => {
      isFetching.value = false
    })
  }

  return { data, isFetching, error, execute }
}
