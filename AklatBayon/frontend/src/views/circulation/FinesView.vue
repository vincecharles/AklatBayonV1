<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Fines</h1>
    </div>
    <div class="toolbar">
      <div class="search-wrapper">
        <span class="search-icon">🔍</span>
        <input v-model="search" class="search-input" placeholder="Search fines..." />
      </div>
      <select v-model="statusFilter" class="form-select" style="width:auto;min-width:140px">
        <option value="">All Status</option>
        <option value="pending">Pending</option>
        <option value="paid">Paid</option>
        <option value="waived">Waived</option>
      </select>
    </div>
    <DataTable :columns="columns" :data="filteredItems" :loading="loading" :search-query="search" :search-keys="['reason']">
      <template #cell-amount="{ value }">
        <span style="font-weight:600;font-family:monospace">₱{{ Number(value).toFixed(2) }}</span>
      </template>
      <template #cell-status="{ value }">
        <span class="badge" :class="statusBadge(value)">{{ value }}</span>
      </template>
      <template #actions="{ row }">
        <template v-if="row.status === 'pending'">
          <button class="btn btn-success btn-sm" @click="collectFine(row)">💵 Collect</button>
          <button class="btn btn-ghost btn-sm" @click="waiveFine(row)">🚫 Waive</button>
        </template>
        <span v-else class="text-muted" style="font-size:0.8rem">—</span>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import DataTable from '@/components/DataTable.vue'
import { finesApi } from '@/api/circulation'

const items = ref([])
const loading = ref(true)
const search = ref('')
const statusFilter = ref('')

const columns = [
  { key: 'id', label: 'ID', width: '60px' },
  { key: 'transaction', label: 'Transaction', width: '100px' },
  { key: 'reason', label: 'Reason' },
  { key: 'amount', label: 'Amount', width: '100px' },
  { key: 'status', label: 'Status', width: '100px' },
  { key: 'created_at', label: 'Date', width: '130px' },
]

const filteredItems = computed(() => {
  if (!statusFilter.value) return items.value
  return items.value.filter(f => f.status === statusFilter.value)
})

function statusBadge(status) {
  return { pending: 'badge-warning', paid: 'badge-success', waived: 'badge-info' }[status] || 'badge-default'
}

async function fetchItems() {
  loading.value = true
  try { const { data } = await finesApi.list(); items.value = data.results || data }
  finally { loading.value = false }
}

async function collectFine(row) {
  if (!confirm('Mark this fine as collected/paid?')) return
  try { await finesApi.collect(row.id); await fetchItems() } catch { alert('Collect failed') }
}

async function waiveFine(row) {
  if (!confirm('Waive this fine?')) return
  try { await finesApi.waive(row.id); await fetchItems() } catch { alert('Waive failed') }
}

onMounted(fetchItems)
</script>
