import client from './client'

export const booksApi = {
  list(params = {}) { return client.get('books/', { params }) },
  get(id) { return client.get(`books/${id}/`) },
  create(data) { return client.post('books/', data) },
  update(id, data) { return client.put(`books/${id}/`, data) },
  delete(id) { return client.delete(`books/${id}/`) },
}

export const bookCopiesApi = {
  list(params = {}) { return client.get('book-copies/', { params }) },
  get(id) { return client.get(`book-copies/${id}/`) },
  create(data) { return client.post('book-copies/', data) },
  update(id, data) { return client.put(`book-copies/${id}/`, data) },
  delete(id) { return client.delete(`book-copies/${id}/`) },
}

export const authorsApi = {
  list(params = {}) { return client.get('authors/', { params }) },
  get(id) { return client.get(`authors/${id}/`) },
  create(data) { return client.post('authors/', data) },
  update(id, data) { return client.put(`authors/${id}/`, data) },
  delete(id) { return client.delete(`authors/${id}/`) },
}

export const publishersApi = {
  list(params = {}) { return client.get('publishers/', { params }) },
  get(id) { return client.get(`publishers/${id}/`) },
  create(data) { return client.post('publishers/', data) },
  update(id, data) { return client.put(`publishers/${id}/`, data) },
  delete(id) { return client.delete(`publishers/${id}/`) },
}

export const categoriesApi = {
  list(params = {}) { return client.get('categories/', { params }) },
  get(id) { return client.get(`categories/${id}/`) },
  create(data) { return client.post('categories/', data) },
  update(id, data) { return client.put(`categories/${id}/`, data) },
  delete(id) { return client.delete(`categories/${id}/`) },
}

export const catalogApi = {
  list(params = {}) { return client.get('catalog/', { params }) },
}
