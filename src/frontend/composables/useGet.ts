export function useGet(url: string) {
  const data = ref()
  const isFetching = ref(false)
  const error = ref('')

  const execute = () => {
    isFetching.value = true
    axios.get(url).then((res) => {
      data.value = res.data
    }).catch((e) => {
      error.value = e
    }).finally(() => {
      isFetching.value = false
    })
  }

  return { data, isFetching, error, execute }
}
