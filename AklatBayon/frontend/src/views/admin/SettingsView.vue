<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Settings</h1>
      <button class="btn btn-primary" @click="openCreate">+ Add Setting</button>
    </div>

    <div v-if="loading" class="loading-center"><div class="spinner"></div></div>

    <div v-else class="glass-card" style="padding:24px">
      <div v-if="items.length === 0" class="empty-state">
        <div class="empty-icon">⚙️</div>
        <div class="empty-title">No settings configured</div>
      </div>

      <div v-else class="settings-list">
        <div v-for="item in items" :key="item.id" class="setting-row">
          <div class="setting-info">
            <span class="setting-key">{{ item.key }}</span>
            <span class="setting-value">{{ item.value }}</span>
          </div>
          <div class="flex gap-sm">
            <button class="btn btn-ghost btn-sm" @click="openEdit(item)">✏️</button>
            <button class="btn btn-ghost btn-sm" @click="confirmDelete(item)">🗑️</button>
          </div>
        </div>
      </div>
    </div>

    <Modal v-model="showModal" :title="editing ? 'Edit Setting' : 'Add Setting'">
      <form @submit.prevent="save" class="flex flex-col gap-md">
        <div class="form-group">
          <label class="form-label">Key</label>
          <input v-model="form.key" class="form-input" required :disabled="!!editing" />
        </div>
        <div class="form-group">
          <label class="form-label">Value</label>
          <textarea v-model="form.value" class="form-textarea" rows="3" required></textarea>
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
import Modal from '@/components/Modal.vue'
import { settingsApi } from '@/api/admin'

const items = ref([])
const loading = ref(true)
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)
const form = ref({ key: '', value: '' })

async function fetchItems() {
  loading.value = true
  try { const { data } = await settingsApi.list(); items.value = data.results || data }
  finally { loading.value = false }
}

function openCreate() { editing.value = null; form.value = { key: '', value: '' }; showModal.value = true }
function openEdit(item) { editing.value = item; form.value = { key: item.key, value: item.value }; showModal.value = true }

async function save() {
  saving.value = true
  try {
    if (editing.value) await settingsApi.update(editing.value.id, form.value)
    else await settingsApi.create(form.value)
    showModal.value = false; await fetchItems()
  } catch { alert('Save failed') } finally { saving.value = false }
}

async function confirmDelete(item) {
  if (!confirm(`Delete setting "${item.key}"?`)) return
  try { await settingsApi.delete(item.id); await fetchItems() } catch { alert('Delete failed') }
}

onMounted(fetchItems)
</script>

<style scoped>
.settings-list { display: flex; flex-direction: column; gap: 8px; }
.setting-row { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; background: var(--bg-glass); border-radius: var(--radius-sm); transition: background var(--transition-fast); }
.setting-row:hover { background: var(--bg-glass-hover); }
.setting-info { display: flex; flex-direction: column; gap: 4px; }
.setting-key { font-size: 0.85rem; font-weight: 600; color: var(--accent-primary-hover); font-family: monospace; }
.setting-value { font-size: 0.85rem; color: var(--text-secondary); }
</style>
