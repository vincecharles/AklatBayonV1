<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Books</h1>
      <button class="btn btn-primary" @click="openCreate">+ Add Book</button>
    </div>

    <div class="toolbar">
      <div class="search-wrapper">
        <span class="search-icon">🔍</span>
        <input v-model="search" class="search-input" placeholder="Search books..." />
      </div>
    </div>

    <DataTable
      :columns="columns"
      :data="books"
      :loading="loading"
      :search-query="search"
      :search-keys="['title', 'isbn', 'author_name']"
    >
      <template #cell-title="{ row }">
        <router-link :to="`/books/${row.id}`" style="color:var(--accent-primary-hover);font-weight:500">
          {{ row.title }}
        </router-link>
      </template>
      <template #cell-available_copies="{ row }">
        <span class="badge" :class="row.available_copies > 0 ? 'badge-success' : 'badge-danger'">
          {{ row.available_copies }} / {{ row.total_copies }}
        </span>
      </template>
      <template #actions="{ row }">
        <button class="btn btn-ghost btn-sm" @click="openEdit(row)">✏️</button>
        <button class="btn btn-ghost btn-sm" @click="confirmDelete(row)">🗑️</button>
      </template>
    </DataTable>

    <Modal v-model="showModal" :title="editing ? 'Edit Book' : 'Add Book'">
      <form @submit.prevent="save" class="flex flex-col gap-md">
        <div v-if="formError" class="alert alert-error">{{ formError }}</div>
        <div class="form-group">
          <label class="form-label">Title</label>
          <input v-model="form.title" class="form-input" required />
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">ISBN</label>
            <input v-model="form.isbn" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">Publication Year</label>
            <input v-model="form.publication_year" type="number" class="form-input" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Author</label>
            <select v-model="form.author" class="form-select">
              <option value="">Select author</option>
              <option v-for="a in authors" :key="a.id" :value="a.id">{{ a.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Category</label>
            <select v-model="form.category" class="form-select">
              <option value="">Select category</option>
              <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">Publisher</label>
          <select v-model="form.publisher" class="form-select">
            <option value="">Select publisher</option>
            <option v-for="p in publishers" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Description</label>
          <textarea v-model="form.description" class="form-textarea" rows="3"></textarea>
        </div>
      </form>
      <template #footer>
        <button class="btn btn-secondary" @click="showModal = false">Cancel</button>
        <button class="btn btn-primary" @click="save" :disabled="saving">{{ saving ? 'Saving…' : 'Save' }}</button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DataTable from '@/components/DataTable.vue'
import Modal from '@/components/Modal.vue'
import { booksApi, authorsApi, publishersApi, categoriesApi } from '@/api/books'

const books = ref([])
const authors = ref([])
const publishers = ref([])
const categories = ref([])
const loading = ref(true)
const search = ref('')
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)
const formError = ref('')

const emptyForm = { title: '', isbn: '', publication_year: '', author: '', publisher: '', category: '', description: '' }
const form = ref({ ...emptyForm })

const columns = [
  { key: 'title', label: 'Title' },
  { key: 'isbn', label: 'ISBN', width: '130px' },
  { key: 'author_name', label: 'Author' },
  { key: 'category_name', label: 'Category' },
  { key: 'publication_year', label: 'Year', width: '80px' },
  { key: 'available_copies', label: 'Copies', width: '100px' },
]

async function fetchAll() {
  loading.value = true
  try {
    const [b, a, p, c] = await Promise.all([
      booksApi.list(), authorsApi.list(), publishersApi.list(), categoriesApi.list()
    ])
    books.value = b.data.results || b.data
    authors.value = a.data.results || a.data
    publishers.value = p.data.results || p.data
    categories.value = flattenCategories(c.data.results || c.data)
  } finally { loading.value = false }
}

function flattenCategories(cats, result = []) {
  cats.forEach(c => {
    result.push({ id: c.id, name: c.name })
    if (c.children?.length) flattenCategories(c.children, result)
  })
  return result
}

function openCreate() {
  editing.value = null
  form.value = { ...emptyForm }
  formError.value = ''
  showModal.value = true
}

function openEdit(row) {
  editing.value = row
  form.value = { title: row.title, isbn: row.isbn, publication_year: row.publication_year, author: row.author, publisher: row.publisher, category: row.category, description: row.description || '' }
  formError.value = ''
  showModal.value = true
}

async function save() {
  saving.value = true
  formError.value = ''
  try {
    if (editing.value) {
      await booksApi.update(editing.value.id, form.value)
    } else {
      await booksApi.create(form.value)
    }
    showModal.value = false
    await fetchAll()
  } catch (e) {
    formError.value = e.response?.data?.detail || Object.values(e.response?.data || {}).flat().join(', ') || 'Save failed'
  } finally { saving.value = false }
}

async function confirmDelete(row) {
  if (!confirm(`Delete "${row.title}"?`)) return
  try {
    await booksApi.delete(row.id)
    await fetchAll()
  } catch (e) {
    alert('Delete failed: ' + (e.response?.data?.detail || 'Unknown error'))
  }
}

onMounted(fetchAll)
</script>
