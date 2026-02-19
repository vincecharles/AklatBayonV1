<template>
  <header class="top-header">
    <div class="logo">
      <i class="fas fa-book-open"></i>
      <span>AklatBayon</span>
    </div>
    <div class="user-info">
      <!-- Theme Toggle -->
      <button class="btn-theme" @click="themeStore.toggle" :title="themeStore.isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'">
        <i :class="themeStore.isDark ? 'fas fa-sun' : 'fas fa-moon'"></i>
      </button>
      <div class="text-end">
        <div class="user-name">{{ user?.first_name || user?.username || 'User' }} {{ user?.last_name || '' }}</div>
        <div class="user-role">{{ user?.role_detail?.name || user?.user_type || 'User' }}</div>
      </div>
      <button class="btn-logout" @click="handleLogout">
        <i class="fas fa-sign-out-alt"></i> Logout
      </button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'

const authStore = useAuthStore()
const themeStore = useThemeStore()
const router = useRouter()
const user = computed(() => authStore.user)

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.top-header {
  background-color: #1a1a2e;
  color: #fff;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1030;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: 700;
}
.logo i {
  font-size: 24px;
  color: #e94560;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 16px;
}
.user-name {
  font-size: 14px;
}
.user-role {
  font-size: 11px;
  color: rgba(255,255,255,0.7);
}
.text-end {
  text-align: right;
}

/* Theme Toggle Button */
.btn-theme {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.2);
  background: rgba(255,255,255,0.08);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  transition: all 0.3s ease;
}
.btn-theme:hover {
  background: rgba(255,255,255,0.15);
  border-color: rgba(255,255,255,0.4);
  transform: rotate(20deg);
}
.btn-theme i {
  transition: transform 0.3s ease;
}

.btn-logout {
  color: #fff;
  background: #e94560;
  border: none;
  padding: 6px 16px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: background 0.2s;
}
.btn-logout:hover {
  background: #d63851;
}
</style>
