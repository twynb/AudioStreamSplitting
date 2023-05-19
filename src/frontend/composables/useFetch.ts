import { createFetch } from '@vueuse/core'

export const useFetch = createFetch({
  baseUrl: 'http://localhost:5000/api',
})
