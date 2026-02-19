import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  /* ── Public ── */
  { path: '/', name: 'landing', component: () => import('@/views/LandingPage.vue') },
  { path: '/catalog', name: 'catalog', component: () => import('@/views/PublicCatalogView.vue') },
  { path: '/login', name: 'login', component: () => import('@/views/LoginView.vue') },

  /* ── Authenticated ── */
  { path: '/dashboard', name: 'dashboard', meta: { requiresAuth: true }, component: () => import('@/views/DashboardView.vue') },

  // User Management
  { path: '/admin/users', name: 'users', meta: { requiresAuth: true }, component: () => import('@/views/admin/UsersView.vue') },
  { path: '/admin/roles', name: 'roles', meta: { requiresAuth: true }, component: () => import('@/views/admin/RolesPermissionsView.vue') },

  // Student Management
  { path: '/circulation/students', name: 'students', meta: { requiresAuth: true }, component: () => import('@/views/circulation/StudentsView.vue') },

  // Catalog
  { path: '/books', name: 'books', meta: { requiresAuth: true }, component: () => import('@/views/books/BooksView.vue') },
  { path: '/books/:id', name: 'book-detail', meta: { requiresAuth: true }, component: () => import('@/views/books/BookDetailView.vue') },
  { path: '/authors', name: 'authors', meta: { requiresAuth: true }, component: () => import('@/views/books/AuthorsView.vue') },
  { path: '/publishers', name: 'publishers', meta: { requiresAuth: true }, component: () => import('@/views/books/PublishersView.vue') },
  { path: '/categories', name: 'categories', meta: { requiresAuth: true }, component: () => import('@/views/books/CategoriesView.vue') },

  // Circulation
  { path: '/circulation/issue', name: 'issue-book', meta: { requiresAuth: true }, component: () => import('@/views/circulation/IssueBookView.vue') },
  { path: '/circulation/return', name: 'return-book', meta: { requiresAuth: true }, component: () => import('@/views/circulation/ReturnBookView.vue') },
  { path: '/circulation/transactions', name: 'transactions', meta: { requiresAuth: true }, component: () => import('@/views/circulation/TransactionHistoryView.vue') },

  // Finance
  { path: '/circulation/fines', name: 'fines', meta: { requiresAuth: true }, component: () => import('@/views/circulation/FinesView.vue') },

  // Administration
  { path: '/admin/reports', name: 'reports', meta: { requiresAuth: true }, component: () => import('@/views/admin/ReportsView.vue') },

  // System
  { path: '/admin/settings', name: 'settings', meta: { requiresAuth: true }, component: () => import('@/views/admin/SettingsView.vue') },
  { path: '/admin/audit-logs', name: 'audit-logs', meta: { requiresAuth: true }, component: () => import('@/views/admin/AuditLogsView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.name === 'login' && auth.isAuthenticated) {
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router
