<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Authors</h1>
      <button class="btn btn-primary" @click="openCreate">+ Add Author</button>
    </div>
    <div class="toolbar">
      <div class="search-wrapper">
        <span class="search-icon">🔍</span>
        <input v-model="search" class="search-input" placeholder="Search authors..." />
      </div>
    </div>
    <DataTable :columns="columns" :data="items" :loading="loading" :search-query="search" :search-keys="['name']">
      <template #actions="{ row }">
        <button class="btn btn-ghost btn-sm" @click="openEdit(row)">✏️</button>
        <button class="btn btn-ghost btn-sm" @click="confirmDelete(row)">🗑️</button>
      </template>
    </DataTable>
    <Modal v-model="showModal" :title="editing ? 'Edit Author' : 'Add Author'">
      <form @submit.prevent="save" class="flex flex-col gap-md">
        <div class="form-group">
          <label class="form-label">Name</label>
          <input v-model="form.name" class="form-input" required />
        </div>
        <div class="form-group">
          <label class="form-label">Bio</label>
          <textarea v-model="form.bio" class="form-textarea" rows="3"></textarea>
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
import { authorsApi } from '@/api/books'

const items = ref([])
const loading = ref(true)
const search = ref('')
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)
const form = ref({ name: '', bio: '' })
const columns = [
  { key: 'name', label: 'Name' },
  { key: 'bio', label: 'Bio' },
  { key: 'created_at', label: 'Created', width: '150px' },
]

async function fetchItems() {
  loading.value = true
  try { const { data } = await authorsApi.list(); items.value = data.results || data }
  finally { loading.value = false }
}
function openCreate() { editing.value = null; form.value = { name: '', bio: '' }; showModal.value = true }
function openEdit(row) { editing.value = row; form.value = { name: row.name, bio: row.bio || '' }; showModal.value = true }
async function save() {
  saving.value = true
  try {
    if (editing.value) await authorsApi.update(editing.value.id, form.value)
    else await authorsApi.create(form.value)
    showModal.value = false; await fetchItems()
  } catch (e) { alert('Save failed') } finally { saving.value = false }
}
async function confirmDelete(row) {
  if (!confirm(`Delete "${row.name}"?`)) return
  try { await authorsApi.delete(row.id); await fetchItems() } catch { alert('Delete failed') }
}
onMounted(fetchItems)
</script>
