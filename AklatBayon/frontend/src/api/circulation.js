import client from './client'

export const circulationApi = {
  issueBook(data) { return client.post('circulation/issue/', data) },
  returnBook(data) { return client.post('circulation/return/', data) },
}

export const transactionsApi = {
  list(params = {}) { return client.get('transactions/', { params }) },
  get(id) { return client.get(`transactions/${id}/`) },
}

export const finesApi = {
  list(params = {}) { return client.get('fines/', { params }) },
  collect(id) { return client.post(`fines/${id}/collect/`) },
  waive(id) { return client.post(`fines/${id}/waive/`) },
}

export const reservationsApi = {
  list(params = {}) { return client.get('reservations/', { params }) },
  create(data) { return client.post('reservations/', data) },
  update(id, data) { return client.put(`reservations/${id}/`, data) },
  delete(id) { return client.delete(`reservations/${id}/`) },
}
