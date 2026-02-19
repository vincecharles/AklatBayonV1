import client from './client'

export const studentsApi = {
  list(params = {}) { return client.get('students/', { params }) },
  get(id) { return client.get(`students/${id}/`) },
  create(data) { return client.post('students/', data) },
  update(id, data) { return client.put(`students/${id}/`, data) },
  delete(id) { return client.delete(`students/${id}/`) },
}

export const gradeLevelsApi = {
  list(params = {}) { return client.get('grade-levels/', { params }) },
}

export const sectionsApi = {
  list(params = {}) { return client.get('sections/', { params }) },
  byGrade(gradeId) { return client.get(`sections/by-grade/${gradeId}/`) },
}

export const academicYearsApi = {
  list(params = {}) { return client.get('academic-years/', { params }) },
}
