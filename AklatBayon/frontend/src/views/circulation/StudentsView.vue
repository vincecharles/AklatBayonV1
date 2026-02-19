<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Students</h1>
      <button class="btn btn-primary" @click="openCreate">+ Add Student</button>
    </div>
    <div class="toolbar">
      <div class="search-wrapper">
        <span class="search-icon">🔍</span>
        <input v-model="search" class="search-input" placeholder="Search students..." />
      </div>
    </div>
    <DataTable :columns="columns" :data="items" :loading="loading" :search-query="search" :search-keys="['student_id','first_name','last_name']">
      <template #cell-full_name="{ row }">
        <span style="font-weight:500;color:var(--text-primary)">{{ row.full_name }}</span>
      </template>
      <template #actions="{ row }">
        <button class="btn btn-ghost btn-sm" @click="openEdit(row)">✏️</button>
        <button class="btn btn-ghost btn-sm" @click="confirmDelete(row)">🗑️</button>
      </template>
    </DataTable>

    <Modal v-model="showModal" :title="editing ? 'Edit Student' : 'Add Student'" max-width="640px">
      <form @submit.prevent="save" class="flex flex-col gap-md">
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Student ID</label>
            <input v-model="form.student_id" class="form-input" required />
          </div>
          <div class="form-group">
            <label class="form-label">First Name</label>
            <input v-model="form.first_name" class="form-input" required />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Last Name</label>
            <input v-model="form.last_name" class="form-input" required />
          </div>
          <div class="form-group">
            <label class="form-label">Contact</label>
            <input v-model="form.contact" class="form-input" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Grade Level</label>
            <select v-model="form.grade_level" class="form-select" @change="onGradeChange">
              <option value="">Select grade</option>
              <option v-for="g in gradeLevels" :key="g.id" :value="g.id">{{ g.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Section</label>
            <select v-model="form.section" class="form-select">
              <option value="">Select section</option>
              <option v-for="s in sections" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Guardian Name</label>
            <input v-model="form.guardian_name" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">Guardian Contact</label>
            <input v-model="form.guardian_contact" class="form-input" />
          </div>
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
import { studentsApi, gradeLevelsApi, sectionsApi } from '@/api/students'

const items = ref([])
const gradeLevels = ref([])
const sections = ref([])
const loading = ref(true)
const search = ref('')
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)

const emptyForm = { student_id: '', first_name: '', last_name: '', contact: '', grade_level: '', section: '', guardian_name: '', guardian_contact: '' }
const form = ref({ ...emptyForm })

const columns = [
  { key: 'student_id', label: 'ID', width: '100px' },
  { key: 'full_name', label: 'Name' },
  { key: 'grade_level_name', label: 'Grade' },
  { key: 'section_name', label: 'Section' },
  { key: 'contact', label: 'Contact' },
]

async function fetchItems() {
  loading.value = true
  try {
    const [s, g] = await Promise.all([studentsApi.list(), gradeLevelsApi.list()])
    items.value = s.data.results || s.data
    gradeLevels.value = g.data.results || g.data
  } finally { loading.value = false }
}

async function onGradeChange() {
  form.value.section = ''
  if (form.value.grade_level) {
    try {
      const { data } = await sectionsApi.byGrade(form.value.grade_level)
      sections.value = data.results || data
    } catch { sections.value = [] }
  } else { sections.value = [] }
}

function openCreate() { editing.value = null; form.value = { ...emptyForm }; sections.value = []; showModal.value = true }
function openEdit(row) {
  editing.value = row
  form.value = { student_id: row.student_id, first_name: row.first_name, last_name: row.last_name, contact: row.contact || '', grade_level: row.grade_level || '', section: row.section || '', guardian_name: row.guardian_name || '', guardian_contact: row.guardian_contact || '' }
  if (row.grade_level) onGradeChange()
  showModal.value = true
}

async function save() {
  saving.value = true
  try {
    const payload = { ...form.value }
    if (!payload.grade_level) delete payload.grade_level
    if (!payload.section) delete payload.section
    if (editing.value) await studentsApi.update(editing.value.id, payload)
    else await studentsApi.create(payload)
    showModal.value = false; await fetchItems()
  } catch (e) { alert('Save failed: ' + (e.response?.data?.detail || JSON.stringify(e.response?.data))) } finally { saving.value = false }
}

async function confirmDelete(row) {
  if (!confirm(`Delete student "${row.full_name}"?`)) return
  try { await studentsApi.delete(row.id); await fetchItems() } catch { alert('Delete failed') }
}

onMounted(fetchItems)
</script>
