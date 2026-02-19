<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Reports</h1>
    </div>

    <div class="glass-card" style="padding:24px;margin-bottom:24px">
      <div class="toolbar" style="margin-bottom:0">
        <div class="form-group" style="min-width:220px">
          <label class="form-label">Report Type</label>
          <select v-model="reportType" class="form-select" @change="fetchReport">
            <option value="">Select a report</option>
            <option value="books_summary">Books Summary</option>
            <option value="circulation_summary">Circulation Summary</option>
            <option value="overdue_books">Overdue Books</option>
            <option value="fines_summary">Fines Summary</option>
            <option value="popular_books">Popular Books</option>
            <option value="student_activity">Student Activity</option>
          </select>
        </div>
        <button class="btn btn-primary" @click="fetchReport" :disabled="!reportType || loading" style="align-self:flex-end">
          {{ loading ? 'Generating…' : '📈 Generate' }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading-center"><div class="spinner"></div></div>

    <div v-else-if="reportData" class="glass-card" style="padding:24px">
      <h3 class="card-title" style="margin-bottom:16px">{{ reportType.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()) }}</h3>

      <div v-if="Array.isArray(reportData)" class="data-table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th v-for="key in reportKeys" :key="key">{{ key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()) }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, i) in reportData" :key="i">
              <td v-for="key in reportKeys" :key="key">{{ row[key] }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else-if="typeof reportData === 'object'">
        <div class="stats-grid">
          <div v-for="(value, key) in reportData" :key="key" class="stat-card">
            <div class="stat-value">{{ value }}</div>
            <div class="stat-label">{{ key.replace(/_/g, ' ') }}</div>
          </div>
        </div>
      </div>

      <p v-else>{{ reportData }}</p>
    </div>

    <div v-else-if="reportType && !loading" class="glass-card" style="padding:40px">
      <div class="empty-state">
        <div class="empty-icon">📈</div>
        <div class="empty-title">Select a report type and click Generate</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { reportsApi } from '@/api/admin'

const reportType = ref('')
const reportData = ref(null)
const loading = ref(false)

const reportKeys = computed(() => {
  if (!Array.isArray(reportData.value) || reportData.value.length === 0) return []
  return Object.keys(reportData.value[0])
})

async function fetchReport() {
  if (!reportType.value) return
  loading.value = true; reportData.value = null
  try {
    const { data } = await reportsApi.get({ type: reportType.value })
    reportData.value = data.results || data.data || data
  } catch (e) {
    reportData.value = 'Failed to generate report: ' + (e.response?.data?.detail || 'Error')
  } finally { loading.value = false }
}
</script>

<style scoped>
.card-title { font-size: 1rem; font-weight: 600; }
</style>
