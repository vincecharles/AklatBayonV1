import client from './client'

export const usersApi = {
  list(params = {}) { return client.get('users/', { params }) },
  get(id) { return client.get(`users/${id}/`) },
  create(data) { return client.post('users/', data) },
  update(id, data) { return client.put(`users/${id}/`, data) },
  delete(id) { return client.delete(`users/${id}/`) },
}

export const rolesApi = {
  list(params = {}) { return client.get('roles/', { params }) },
  get(id) { return client.get(`roles/${id}/`) },
  create(data) { return client.post('roles/', data) },
  update(id, data) { return client.put(`roles/${id}/`, data) },
  delete(id) { return client.delete(`roles/${id}/`) },
  getPermissions(id) { return client.get(`roles/${id}/permissions/`) },
  updatePermissions(id, data) { return client.put(`roles/${id}/permissions/`, data) },
}

export const permissionsApi = {
  list(params = {}) { return client.get('permissions/', { params }) },
}

export const settingsApi = {
  list(params = {}) { return client.get('settings/', { params }) },
  get(id) { return client.get(`settings/${id}/`) },
  create(data) { return client.post('settings/', data) },
  update(id, data) { return client.put(`settings/${id}/`, data) },
  delete(id) { return client.delete(`settings/${id}/`) },
}

export const auditLogsApi = {
  list(params = {}) { return client.get('audit-logs/', { params }) },
}

export const dashboardApi = {
  get() { return client.get('dashboard/') },
}

export const reportsApi = {
  get(params = {}) { return client.get('reports/', { params }) },
}
