import client from './client'

export const authApi = {
  login(username, password) {
    return client.post('auth/login/', { username, password })
  },

  logout(refresh) {
    return client.post('auth/logout/', { refresh })
  },

  getMe() {
    return client.get('auth/me/')
  },

  refreshToken(refresh) {
    return client.post('auth/token/refresh/', { refresh })
  },
}
