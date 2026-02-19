<template>
  <div class="dashboard">
    <div class="page-header">
      <h1 class="page-title">Dashboard</h1>
      <span class="text-muted" style="font-size:0.85rem">Welcome back, {{ authStore.fullName }}</span>
    </div>

    <div v-if="loading" class="loading-center"><div class="spinner"></div></div>

    <template v-else>
      <div class="stats-grid">
        <StatsCard icon="📖" :value="stats.total_books ?? 0" label="Total Books" color="#6366f1" />
        <StatsCard icon="📤" :value="stats.active_loans ?? 0" label="Active Loans" color="#06b6d4" />
        <StatsCard icon="⏰" :value="stats.overdue ?? 0" label="Overdue" color="#ef4444" />
        <StatsCard icon="💰" :value="stats.pending_fines ?? 0" label="Pending Fines" color="#f59e0b" />
        <StatsCard icon="🎓" :value="stats.total_students ?? 0" label="Students" color="#10b981" />
        <StatsCard icon="📋" :value="stats.total_transactions ?? 0" label="Transactions" color="#8b5cf6" />
      </div>

      <div class="dashboard-grid">
        <div class="glass-card quick-actions-card">
          <h3 class="card-title">Quick Actions</h3>
          <div class="quick-actions">
            <router-link to="/circulation/issue" class="quick-action-btn">
              <span>📤</span> Issue Book
            </router-link>
            <router-link to="/circulation/return" class="quick-action-btn">
              <span>📥</span> Return Book
            </router-link>
            <router-link to="/students" class="quick-action-btn">
              <span>🎓</span> Students
            </router-link>
            <router-link to="/books" class="quick-action-btn">
              <span>📖</span> Books
            </router-link>
            <router-link to="/reports" class="quick-action-btn">
              <span>📈</span> Reports
            </router-link>
            <router-link to="/fines" class="quick-action-btn">
              <span>💰</span> Fines
            </router-link>
          </div>
        </div>

        <div class="glass-card recent-card">
          <h3 class="card-title">Recent Activity</h3>
          <div v-if="stats.recent_activity && stats.recent_activity.length > 0" class="activity-list">
            <div v-for="item in stats.recent_activity" :key="item.id" class="activity-item">
              <div class="activity-dot"></div>
              <div class="activity-content">
                <span class="activity-text">{{ item.description || item.action }}</span>
                <span class="activity-time">{{ item.created_at }}</span>
              </div>
            </div>
          </div>
          <div v-else class="empty-state" style="padding: 30px">
            <div class="empty-icon" style="font-size:2rem">📭</div>
            <div class="empty-title">No recent activity</div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { dashboardApi } from '@/api/admin'
import StatsCard from '@/components/StatsCard.vue'

const authStore = useAuthStore()
const stats = ref({})
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await dashboardApi.get()
    stats.value = data
  } catch (e) {
    console.error('Failed to load dashboard:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--text-heading);
}

.quick-actions-card, .recent-card {
  padding: 24px;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.quick-action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 8px;
  background: var(--bg-glass);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: 0.8rem;
  font-weight: 500;
  text-decoration: none;
  transition: all var(--transition-base);
}
.quick-action-btn span { font-size: 1.5rem; }
.quick-action-btn:hover {
  background: var(--bg-glass-hover);
  color: var(--text-primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow);
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.activity-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent-primary);
  margin-top: 6px;
  flex-shrink: 0;
}

.activity-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.activity-text { font-size: 0.85rem; color: var(--text-secondary); }
.activity-time { font-size: 0.75rem; color: var(--text-muted); }

@media (max-width: 1024px) {
  .dashboard-grid { grid-template-columns: 1fr; }
  .quick-actions { grid-template-columns: repeat(2, 1fr); }
}
</style>
