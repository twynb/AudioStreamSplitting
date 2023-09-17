import type { AxiosRequestConfig } from 'axios'

interface GetConfig {
  url: string
  axiosConfig?: AxiosRequestConfig
  onSuccess?: (data: any) => void
}

/**
 * Execute a GET request and manage the response data, loading state, and errors.
 *
 * @param config - The configuration for the GET request.
 * @returns An object containing the response data, loading state, error message, and an execution function.
 */
export function useGet(config: GetConfig) {
  const data = ref<unknown>()
  const isFetching = ref(false)
  const error = ref('')

  const execute = () => {
    isFetching.value = true
    axios.get(config.url, config.axiosConfig).then((res) => {
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
