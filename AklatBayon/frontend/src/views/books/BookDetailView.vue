<template>
  <div>
    <div class="page-header">
      <div>
        <router-link to="/books" class="back-link">← Back to Books</router-link>
        <h1 class="page-title mt-sm">{{ book?.title || 'Book Detail' }}</h1>
      </div>
      <div class="flex gap-sm">
        <button class="btn btn-secondary" @click="openEditCopy">+ Add Copy</button>
      </div>
    </div>

    <div v-if="loading" class="loading-center"><div class="spinner"></div></div>

    <template v-else-if="book">
      <div class="detail-grid">
        <div class="glass-card detail-card">
          <h3 class="card-title">Book Information</h3>
          <div class="detail-rows">
            <div class="detail-row"><span class="detail-label">Title</span><span>{{ book.title }}</span></div>
            <div class="detail-row"><span class="detail-label">ISBN</span><span>{{ book.isbn || '—' }}</span></div>
            <div class="detail-row"><span class="detail-label">Author</span><span>{{ book.author_detail?.name || '—' }}</span></div>
            <div class="detail-row"><span class="detail-label">Publisher</span><span>{{ book.publisher_detail?.name || '—' }}</span></div>
            <div class="detail-row"><span class="detail-label">Category</span><span>{{ book.category_detail?.name || '—' }}</span></div>
            <div class="detail-row"><span class="detail-label">Year</span><span>{{ book.publication_year || '—' }}</span></div>
            <div class="detail-row"><span class="detail-label">Total Copies</span><span>{{ book.total_copies }}</span></div>
            <div class="detail-row"><span class="detail-label">Available</span>
              <span class="badge" :class="book.available_copies > 0 ? 'badge-success' : 'badge-danger'">
                {{ book.available_copies }}
              </span>
            </div>
          </div>
          <div v-if="book.description" class="mt-md">
            <span class="detail-label">Description</span>
            <p style="margin-top:6px;color:var(--text-secondary);font-size:0.9rem">{{ book.description }}</p>
          </div>
        </div>

        <div class="glass-card detail-card">
          <h3 class="card-title">Book Copies</h3>
          <div class="copies-list">
            <div v-for="copy in book.copies" :key="copy.id" class="copy-item">
              <span class="copy-accession">{{ copy.accession_number }}</span>
              <span class="badge" :class="statusBadge(copy.status)">{{ copy.status }}</span>
            </div>
            <div v-if="!book.copies?.length" class="empty-state" style="padding:20px">
              <div class="empty-title">No copies registered</div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <Modal v-model="showCopyModal" title="Add Book Copy">
      <form @submit.prevent="saveCopy" class="flex flex-col gap-md">
        <div class="form-group">
          <label class="form-label">Accession Number</label>
          <input v-model="copyForm.accession_number" class="form-input" required />
        </div>
        <div class="form-group">
          <label class="form-label">Status</label>
          <select v-model="copyForm.status" class="form-select">
            <option value="available">Available</option>
            <option value="borrowed">Borrowed</option>
            <option value="reserved">Reserved</option>
            <option value="lost">Lost</option>
            <option value="damaged">Damaged</option>
          </select>
        </div>
      </form>
      <template #footer>
        <button class="btn btn-secondary" @click="showCopyModal = false">Cancel</button>
        <button class="btn btn-primary" @click="saveCopy">Add Copy</button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Modal from '@/components/Modal.vue'
import { booksApi, bookCopiesApi } from '@/api/books'

const route = useRoute()
const book = ref(null)
const loading = ref(true)
const showCopyModal = ref(false)
const copyForm = ref({ accession_number: '', status: 'available' })

async function fetchBook() {
  loading.value = true
  try {
    const { data } = await booksApi.get(route.params.id)
    book.value = data
  } finally { loading.value = false }
}

function statusBadge(status) {
  const map = { available: 'badge-success', borrowed: 'badge-warning', reserved: 'badge-info', lost: 'badge-danger', damaged: 'badge-danger' }
  return map[status] || 'badge-default'
}

function openEditCopy() {
  copyForm.value = { accession_number: '', status: 'available' }
  showCopyModal.value = true
}

async function saveCopy() {
  try {
    await bookCopiesApi.create({ ...copyForm.value, book: route.params.id })
    showCopyModal.value = false
    await fetchBook()
  } catch (e) {
    alert('Failed to add copy: ' + (e.response?.data?.detail || 'Error'))
  }
}

onMounted(fetchBook)
</script>

<style scoped>
.back-link { font-size: 0.85rem; color: var(--text-muted); }
.back-link:hover { color: var(--accent-primary); }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.detail-card { padding: 24px; }
.card-title { font-size: 1rem; font-weight: 600; margin-bottom: 16px; }
.detail-rows { display: flex; flex-direction: column; gap: 12px; }
.detail-row { display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem; }
.detail-label { color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.04em; }
.copies-list { display: flex; flex-direction: column; gap: 8px; }
.copy-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: var(--bg-glass); border-radius: var(--radius-sm); }
.copy-accession { font-family: monospace; font-size: 0.85rem; color: var(--text-primary); }
@media (max-width: 1024px) { .detail-grid { grid-template-columns: 1fr; } }
</style>
