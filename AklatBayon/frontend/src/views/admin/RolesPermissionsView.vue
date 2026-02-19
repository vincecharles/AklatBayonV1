<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Roles & Permissions</h1>
      <button class="btn btn-primary" @click="openCreateRole">+ Add Role</button>
    </div>

    <div v-if="loading" class="loading-center"><div class="spinner"></div></div>

    <template v-else>
      <div class="roles-grid">
        <div
          v-for="role in roles"
          :key="role.id"
          class="glass-card role-card"
          :class="{ selected: selectedRole?.id === role.id }"
          @click="selectRole(role)"
        >
          <div class="role-header">
            <h3 class="role-name">{{ role.name }}</h3>
            <div class="role-actions">
              <button class="btn btn-ghost btn-sm" @click.stop="openEditRole(role)">✏️</button>
              <button class="btn btn-ghost btn-sm" @click.stop="confirmDeleteRole(role)">🗑️</button>
            </div>
          </div>
          <p class="role-desc">{{ role.description || 'No description' }}</p>
          <span class="badge badge-info">{{ role.permissions?.length || 0 }} permissions</span>
        </div>
      </div>

      <div v-if="selectedRole" class="glass-card perm-card mt-lg">
        <h3 class="card-title">Permissions for "{{ selectedRole.name }}"</h3>
        <p class="text-muted mb-md" style="font-size:0.85rem">Toggle permissions and click Save to update.</p>

        <div v-if="permGroups.length === 0" class="empty-state" style="padding:20px">
          <div class="empty-title">No permissions available</div>
        </div>

        <div v-for="group in permGroups" :key="group.name" class="perm-group">
          <h4 class="perm-group-label">{{ group.name }}</h4>
          <div class="perm-grid">
            <label v-for="perm in group.perms" :key="perm.id" class="perm-toggle">
              <input type="checkbox" v-model="selectedPermIds" :value="perm.id" />
              <span>{{ perm.name }}</span>
            </label>
          </div>
        </div>

        <div class="mt-md">
          <button class="btn btn-primary" @click="savePermissions" :disabled="savingPerms">
            {{ savingPerms ? 'Saving…' : 'Save Permissions' }}
          </button>
        </div>
      </div>
    </template>

    <Modal v-model="showRoleModal" :title="editingRole ? 'Edit Role' : 'Add Role'">
      <form @submit.prevent="saveRole" class="flex flex-col gap-md">
        <div class="form-group">
          <label class="form-label">Name</label>
          <input v-model="roleForm.name" class="form-input" required />
        </div>
        <div class="form-group">
          <label class="form-label">Slug</label>
          <input v-model="roleForm.slug" class="form-input" />
        </div>
        <div class="form-group">
          <label class="form-label">Description</label>
          <textarea v-model="roleForm.description" class="form-textarea" rows="2"></textarea>
        </div>
      </form>
      <template #footer>
        <button class="btn btn-secondary" @click="showRoleModal = false">Cancel</button>
        <button class="btn btn-primary" @click="saveRole" :disabled="savingRole">{{ savingRole ? 'Saving…' : 'Save' }}</button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Modal from '@/components/Modal.vue'
import { rolesApi, permissionsApi } from '@/api/admin'

const roles = ref([])
const allPermissions = ref([])
const selectedRole = ref(null)
const selectedPermIds = ref([])
const loading = ref(true)
const savingPerms = ref(false)
const showRoleModal = ref(false)
const editingRole = ref(null)
const savingRole = ref(false)
const roleForm = ref({ name: '', slug: '', description: '' })

const permGroups = computed(() => {
  const groups = {}
  allPermissions.value.forEach(p => {
    const g = p.group || 'General'
    if (!groups[g]) groups[g] = []
    groups[g].push(p)
  })
  return Object.entries(groups).map(([name, perms]) => ({ name, perms }))
})

async function fetchAll() {
  loading.value = true
  try {
    const [r, p] = await Promise.all([rolesApi.list(), permissionsApi.list()])
    roles.value = r.data.results || r.data
    allPermissions.value = p.data.results || p.data
  } finally { loading.value = false }
}

function selectRole(role) {
  selectedRole.value = role
  selectedPermIds.value = (role.permissions || []).map(p => p.id)
}

async function savePermissions() {
  savingPerms.value = true
  try {
    await rolesApi.updatePermissions(selectedRole.value.id, { permission_ids: selectedPermIds.value })
    await fetchAll()
    const updated = roles.value.find(r => r.id === selectedRole.value.id)
    if (updated) selectRole(updated)
  } catch { alert('Save failed') } finally { savingPerms.value = false }
}

function openCreateRole() { editingRole.value = null; roleForm.value = { name: '', slug: '', description: '' }; showRoleModal.value = true }
function openEditRole(role) { editingRole.value = role; roleForm.value = { name: role.name, slug: role.slug, description: role.description || '' }; showRoleModal.value = true }

async function saveRole() {
  savingRole.value = true
  try {
    if (editingRole.value) await rolesApi.update(editingRole.value.id, roleForm.value)
    else await rolesApi.create(roleForm.value)
    showRoleModal.value = false; await fetchAll()
  } catch { alert('Save failed') } finally { savingRole.value = false }
}

async function confirmDeleteRole(role) {
  if (!confirm(`Delete role "${role.name}"?`)) return
  try { await rolesApi.delete(role.id); if (selectedRole.value?.id === role.id) selectedRole.value = null; await fetchAll() } catch { alert('Delete failed') }
}

onMounted(fetchAll)
</script>

<style scoped>
.roles-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.role-card { padding: 20px; cursor: pointer; }
.role-card.selected { border-color: var(--accent-primary); box-shadow: var(--shadow-glow); }
.role-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.role-name { font-size: 1rem; font-weight: 600; }
.role-actions { display: flex; gap: 4px; }
.role-desc { font-size: 0.85rem; color: var(--text-muted); margin-bottom: 10px; }
.perm-card { padding: 24px; }
.card-title { font-size: 1rem; font-weight: 600; margin-bottom: 8px; }
.perm-group { margin-bottom: 20px; }
.perm-group-label { font-size: 0.8rem; font-weight: 600; color: var(--accent-primary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px; }
.perm-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 8px; }
.perm-toggle { display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: var(--text-secondary); cursor: pointer; padding: 6px 10px; border-radius: var(--radius-sm); transition: background var(--transition-fast); }
.perm-toggle:hover { background: var(--bg-glass); }
.perm-toggle input[type="checkbox"] { accent-color: var(--accent-primary); }
</style>
