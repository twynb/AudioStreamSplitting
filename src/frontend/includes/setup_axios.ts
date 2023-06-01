import axios from 'axios'

export function setupAxios() {
  axios.defaults.baseURL = 'http://localhost:5000/api'
}
