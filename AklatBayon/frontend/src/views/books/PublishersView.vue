<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Publishers</h1>
      <button class="btn btn-primary" @click="openCreate">+ Add Publisher</button>
    </div>
    <div class="toolbar">
      <div class="search-wrapper">
        <span class="search-icon">🔍</span>
        <input v-model="search" class="search-input" placeholder="Search publishers..." />
      </div>
    </div>
    <DataTable :columns="columns" :data="items" :loading="loading" :search-query="search" :search-keys="['name']">
      <template #actions="{ row }">
        <button class="btn btn-ghost btn-sm" @click="openEdit(row)">✏️</button>
        <button class="btn btn-ghost btn-sm" @click="confirmDelete(row)">🗑️</button>
      </template>
    </DataTable>
    <Modal v-model="showModal" :title="editing ? 'Edit Publisher' : 'Add Publisher'">
      <form @submit.prevent="save" class="flex flex-col gap-md">
        <div class="form-group">
          <label class="form-label">Name</label>
          <input v-model="form.name" class="form-input" required />
        </div>
        <div class="form-group">
          <label class="form-label">Address</label>
          <input v-model="form.address" class="form-input" />
        </div>
        <div class="form-group">
          <label class="form-label">Contact</label>
          <input v-model="form.contact" class="form-input" />
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
import { publishersApi } from '@/api/books'

const items = ref([])
const loading = ref(true)
const search = ref('')
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)
const form = ref({ name: '', address: '', contact: '' })
const columns = [
  { key: 'name', label: 'Name' },
  { key: 'address', label: 'Address' },
  { key: 'contact', label: 'Contact' },
  { key: 'created_at', label: 'Created', width: '150px' },
]

async function fetchItems() {
  loading.value = true
  try { const { data } = await publishersApi.list(); items.value = data.results || data }
  finally { loading.value = false }
}
function openCreate() { editing.value = null; form.value = { name: '', address: '', contact: '' }; showModal.value = true }
function openEdit(row) { editing.value = row; form.value = { name: row.name, address: row.address || '', contact: row.contact || '' }; showModal.value = true }
async function save() {
  saving.value = true
  try {
    if (editing.value) await publishersApi.update(editing.value.id, form.value)
    else await publishersApi.create(form.value)
    showModal.value = false; await fetchItems()
  } catch { alert('Save failed') } finally { saving.value = false }
}
async function confirmDelete(row) {
  if (!confirm(`Delete "${row.name}"?`)) return
  try { await publishersApi.delete(row.id); await fetchItems() } catch { alert('Delete failed') }
}
onMounted(fetchItems)
</script>
