<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Return Book</h1>
    </div>

    <div class="glass-card" style="padding:32px;max-width:640px">
      <div v-if="success" class="alert alert-success">✅ Book returned successfully!</div>
      <div v-if="error" class="alert alert-error">⚠️ {{ error }}</div>

      <form @submit.prevent="submit" class="flex flex-col gap-md">
        <div class="form-group">
          <label class="form-label">Active Transaction</label>
          <select v-model="selectedTransaction" class="form-select" required>
            <option value="">Select a transaction</option>
            <option v-for="t in activeTransactions" :key="t.id" :value="t.id">
              #{{ t.id }} — {{ t.student_name }} → {{ t.book_title }} ({{ t.accession_number }})
            </option>
          </select>
        </div>

        <div v-if="selectedTx" class="detail-box">
          <div class="detail-row"><span class="detail-label">Student</span><span>{{ selectedTx.student_name }}</span></div>
          <div class="detail-row"><span class="detail-label">Book</span><span>{{ selectedTx.book_title }}</span></div>
          <div class="detail-row"><span class="detail-label">Issued</span><span>{{ selectedTx.issued_date }}</span></div>
          <div class="detail-row"><span class="detail-label">Due</span>
            <span :class="isOverdue ? 'text-danger' : ''">{{ selectedTx.due_date }} {{ isOverdue ? '(OVERDUE)' : '' }}</span>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Notes</label>
          <textarea v-model="notes" class="form-textarea" rows="2" placeholder="Optional return notes..."></textarea>
        </div>

        <button type="submit" class="btn btn-primary btn-lg" :disabled="submitting || !selectedTransaction">
          {{ submitting ? 'Processing…' : '📥 Process Return' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { transactionsApi, circulationApi } from '@/api/circulation'

const activeTransactions = ref([])
const selectedTransaction = ref('')
const notes = ref('')
const submitting = ref(false)
const success = ref(false)
const error = ref('')

const selectedTx = computed(() => activeTransactions.value.find(t => t.id === Number(selectedTransaction.value)))
const isOverdue = computed(() => selectedTx.value && new Date(selectedTx.value.due_date) < new Date())

onMounted(async () => {
  try {
    const { data } = await transactionsApi.list({ status: 'borrowed' })
    activeTransactions.value = data.results || data
  } catch (e) { console.error(e) }
})

async function submit() {
  submitting.value = true; success.value = false; error.value = ''
  try {
    await circulationApi.returnBook({
      transaction_id: Number(selectedTransaction.value),
      notes: notes.value,
    })
    success.value = true
    activeTransactions.value = activeTransactions.value.filter(t => t.id !== Number(selectedTransaction.value))
    selectedTransaction.value = ''
    notes.value = ''
  } catch (e) {
    error.value = e.response?.data?.detail || 'Return failed'
  } finally { submitting.value = false }
}
</script>

<style scoped>
.detail-box {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  background: var(--bg-glass);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
}
.detail-row { display: flex; justify-content: space-between; font-size: 0.9rem; }
.detail-label { color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase; }
</style>
