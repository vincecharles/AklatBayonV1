<template>
  <div class="login-page">
    <div class="login-bg">
      <div class="bg-orb bg-orb-1"></div>
      <div class="bg-orb bg-orb-2"></div>
      <div class="bg-orb bg-orb-3"></div>
    </div>

    <div class="login-container fade-in-up">
      <div class="login-card glass-card">
        <div class="login-header">
          <span class="login-logo">📚</span>
          <h1 class="login-title">AklatBayon</h1>
          <p class="login-subtitle">Library Management System</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div v-if="error" class="alert alert-error">⚠️ {{ error }}</div>

          <div class="form-group">
            <label class="form-label" for="username">Username</label>
            <input
              id="username"
              v-model="username"
              type="text"
              class="form-input"
              placeholder="Enter your username"
              required
              autofocus
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="password">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              class="form-input"
              placeholder="Enter your password"
              required
            />
          </div>

          <button type="submit" class="btn btn-primary btn-lg w-full" :disabled="loading">
            <span v-if="loading" class="spinner" style="width:18px;height:18px;border-width:2px;"></span>
            {{ loading ? 'Signing in…' : 'Sign In' }}
          </button>
        </form>

        <div class="login-footer">
          <router-link to="/">← Back to home</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await authStore.login(username.value, password.value)
    const redirect = route.query.redirect || '/dashboard'
    router.push(redirect)
  } catch (err) {
    error.value = err.response?.data?.non_field_errors?.[0]
      || err.response?.data?.detail
      || 'Invalid credentials. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  background: var(--bg-primary);
  padding: 20px;
}

.login-bg {
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.3;
}
.bg-orb-1 {
  width: 500px; height: 500px;
  background: #6366f1;
  top: -10%; left: -10%;
  animation: float 8s ease-in-out infinite;
}
.bg-orb-2 {
  width: 400px; height: 400px;
  background: #8b5cf6;
  bottom: -10%; right: -10%;
  animation: float 10s ease-in-out infinite reverse;
}
.bg-orb-3 {
  width: 300px; height: 300px;
  background: #06b6d4;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  animation: float 12s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  33% { transform: translate(30px, -20px); }
  66% { transform: translate(-20px, 20px); }
}

.login-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 420px;
}

.login-card {
  padding: 40px 32px;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}
.login-logo { font-size: 3rem; display: block; margin-bottom: 12px; }
.login-title {
  font-size: 1.8rem;
  font-weight: 800;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.login-subtitle { color: var(--text-muted); font-size: 0.9rem; margin-top: 4px; }

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.login-footer {
  margin-top: 24px;
  text-align: center;
  font-size: 0.85rem;
}

.w-full { width: 100%; }
</style>
