import axios from 'axios'
import { ElMessage } from 'element-plus'
import { authState, clearAuth } from './state/auth'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000',
  withCredentials: true,
})

api.interceptors.request.use((config) => {
  if (authState.token) {
    config.headers.Authorization = `Bearer ${authState.token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const status = error?.response?.status
    if (status === 401) {
      clearAuth()
      ElMessage.error('登录状态已失效，请重新登录')
    } else if (error?.response?.data?.detail) {
      ElMessage.error(String(error.response.data.detail))
    } else {
      ElMessage.error('请求失败，请稍后重试')
    }
    return Promise.reject(error)
  },
)

export const GRAVATAR_BASE_URL =
  import.meta.env.VITE_GRAVATAR_BASE_URL || 'https://www.gravatar.com/avatar/'
