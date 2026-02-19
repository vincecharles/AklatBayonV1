<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Users</h1>
      <button class="btn btn-primary" @click="openCreate">+ Add User</button>
    </div>
    <div class="toolbar">
      <div class="search-wrapper">
        <span class="search-icon">🔍</span>
        <input v-model="search" class="search-input" placeholder="Search users..." />
      </div>
    </div>
    <DataTable :columns="columns" :data="items" :loading="loading" :search-query="search" :search-keys="['username','email','first_name','last_name']">
      <template #cell-username="{ row }">
        <span style="font-weight:500;color:var(--text-primary)">{{ row.username }}</span>
      </template>
      <template #cell-is_active="{ value }">
        <span class="badge" :class="value ? 'badge-success' : 'badge-danger'">{{ value ? 'Active' : 'Inactive' }}</span>
      </template>
      <template #cell-role_detail="{ row }">
        {{ row.role_detail?.name || '—' }}
      </template>
      <template #actions="{ row }">
        <button class="btn btn-ghost btn-sm" @click="openEdit(row)">✏️</button>
        <button class="btn btn-ghost btn-sm" @click="confirmDelete(row)">🗑️</button>
      </template>
    </DataTable>

    <Modal v-model="showModal" :title="editing ? 'Edit User' : 'Add User'" max-width="640px">
      <form @submit.prevent="save" class="flex flex-col gap-md">
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Username</label>
            <input v-model="form.username" class="form-input" required />
          </div>
          <div class="form-group">
            <label class="form-label">Email</label>
            <input v-model="form.email" type="email" class="form-input" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">First Name</label>
            <input v-model="form.first_name" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">Last Name</label>
            <input v-model="form.last_name" class="form-input" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Password {{ editing ? '(leave blank to keep)' : '' }}</label>
            <input v-model="form.password" type="password" class="form-input" :required="!editing" />
          </div>
          <div class="form-group">
            <label class="form-label">User Type</label>
            <input v-model="form.user_type" class="form-input" placeholder="e.g. librarian" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Role</label>
            <select v-model="form.role" class="form-select">
              <option value="">No role</option>
              <option v-for="r in roles" :key="r.id" :value="r.id">{{ r.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Phone</label>
            <input v-model="form.phone" class="form-input" />
          </div>
        </div>
        <div class="form-group">
          <label style="display:flex;align-items:center;gap:8px;cursor:pointer">
            <input v-model="form.is_active" type="checkbox" /> Active
          </label>
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
import { usersApi, rolesApi } from '@/api/admin'

const items = ref([])
const roles = ref([])
const loading = ref(true)
const search = ref('')
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)

const emptyForm = { username: '', email: '', first_name: '', last_name: '', password: '', user_type: '', role: '', phone: '', is_active: true }
const form = ref({ ...emptyForm })

const columns = [
  { key: 'username', label: 'Username' },
  { key: 'email', label: 'Email' },
  { key: 'first_name', label: 'First Name' },
  { key: 'last_name', label: 'Last Name' },
  { key: 'role_detail', label: 'Role', width: '120px' },
  { key: 'is_active', label: 'Status', width: '90px' },
]

async function fetchItems() {
  loading.value = true
  try {
    const [u, r] = await Promise.all([usersApi.list(), rolesApi.list()])
    items.value = u.data.results || u.data
    roles.value = r.data.results || r.data
  } finally { loading.value = false }
}

function openCreate() { editing.value = null; form.value = { ...emptyForm }; showModal.value = true }
function openEdit(row) {
  editing.value = row
  form.value = { username: row.username, email: row.email || '', first_name: row.first_name || '', last_name: row.last_name || '', password: '', user_type: row.user_type || '', role: row.role || '', phone: row.phone || '', is_active: row.is_active }
  showModal.value = true
}

async function save() {
  saving.value = true
  try {
    const payload = { ...form.value }
    if (editing.value && !payload.password) delete payload.password
    if (!payload.role) delete payload.role
    if (editing.value) await usersApi.update(editing.value.id, payload)
    else await usersApi.create(payload)
    showModal.value = false; await fetchItems()
  } catch (e) { alert('Save failed: ' + JSON.stringify(e.response?.data)) } finally { saving.value = false }
}

async function confirmDelete(row) {
  if (!confirm(`Delete user "${row.username}"?`)) return
  try { await usersApi.delete(row.id); await fetchItems() } catch { alert('Delete failed') }
}

onMounted(fetchItems)
</script>
