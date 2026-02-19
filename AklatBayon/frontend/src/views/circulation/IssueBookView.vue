<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Issue Book</h1>
    </div>

    <div class="glass-card" style="padding:32px;max-width:640px">
      <div v-if="success" class="alert alert-success">✅ Book issued successfully!</div>
      <div v-if="error" class="alert alert-error">⚠️ {{ error }}</div>

      <form @submit.prevent="submit" class="flex flex-col gap-md">
        <div class="form-group">
          <label class="form-label">Student</label>
          <select v-model="form.student_id" class="form-select" required>
            <option value="">Select a student</option>
            <option v-for="s in students" :key="s.id" :value="s.id">{{ s.student_id }} — {{ s.full_name }}</option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">Book Copy (Accession Number)</label>
          <select v-model="form.book_copy_id" class="form-select" required>
            <option value="">Select a book copy</option>
            <option v-for="c in availableCopies" :key="c.id" :value="c.id">{{ c.accession_number }} — {{ c.book_title }}</option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">Due Date</label>
          <input v-model="form.due_date" type="date" class="form-input" required />
        </div>

        <div class="form-group">
          <label class="form-label">Notes</label>
          <textarea v-model="form.notes" class="form-textarea" rows="2" placeholder="Optional notes..."></textarea>
        </div>

        <button type="submit" class="btn btn-primary btn-lg" :disabled="submitting">
          {{ submitting ? 'Issuing…' : '📤 Issue Book' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { studentsApi } from '@/api/students'
import { bookCopiesApi } from '@/api/books'
import { circulationApi } from '@/api/circulation'

const students = ref([])
const availableCopies = ref([])
const submitting = ref(false)
const success = ref(false)
const error = ref('')

const form = ref({ student_id: '', book_copy_id: '', due_date: '', notes: '' })

onMounted(async () => {
  try {
    const [s, c] = await Promise.all([studentsApi.list(), bookCopiesApi.list({ status: 'available' })])
    students.value = s.data.results || s.data
    const copies = c.data.results || c.data
    // enrich copies with book title if available
    availableCopies.value = copies.map(copy => ({
      ...copy,
      book_title: copy.book_title || `Book #${copy.book}`
    }))
  } catch (e) { console.error(e) }
})

async function submit() {
  submitting.value = true; success.value = false; error.value = ''
  try {
    await circulationApi.issueBook({
      book_copy_id: Number(form.value.book_copy_id),
      student_id: Number(form.value.student_id),
      due_date: form.value.due_date,
      notes: form.value.notes,
    })
    success.value = true
    form.value = { student_id: '', book_copy_id: '', due_date: '', notes: '' }
  } catch (e) {
    error.value = e.response?.data?.detail || Object.values(e.response?.data || {}).flat().join(', ') || 'Issue failed'
  } finally { submitting.value = false }
}
</script>
