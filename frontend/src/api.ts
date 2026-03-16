import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000',
  withCredentials: true,
})

export const GRAVATAR_BASE_URL =
  import.meta.env.VITE_GRAVATAR_BASE_URL || 'https://www.gravatar.com/avatar/'
