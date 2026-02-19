<template>
  <div class="app-root">
    <!-- Authenticated layout: top header + sidebar + content -->
    <template v-if="showLayout">
      <AppTopbar />
      <AppSidebar />
      <main class="main-content">
        <router-view />
      </main>
    </template>

    <!-- Public / Login layout (no sidebar) -->
    <template v-else>
      <router-view />
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppSidebar from '@/components/AppSidebar.vue'
import AppTopbar from '@/components/AppTopbar.vue'

const route = useRoute()

const publicRoutes = ['landing', 'catalog', 'login']
const showLayout = computed(() => !publicRoutes.includes(route.name))
</script>

<style scoped>
.main-content {
  margin-left: 260px;
  margin-top: 60px;
  padding: 24px;
  min-height: calc(100vh - 60px);
  background: var(--bg-primary);
}

@media (max-width: 768px) {
  .main-content { margin-left: 0; }
}
</style>
