import { defineStore } from 'pinia'

import api from '@/api/client'
import type { AuthResponse, UserSummary } from '@/types'

interface AuthState {
  token: string
  user: UserSummary | null
  initialized: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('memeclub_token') ?? '',
    user: null,
    initialized: false
  }),
  getters: {
    isLoggedIn: (state) => Boolean(state.user)
  },
  actions: {
    setAuth(payload: AuthResponse) {
      this.token = payload.access_token
      this.user = payload.user
      localStorage.setItem('memeclub_token', payload.access_token)
    },
    clearAuth() {
      this.token = ''
      this.user = null
      localStorage.removeItem('memeclub_token')
    },
    async bootstrap() {
      if (this.initialized) {
        return
      }
      try {
        const { data } = await api.get<AuthResponse>('/auth/me')
        this.setAuth(data)
      } catch {
        this.clearAuth()
      } finally {
        this.initialized = true
      }
    },
    async logout() {
      await api.post('/auth/logout')
      this.clearAuth()
    }
  }
})
