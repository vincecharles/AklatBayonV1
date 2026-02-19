<template>
  <div>
    <div class="data-table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th
              v-for="col in columns"
              :key="col.key"
              :class="{ sorted: sortKey === col.key }"
              :style="col.width ? { width: col.width } : {}"
              @click="col.sortable !== false && toggleSort(col.key)"
            >
              {{ col.label }}
              <span v-if="sortKey === col.key" class="sort-arrow">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
            </th>
            <th v-if="$slots.actions" style="width: 120px">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td :colspan="totalCols" class="text-center" style="padding:40px">
              <div class="loading-center"><div class="spinner"></div></div>
            </td>
          </tr>
          <tr v-else-if="sortedData.length === 0">
            <td :colspan="totalCols">
              <div class="empty-state">
                <div class="empty-icon">📭</div>
                <div class="empty-title">No records found</div>
                <div class="empty-desc">Try adjusting your search or filters.</div>
              </div>
            </td>
          </tr>
          <tr v-for="row in paginatedData" :key="row.id || row[columns[0]?.key]">
            <td v-for="col in columns" :key="col.key">
              <slot :name="'cell-' + col.key" :row="row" :value="row[col.key]">
                {{ row[col.key] }}
              </slot>
            </td>
            <td v-if="$slots.actions">
              <div class="flex gap-sm">
                <slot name="actions" :row="row" />
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="totalPages > 1" class="pagination">
      <button class="page-btn" :disabled="currentPage <= 1" @click="currentPage--">‹</button>
      <button
        v-for="p in displayPages"
        :key="p"
        class="page-btn"
        :class="{ active: p === currentPage }"
        @click="currentPage = p"
      >{{ p }}</button>
      <button class="page-btn" :disabled="currentPage >= totalPages" @click="currentPage++">›</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  columns: { type: Array, required: true },
  data: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  perPage: { type: Number, default: 10 },
  searchQuery: { type: String, default: '' },
  searchKeys: { type: Array, default: () => [] },
})

const sortKey = ref('')
const sortOrder = ref('asc')
const currentPage = ref(1)

const totalCols = computed(() => props.columns.length + (!!Object.keys({}).length || 1))

watch(() => props.searchQuery, () => { currentPage.value = 1 })

function toggleSort(key) {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
}

const filteredData = computed(() => {
  if (!props.searchQuery || props.searchKeys.length === 0) return props.data
  const q = props.searchQuery.toLowerCase()
  return props.data.filter(row =>
    props.searchKeys.some(key => String(row[key] || '').toLowerCase().includes(q))
  )
})

const sortedData = computed(() => {
  if (!sortKey.value) return filteredData.value
  return [...filteredData.value].sort((a, b) => {
    const va = a[sortKey.value] ?? ''
    const vb = b[sortKey.value] ?? ''
    const cmp = String(va).localeCompare(String(vb), undefined, { numeric: true })
    return sortOrder.value === 'asc' ? cmp : -cmp
  })
})

const totalPages = computed(() => Math.ceil(sortedData.value.length / props.perPage))

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * props.perPage
  return sortedData.value.slice(start, start + props.perPage)
})

const displayPages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value
  let start = Math.max(1, current - 2)
  let end = Math.min(total, current + 2)
  if (end - start < 4) {
    if (start === 1) end = Math.min(total, start + 4)
    else start = Math.max(1, end - 4)
  }
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})
</script>
