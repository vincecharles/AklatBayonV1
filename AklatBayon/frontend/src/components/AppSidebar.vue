<template>
  <nav class="sidebar">
    <!-- Dashboard -->
    <router-link to="/dashboard" class="nav-link" :class="{ active: $route.name === 'dashboard' }">
      <i class="fas fa-tachometer-alt"></i> Dashboard
    </router-link>

    <!-- User Manage -->
    <div class="nav-dropdown">
      <a href="#" class="nav-link nav-dropdown-toggle" @click.prevent="toggle('userManage')">
        <i class="fas fa-users-cog"></i>
        <span>User Manage</span>
        <i class="fas fa-chevron-down ms-auto nav-chevron" :class="{ rotated: open.userManage }"></i>
      </a>
      <div class="nav-dropdown-items" v-show="open.userManage">
        <router-link to="/admin/users" class="nav-link nav-child-link" :class="{ active: $route.name === 'users' }">
          <i class="fas fa-user"></i> User
        </router-link>
        <router-link to="/admin/roles" class="nav-link nav-child-link" :class="{ active: $route.name === 'roles' }">
          <i class="fas fa-user-shield"></i> Role
        </router-link>
      </div>
    </div>

    <!-- Student Management -->
    <router-link to="/circulation/students" class="nav-link" :class="{ active: $route.name === 'students' }">
      <i class="fas fa-user-graduate"></i> Student Management
    </router-link>

    <!-- Catalog -->
    <div class="nav-dropdown">
      <a href="#" class="nav-link nav-dropdown-toggle" @click.prevent="toggle('catalog')">
        <i class="fas fa-book"></i>
        <span>Catalog</span>
        <i class="fas fa-chevron-down ms-auto nav-chevron" :class="{ rotated: open.catalog }"></i>
      </a>
      <div class="nav-dropdown-items" v-show="open.catalog">
        <router-link to="/books" class="nav-link nav-child-link" :class="{ active: $route.name === 'books' }">
          <i class="fas fa-book-open"></i> Books
        </router-link>
        <router-link to="/authors" class="nav-link nav-child-link" :class="{ active: $route.name === 'authors' }">
          <i class="fas fa-pen-fancy"></i> Authors
        </router-link>
        <router-link to="/publishers" class="nav-link nav-child-link" :class="{ active: $route.name === 'publishers' }">
          <i class="fas fa-building"></i> Publishers
        </router-link>
        <router-link to="/categories" class="nav-link nav-child-link" :class="{ active: $route.name === 'categories' }">
          <i class="fas fa-tags"></i> Categories
        </router-link>
      </div>
    </div>

    <!-- Circulation -->
    <div class="nav-dropdown">
      <a href="#" class="nav-link nav-dropdown-toggle" @click.prevent="toggle('circulation')">
        <i class="fas fa-exchange-alt"></i>
        <span>Circulation</span>
        <i class="fas fa-chevron-down ms-auto nav-chevron" :class="{ rotated: open.circulation }"></i>
      </a>
      <div class="nav-dropdown-items" v-show="open.circulation">
        <router-link to="/circulation/issue" class="nav-link nav-child-link" :class="{ active: $route.name === 'issue-book' }">
          <i class="fas fa-hand-holding"></i> Issue Book
        </router-link>
        <router-link to="/circulation/return" class="nav-link nav-child-link" :class="{ active: $route.name === 'return-book' }">
          <i class="fas fa-undo"></i> Return Book
        </router-link>
        <router-link to="/circulation/transactions" class="nav-link nav-child-link" :class="{ active: $route.name === 'transactions' }">
          <i class="fas fa-history"></i> Borrowing History
        </router-link>
      </div>
    </div>

    <!-- Finance -->
    <div class="nav-dropdown">
      <a href="#" class="nav-link nav-dropdown-toggle" @click.prevent="toggle('finance')">
        <i class="fas fa-money-bill-wave"></i>
        <span>Finance</span>
        <i class="fas fa-chevron-down ms-auto nav-chevron" :class="{ rotated: open.finance }"></i>
      </a>
      <div class="nav-dropdown-items" v-show="open.finance">
        <router-link to="/circulation/fines" class="nav-link nav-child-link" :class="{ active: $route.name === 'fines' }">
          <i class="fas fa-receipt"></i> Fine Manage
        </router-link>
      </div>
    </div>

    <!-- Administration -->
    <div class="nav-dropdown">
      <a href="#" class="nav-link nav-dropdown-toggle" @click.prevent="toggle('admin')">
        <i class="fas fa-chart-bar"></i>
        <span>Administration</span>
        <i class="fas fa-chevron-down ms-auto nav-chevron" :class="{ rotated: open.admin }"></i>
      </a>
      <div class="nav-dropdown-items" v-show="open.admin">
        <router-link to="/admin/reports" class="nav-link nav-child-link" :class="{ active: $route.name === 'reports' }">
          <i class="fas fa-file-alt"></i> Reports
        </router-link>
      </div>
    </div>

    <!-- System -->
    <div class="nav-dropdown">
      <a href="#" class="nav-link nav-dropdown-toggle" @click.prevent="toggle('system')">
        <i class="fas fa-cog"></i>
        <span>System</span>
        <i class="fas fa-chevron-down ms-auto nav-chevron" :class="{ rotated: open.system }"></i>
      </a>
      <div class="nav-dropdown-items" v-show="open.system">
        <router-link to="/admin/settings" class="nav-link nav-child-link" :class="{ active: $route.name === 'settings' }">
          <i class="fas fa-sliders-h"></i> Settings
        </router-link>
        <router-link to="/admin/audit-logs" class="nav-link nav-child-link" :class="{ active: $route.name === 'audit-logs' }">
          <i class="fas fa-clipboard-list"></i> Audit Logs
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { reactive, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const open = reactive({
  userManage: false,
  catalog: false,
  circulation: false,
  finance: false,
  admin: false,
  system: false,
})

function toggle(group) {
  open[group] = !open[group]
}

// Auto-open the dropdown containing the active route
watch(() => route.name, (name) => {
  if (['users', 'roles'].includes(name)) open.userManage = true
  if (['books', 'book-detail', 'authors', 'publishers', 'categories'].includes(name)) open.catalog = true
  if (['issue-book', 'return-book', 'transactions'].includes(name)) open.circulation = true
  if (['fines'].includes(name)) open.finance = true
  if (['reports'].includes(name)) open.admin = true
  if (['settings', 'audit-logs'].includes(name)) open.system = true
}, { immediate: true })
</script>

<style scoped>
.sidebar {
  width: 260px;
  background-color: #1a1a2e;
  position: fixed;
  top: 60px;
  left: 0;
  bottom: 0;
  overflow-y: auto;
  z-index: 1020;
  padding-top: 8px;
}
.sidebar::-webkit-scrollbar { width: 4px; }
.sidebar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 4px; }

.nav-link {
  color: rgba(255,255,255,0.75);
  padding: 12px 24px;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.2s;
  text-decoration: none;
  border-left: 3px solid transparent;
  cursor: pointer;
}
.nav-link:hover {
  background-color: rgba(255,255,255,0.08);
  color: #fff;
}
.nav-link.active {
  background-color: #e94560;
  color: #fff;
  border-left-color: #fff;
}
.nav-link i {
  width: 20px;
  text-align: center;
  font-size: 15px;
}

.nav-dropdown-toggle {
  cursor: pointer;
}
.nav-dropdown-toggle .ms-auto {
  margin-left: auto;
}
.nav-chevron {
  font-size: 11px;
  transition: transform 0.25s ease;
}
.nav-chevron.rotated {
  transform: rotate(180deg);
}

.nav-dropdown-items {
  background: rgba(0,0,0,0.15);
}
.nav-dropdown-items .nav-link {
  padding-left: 48px;
  font-size: 13px;
}
.nav-child-link i {
  font-size: 10px;
}

@media (max-width: 768px) {
  .sidebar { display: none; }
}
</style>
