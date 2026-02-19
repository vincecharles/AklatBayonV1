<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Audit Logs</h1>
    </div>
    <div class="toolbar">
      <div class="search-wrapper">
        <span class="search-icon">🔍</span>
        <input v-model="search" class="search-input" placeholder="Search logs..." />
      </div>
      <select v-model="actionFilter" class="form-select" style="width:auto;min-width:140px">
        <option value="">All Actions</option>
        <option value="create">Create</option>
        <option value="update">Update</option>
        <option value="delete">Delete</option>
        <option value="login">Login</option>
        <option value="logout">Logout</option>
      </select>
    </div>
    <DataTable :columns="columns" :data="filteredItems" :loading="loading" :search-query="search" :search-keys="['username','description','action','model_type']">
      <template #cell-action="{ value }">
        <span class="badge" :class="actionBadge(value)">{{ value }}</span>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import DataTable from '@/components/DataTable.vue'
import { auditLogsApi } from '@/api/admin'

const items = ref([])
const loading = ref(true)
const search = ref('')
const actionFilter = ref('')

const columns = [
  { key: 'id', label: 'ID', width: '60px' },
  { key: 'username', label: 'User', width: '120px' },
  { key: 'action', label: 'Action', width: '100px' },
  { key: 'description', label: 'Description' },
  { key: 'model_type', label: 'Model', width: '100px' },
  { key: 'ip_address', label: 'IP', width: '120px' },
  { key: 'created_at', label: 'Timestamp', width: '160px' },
]

const filteredItems = computed(() => {
  if (!actionFilter.value) return items.value
  return items.value.filter(l => l.action?.toLowerCase() === actionFilter.value)
})

function actionBadge(action) {
  const map = { create: 'badge-success', update: 'badge-info', delete: 'badge-danger', login: 'badge-warning', logout: 'badge-default' }
  return map[action?.toLowerCase()] || 'badge-default'
}

onMounted(async () => {
  try { const { data } = await auditLogsApi.list(); items.value = data.results || data }
  finally { loading.value = false }
})
</script>
