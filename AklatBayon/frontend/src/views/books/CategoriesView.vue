<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Categories</h1>
      <button class="btn btn-primary" @click="openCreate">+ Add Category</button>
    </div>

    <div v-if="loading" class="loading-center"><div class="spinner"></div></div>

    <div v-else class="glass-card" style="padding:24px">
      <div v-if="categories.length === 0" class="empty-state">
        <div class="empty-icon">📭</div>
        <div class="empty-title">No categories yet</div>
      </div>
      <div v-else class="category-tree">
        <CategoryNode
          v-for="cat in categories"
          :key="cat.id"
          :category="cat"
          :depth="0"
          @edit="openEdit"
          @delete="confirmDelete"
        />
      </div>
    </div>

    <Modal v-model="showModal" :title="editing ? 'Edit Category' : 'Add Category'">
      <form @submit.prevent="save" class="flex flex-col gap-md">
        <div class="form-group">
          <label class="form-label">Name</label>
          <input v-model="form.name" class="form-input" required />
        </div>
        <div class="form-group">
          <label class="form-label">Parent Category</label>
          <select v-model="form.parent" class="form-select">
            <option :value="null">None (Top Level)</option>
            <option v-for="c in flatCategories" :key="c.id" :value="c.id">{{ c.prefix }}{{ c.name }}</option>
          </select>
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
import { ref, computed, onMounted, defineComponent, h } from 'vue'
import Modal from '@/components/Modal.vue'
import { categoriesApi } from '@/api/books'

const categories = ref([])
const loading = ref(true)
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)
const form = ref({ name: '', parent: null })

async function fetchItems() {
  loading.value = true
  try { const { data } = await categoriesApi.list(); categories.value = data.results || data }
  finally { loading.value = false }
}

const flatCategories = computed(() => {
  const result = []
  function flatten(cats, depth = 0) {
    cats.forEach(c => {
      result.push({ id: c.id, name: c.name, prefix: '— '.repeat(depth) })
      if (c.children?.length) flatten(c.children, depth + 1)
    })
  }
  flatten(categories.value)
  return result
})

function openCreate() { editing.value = null; form.value = { name: '', parent: null }; showModal.value = true }
function openEdit(cat) { editing.value = cat; form.value = { name: cat.name, parent: cat.parent }; showModal.value = true }

async function save() {
  saving.value = true
  try {
    if (editing.value) await categoriesApi.update(editing.value.id, form.value)
    else await categoriesApi.create(form.value)
    showModal.value = false; await fetchItems()
  } catch { alert('Save failed') } finally { saving.value = false }
}

async function confirmDelete(cat) {
  if (!confirm(`Delete "${cat.name}"?`)) return
  try { await categoriesApi.delete(cat.id); await fetchItems() } catch { alert('Delete failed') }
}

onMounted(fetchItems)

const CategoryNode = defineComponent({
  name: 'CategoryNode',
  props: { category: Object, depth: Number },
  emits: ['edit', 'delete'],
  setup(props, { emit }) {
    const expanded = ref(true)
    return () => h('div', { class: 'tree-node' }, [
      h('div', {
        class: 'tree-item',
        style: { paddingLeft: (props.depth * 24 + 12) + 'px' }
      }, [
        props.category.children?.length
          ? h('button', {
              class: 'tree-toggle',
              onClick: () => { expanded.value = !expanded.value }
            }, expanded.value ? '▾' : '▸')
          : h('span', { class: 'tree-toggle', style: 'visibility:hidden' }, '▸'),
        h('span', { class: 'tree-name' }, props.category.name),
        h('div', { class: 'tree-actions' }, [
          h('button', { class: 'btn btn-ghost btn-sm', onClick: () => emit('edit', props.category) }, '✏️'),
          h('button', { class: 'btn btn-ghost btn-sm', onClick: () => emit('delete', props.category) }, '🗑️'),
        ])
      ]),
      expanded.value && props.category.children?.length
        ? h('div', { class: 'tree-children' },
            props.category.children.map(child =>
              h(CategoryNode, {
                key: child.id,
                category: child,
                depth: props.depth + 1,
                onEdit: (c) => emit('edit', c),
                onDelete: (c) => emit('delete', c),
              })
            )
          )
        : null
    ])
  }
})
</script>

<style scoped>
.category-tree { }
.tree-node { }
.tree-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  transition: background var(--transition-fast);
}
.tree-item:hover { background: var(--bg-glass); }
.tree-toggle {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 0.9rem;
  flex-shrink: 0;
}
.tree-name { flex: 1; font-size: 0.9rem; color: var(--text-primary); }
.tree-actions { display: flex; gap: 4px; opacity: 0; transition: opacity var(--transition-fast); }
.tree-item:hover .tree-actions { opacity: 1; }
</style>
