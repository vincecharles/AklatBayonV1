import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    fullName: (state) => {
      if (!state.user) return ''
      return `${state.user.first_name} ${state.user.last_name}`.trim() || state.user.username
    },
  },

  actions: {
    async login(username, password) {
      const { data } = await authApi.login(username, password)
      this.accessToken = data.access
      this.refreshToken = data.refresh
      this.user = data.user
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      localStorage.setItem('user', JSON.stringify(data.user))
    },

    async logout() {
      try {
        if (this.refreshToken) {
          await authApi.logout(this.refreshToken)
        }
      } catch {
      } finally {
        this.user = null
        this.accessToken = null
        this.refreshToken = null
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
      }
    },

    async fetchUser() {
      try {
        const { data } = await authApi.getMe()
        this.user = data
        localStorage.setItem('user', JSON.stringify(data))
      } catch {
        await this.logout()
      }
    },

    initialize() {
      const token = localStorage.getItem('access_token')
      if (token) {
        this.accessToken = token
        this.refreshToken = localStorage.getItem('refresh_token')
        this.user = JSON.parse(localStorage.getItem('user') || 'null')
      }
    },
  },
})
