<template>
  <div class="catalog-page">
    <!-- Nav -->
    <nav class="catalog-nav">
      <div class="nav-brand">
        <span class="nav-logo">📚</span>
        <span class="nav-name">AklatBayon</span>
      </div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/login" class="btn btn-primary btn-sm">Sign In</router-link>
      </div>
    </nav>

    <div class="catalog-content">
      <div class="catalog-header">
        <h1 class="page-title">Public Catalog</h1>
        <p class="text-muted">Browse our entire book collection</p>
      </div>

      <div class="toolbar">
        <div class="search-wrapper" style="max-width:500px">
          <span class="search-icon">🔍</span>
          <input v-model="search" class="search-input" placeholder="Search by title, author, ISBN..." @input="debouncedFetch" />
        </div>
        <select v-model="categoryFilter" class="form-select" style="width:auto;min-width:160px" @change="fetchCatalog">
          <option value="">All Categories</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </div>

      <div v-if="loading" class="loading-center"><div class="spinner"></div></div>

      <div v-else-if="books.length === 0" class="empty-state" style="padding:60px">
        <div class="empty-icon">📭</div>
        <div class="empty-title">No books found</div>
        <div class="empty-desc">Try a different search or category.</div>
      </div>

      <div v-else class="catalog-grid">
        <div v-for="book in books" :key="book.id" class="glass-card book-card">
          <div class="book-cover">📖</div>
          <div class="book-info">
            <h3 class="book-title">{{ book.title }}</h3>
            <p class="book-author">{{ book.author_name || 'Unknown Author' }}</p>
            <div class="book-meta">
              <span v-if="book.category_name" class="badge badge-info">{{ book.category_name }}</span>
              <span class="badge" :class="book.available_copies > 0 ? 'badge-success' : 'badge-danger'">
                {{ book.available_copies > 0 ? `${book.available_copies} available` : 'Unavailable' }}
              </span>
            </div>
            <p v-if="book.isbn" class="book-isbn">ISBN: {{ book.isbn }}</p>
          </div>
        </div>
      </div>
    </div>

    <footer class="catalog-footer">
      <p>© 2026 AklatBayon · Library Management System</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { catalogApi, categoriesApi } from '@/api/books'

const books = ref([])
const categories = ref([])
const loading = ref(true)
const search = ref('')
const categoryFilter = ref('')

let debounceTimer = null

function flattenCats(cats, result = []) {
  cats.forEach(c => {
    result.push({ id: c.id, name: c.name })
    if (c.children?.length) flattenCats(c.children, result)
  })
  return result
}

async function fetchCatalog() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    if (categoryFilter.value) params.category = categoryFilter.value
    const { data } = await catalogApi.list(params)
    books.value = data.results || data
  } finally { loading.value = false }
}

function debouncedFetch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(fetchCatalog, 300)
}

onMounted(async () => {
  try {
    const { data } = await categoriesApi.list()
    categories.value = flattenCats(data.results || data)
  } catch { /* categories may require auth, ok to fail silently */ }
  await fetchCatalog()
})
</script>

<style scoped>
.catalog-page { min-height: 100vh; background: var(--bg-primary); }

.catalog-nav {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 40px;
  border-bottom: 1px solid var(--border-color);
  background: rgba(10, 14, 23, 0.8);
  backdrop-filter: blur(12px);
  position: sticky; top: 0; z-index: 10;
}
.nav-brand { display: flex; align-items: center; gap: 10px; }
.nav-logo { font-size: 1.5rem; }
.nav-name { font-size: 1.15rem; font-weight: 700; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.nav-links { display: flex; align-items: center; gap: 20px; }
.nav-link { color: var(--text-secondary); font-size: 0.9rem; font-weight: 500; }
.nav-link:hover { color: var(--text-primary); }

.catalog-content { padding: 40px; max-width: 1200px; margin: 0 auto; }
.catalog-header { margin-bottom: 28px; }

.catalog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.book-card { padding: 20px; display: flex; gap: 16px; }
.book-cover {
  width: 60px; height: 80px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  background: var(--gradient-card); border-radius: var(--radius-sm);
  font-size: 2rem;
}
.book-info { flex: 1; min-width: 0; }
.book-title { font-size: 0.95rem; font-weight: 600; margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.book-author { font-size: 0.8rem; color: var(--text-muted); margin-bottom: 8px; }
.book-meta { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 6px; }
.book-isbn { font-size: 0.75rem; color: var(--text-muted); font-family: monospace; }

.catalog-footer { padding: 32px; text-align: center; color: var(--text-muted); font-size: 0.8rem; border-top: 1px solid var(--border-color); }

@media (max-width: 768px) {
  .catalog-content { padding: 20px; }
  .catalog-nav { padding: 12px 20px; }
}
</style>
