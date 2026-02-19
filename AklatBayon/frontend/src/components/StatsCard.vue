<template>
  <div class="stat-card" :style="{ '--card-color': color }">
    <div class="stat-icon" :style="{ background: color + '20', color: color }">
      {{ icon }}
    </div>
    <div class="stat-value">{{ displayValue }}</div>
    <div class="stat-label">{{ label }}</div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  icon: { type: String, default: '📊' },
  value: { type: [Number, String], default: 0 },
  label: { type: String, default: '' },
  color: { type: String, default: '#6366f1' },
})

const displayValue = ref(0)

function animateCount(target) {
  const num = Number(target)
  if (isNaN(num)) { displayValue.value = target; return }
  const duration = 600
  const startTime = performance.now()
  const startVal = 0
  function step(now) {
    const progress = Math.min((now - startTime) / duration, 1)
    const eased = 1 - Math.pow(1 - progress, 3)
    displayValue.value = Math.round(startVal + (num - startVal) * eased)
    if (progress < 1) requestAnimationFrame(step)
  }
  requestAnimationFrame(step)
}

onMounted(() => animateCount(props.value))
watch(() => props.value, (v) => animateCount(v))
</script>
