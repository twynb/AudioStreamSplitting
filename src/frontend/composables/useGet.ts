import type { AxiosRequestConfig } from 'axios'

interface GetConfig {
  url: string
  axiosConfig?: AxiosRequestConfig
  onSuccess?: (data: any) => void
}

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
