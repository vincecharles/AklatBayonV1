<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Transaction History</h1>
    </div>
    <div class="toolbar">
      <div class="search-wrapper">
        <span class="search-icon">🔍</span>
        <input v-model="search" class="search-input" placeholder="Search transactions..." />
      </div>
      <select v-model="statusFilter" class="form-select" style="width:auto;min-width:140px">
        <option value="">All Status</option>
        <option value="borrowed">Borrowed</option>
        <option value="returned">Returned</option>
        <option value="overdue">Overdue</option>
      </select>
    </div>
    <DataTable :columns="columns" :data="filteredItems" :loading="loading" :search-query="search" :search-keys="['student_name','book_title','accession_number']">
      <template #cell-status="{ value }">
        <span class="badge" :class="statusBadge(value)">{{ value }}</span>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import DataTable from '@/components/DataTable.vue'
import { transactionsApi } from '@/api/circulation'

const items = ref([])
const loading = ref(true)
const search = ref('')
const statusFilter = ref('')

const columns = [
  { key: 'id', label: 'ID', width: '60px' },
  { key: 'student_name', label: 'Student' },
  { key: 'book_title', label: 'Book' },
  { key: 'accession_number', label: 'Accession', width: '120px' },
  { key: 'issued_date', label: 'Issued', width: '110px' },
  { key: 'due_date', label: 'Due', width: '110px' },
  { key: 'returned_date', label: 'Returned', width: '110px' },
  { key: 'status', label: 'Status', width: '100px' },
]

const filteredItems = computed(() => {
  if (!statusFilter.value) return items.value
  return items.value.filter(t => t.status === statusFilter.value)
})

function statusBadge(status) {
  return { borrowed: 'badge-warning', returned: 'badge-success', overdue: 'badge-danger' }[status] || 'badge-default'
}

onMounted(async () => {
  try { const { data } = await transactionsApi.list(); items.value = data.results || data }
  finally { loading.value = false }
})
</script>
