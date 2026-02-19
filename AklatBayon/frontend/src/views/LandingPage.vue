<template>
  <div class="landing-root" :class="timeClass">
    <!-- Background Particles -->
    <div class="particles" ref="particlesEl"></div>

    <!-- Status Bar -->
    <div class="status-bar">
      <div class="system-status">
        <div class="status-dot"></div>
        SYSTEM ONLINE
      </div>
      <div style="text-align:right">
        <div class="clock">{{ clockText }}</div>
        <div class="station-label">FEATI-LMS STATION 01</div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Logo with Scanning Animation -->
      <div class="logo-container">
        <div class="scan-ring"></div>
        <div class="scan-ring"></div>
        <div class="scan-ring"></div>
        <div class="logo-glow"></div>
        <div class="scan-line"></div>
        <img src="/images/logo.png" alt="FEATI University Logo" />
      </div>

      <!-- Guest view -->
      <h1 class="main-title">FEATI-LMS</h1>
      <h2 class="sub-title">AKLATBAYON</h2>

      <div class="instruction-text">
        <i class="fas fa-book-reader"></i>
        Welcome to FEATI University Library
      </div>

      <router-link to="/login" class="auth-btn">
        <div class="icon-circle">
          <i class="fas fa-sign-in-alt"></i>
        </div>
        <span>Login</span>
      </router-link>
    </div>

    <!-- Time-of-day indicator -->
    <div class="time-indicator">
      <i :class="timeIcon"></i>
      <span>{{ timeLabel }}</span>
    </div>

    <!-- Welcome Toast -->
    <div class="welcome-toast" v-if="showToast">
      <div class="toast-icon">
        <i class="fas fa-check-circle"></i>
      </div>
      <div class="toast-content">
        <div class="toast-label">SYSTEM READY</div>
        <div class="toast-title">Welcome to FEATI-LMS</div>
        <div class="toast-detail">System <span class="text-green">ONLINE</span> — {{ currentTime }}</div>
      </div>
      <div class="toast-avatar">
        <i class="fas fa-university"></i>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const clockText = ref('')
const currentTime = ref('')
const showToast = ref(true)
const particlesEl = ref(null)
const hour = ref(new Date().getHours())

// Time-of-day class
const timeClass = computed(() => {
  const h = hour.value
  if (h >= 5 && h < 7) return 'time-dawn'
  if (h >= 7 && h < 12) return 'time-morning'
  if (h >= 12 && h < 17) return 'time-afternoon'
  if (h >= 17 && h < 19) return 'time-dusk'
  return 'time-night'
})

const timeIcon = computed(() => {
  const h = hour.value
  if (h >= 5 && h < 7) return 'fas fa-cloud-sun'
  if (h >= 7 && h < 17) return 'fas fa-sun'
  if (h >= 17 && h < 19) return 'fas fa-cloud-sun'
  return 'fas fa-moon'
})

const timeLabel = computed(() => {
  const h = hour.value
  if (h >= 5 && h < 7) return 'Dawn'
  if (h >= 7 && h < 12) return 'Morning'
  if (h >= 12 && h < 17) return 'Afternoon'
  if (h >= 17 && h < 19) return 'Dusk'
  return 'Night'
})

function updateClock() {
  const now = new Date()
  let h = now.getHours()
  const m = String(now.getMinutes()).padStart(2, '0')
  const s = String(now.getSeconds()).padStart(2, '0')
  const ampm = h >= 12 ? 'PM' : 'AM'
  h = h % 12 || 12
  clockText.value = `${h}:${m}:${s} ${ampm}`
  currentTime.value = `${h}:${m} ${ampm}`
  hour.value = now.getHours()
}

function generateParticles() {
  if (!particlesEl.value) return
  for (let i = 0; i < 30; i++) {
    const p = document.createElement('div')
    p.className = 'particle'
    p.style.left = Math.random() * 100 + '%'
    p.style.animationDuration = (8 + Math.random() * 12) + 's'
    p.style.animationDelay = Math.random() * 10 + 's'
    p.style.width = p.style.height = (1 + Math.random() * 3) + 'px'
    particlesEl.value.appendChild(p)
  }
}

let clockInterval = null

onMounted(() => {
  updateClock()
  clockInterval = setInterval(updateClock, 1000)
  generateParticles()

  // hide toast after 5s
  setTimeout(() => { showToast.value = false }, 5000)
})

onUnmounted(() => {
  clearInterval(clockInterval)
})
</script>

<style scoped>
.landing-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  color: #ffffff;
  font-family: 'Segoe UI', Arial, sans-serif;
  transition: background 1s ease;
  position: relative;
}

/* ── Time-of-day backgrounds ── */
.time-night { background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 50%, #0f3460 100%); }
.time-dawn { background: linear-gradient(135deg, #1a1a2e 0%, #2d1b4e 30%, #e07040 70%, #f4a460 100%); }
.time-morning { background: linear-gradient(135deg, #1565c0 0%, #42a5f5 50%, #90caf9 100%); }
.time-afternoon { background: linear-gradient(135deg, #0d47a1 0%, #1976d2 50%, #64b5f6 100%); }
.time-dusk { background: linear-gradient(135deg, #1a1a2e 0%, #4a1942 30%, #c0392b 70%, #e67e22 100%); }

/* ── Time-aware font colors ── */
/* Dawn */
.time-dawn .main-title, .time-dawn .sub-title { color: #fff3e0; text-shadow: 0 0 30px rgba(244,164,96,0.4); }
.time-dawn .system-status { color: rgba(255,243,224,0.8); }
.time-dawn .clock { color: #fff3e0; }
.time-dawn .station-label { color: rgba(255,243,224,0.6); }
.time-dawn .instruction-text { color: rgba(255,243,224,0.7); }
.time-dawn .auth-btn { color: rgba(255,243,224,0.9); }
.time-dawn .auth-btn .icon-circle { border-color: rgba(255,243,224,0.6); background: rgba(255,243,224,0.1); }
.time-dawn .auth-btn .icon-circle i { color: #fff3e0; }
.time-dawn .auth-btn:hover .icon-circle { border-color: #fff3e0; background: rgba(255,243,224,0.2); box-shadow: 0 0 25px rgba(244,164,96,0.3); }
.time-dawn .time-indicator { color: rgba(255,243,224,0.5); }
.time-dawn .scan-ring { border-color: rgba(255,243,224,0.4) !important; }
.time-dawn .scan-line { background: linear-gradient(90deg, transparent, rgba(255,243,224,0.8), transparent) !important; box-shadow: 0 0 15px rgba(244,164,96,0.5) !important; }
.time-dawn .logo-glow { background: radial-gradient(circle, rgba(244,164,96,0.15) 0%, transparent 70%) !important; }
.time-dawn .logo-container img { filter: drop-shadow(0 0 20px rgba(244,164,96,0.3)); }

/* Morning */
.time-morning .main-title, .time-morning .sub-title { color: #0d2137; text-shadow: 0 0 30px rgba(13,33,55,0.2); }
.time-morning .system-status { color: rgba(13,33,55,0.7); }
.time-morning .status-dot { background-color: #1b5e20 !important; }
.time-morning .clock { color: #0d2137; }
.time-morning .station-label { color: rgba(13,33,55,0.5); }
.time-morning .instruction-text { color: rgba(13,33,55,0.6); }
.time-morning .auth-btn { color: rgba(13,33,55,0.8); }
.time-morning .auth-btn .icon-circle { border-color: rgba(13,33,55,0.5); background: rgba(13,33,55,0.08); }
.time-morning .auth-btn .icon-circle i { color: #0d2137; }
.time-morning .auth-btn:hover .icon-circle { border-color: #0d2137; background: rgba(13,33,55,0.15); box-shadow: 0 0 25px rgba(13,33,55,0.2); }
.time-morning .time-indicator { color: rgba(13,33,55,0.5); }
.time-morning .scan-ring { border-color: rgba(13,33,55,0.3) !important; }
.time-morning .scan-line { background: linear-gradient(90deg, transparent, rgba(13,33,55,0.6), transparent) !important; box-shadow: 0 0 15px rgba(13,33,55,0.3) !important; }
.time-morning .logo-glow { background: radial-gradient(circle, rgba(13,33,55,0.1) 0%, transparent 70%) !important; }
.time-morning .logo-container img { filter: drop-shadow(0 0 20px rgba(13,33,55,0.2)); }
.time-morning .particle { background: rgba(255,255,255,0.25) !important; }
.time-morning .welcome-toast { background: rgba(144,202,249,0.9) !important; border-color: rgba(27,94,32,0.5) !important; }
.time-morning .toast-title { color: #0d2137 !important; }
.time-morning .toast-detail { color: rgba(13,33,55,0.5) !important; }

/* Afternoon */
.time-afternoon .main-title, .time-afternoon .sub-title { color: #e3f2fd; text-shadow: 0 0 30px rgba(227,242,253,0.3); }
.time-afternoon .system-status { color: rgba(227,242,253,0.8); }
.time-afternoon .clock { color: #e3f2fd; }
.time-afternoon .station-label { color: rgba(227,242,253,0.5); }
.time-afternoon .instruction-text { color: rgba(227,242,253,0.7); }
.time-afternoon .auth-btn { color: rgba(227,242,253,0.9); }
.time-afternoon .auth-btn .icon-circle { border-color: rgba(227,242,253,0.6); background: rgba(227,242,253,0.1); }
.time-afternoon .auth-btn .icon-circle i { color: #e3f2fd; }
.time-afternoon .auth-btn:hover .icon-circle { border-color: #e3f2fd; background: rgba(227,242,253,0.2); box-shadow: 0 0 25px rgba(100,181,246,0.3); }
.time-afternoon .time-indicator { color: rgba(227,242,253,0.5); }
.time-afternoon .scan-ring { border-color: rgba(227,242,253,0.4) !important; }
.time-afternoon .scan-line { background: linear-gradient(90deg, transparent, rgba(227,242,253,0.8), transparent) !important; box-shadow: 0 0 15px rgba(100,181,246,0.5) !important; }
.time-afternoon .logo-glow { background: radial-gradient(circle, rgba(100,181,246,0.15) 0%, transparent 70%) !important; }
.time-afternoon .logo-container img { filter: drop-shadow(0 0 20px rgba(100,181,246,0.3)); }
.time-afternoon .particle { background: rgba(255,255,255,0.25) !important; }

/* Dusk */
.time-dusk .main-title, .time-dusk .sub-title { color: #ffecd2; text-shadow: 0 0 30px rgba(230,126,34,0.4); }
.time-dusk .system-status { color: rgba(255,236,210,0.8); }
.time-dusk .clock { color: #ffecd2; }
.time-dusk .station-label { color: rgba(255,236,210,0.6); }
.time-dusk .instruction-text { color: rgba(255,236,210,0.7); }
.time-dusk .auth-btn { color: rgba(255,236,210,0.9); }
.time-dusk .auth-btn .icon-circle { border-color: rgba(255,236,210,0.6); background: rgba(255,236,210,0.1); }
.time-dusk .auth-btn .icon-circle i { color: #ffecd2; }
.time-dusk .auth-btn:hover .icon-circle { border-color: #ffecd2; background: rgba(255,236,210,0.2); box-shadow: 0 0 25px rgba(230,126,34,0.3); }
.time-dusk .time-indicator { color: rgba(255,236,210,0.5); }
.time-dusk .scan-ring { border-color: rgba(255,236,210,0.4) !important; }
.time-dusk .scan-line { background: linear-gradient(90deg, transparent, rgba(255,236,210,0.8), transparent) !important; box-shadow: 0 0 15px rgba(230,126,34,0.5) !important; }
.time-dusk .logo-glow { background: radial-gradient(circle, rgba(230,126,34,0.15) 0%, transparent 70%) !important; }
.time-dusk .logo-container img { filter: drop-shadow(0 0 20px rgba(230,126,34,0.3)); }

/* Night */
.time-night .main-title, .time-night .sub-title { color: #e0e6f0; text-shadow: 0 0 30px rgba(224,230,240,0.2); }
.time-night .system-status { color: rgba(224,230,240,0.7); }
.time-night .clock { color: #e0e6f0; }
.time-night .station-label { color: rgba(224,230,240,0.5); }
.time-night .instruction-text { color: rgba(224,230,240,0.6); }
.time-night .auth-btn { color: rgba(224,230,240,0.8); }
.time-night .auth-btn .icon-circle { border-color: rgba(224,230,240,0.4); background: rgba(224,230,240,0.08); }
.time-night .auth-btn .icon-circle i { color: #e0e6f0; }
.time-night .auth-btn:hover { color: #ffffff; }
.time-night .auth-btn:hover .icon-circle { border-color: #e0e6f0; background: rgba(224,230,240,0.15); box-shadow: 0 0 25px rgba(224,230,240,0.15); }
.time-night .time-indicator { color: rgba(224,230,240,0.4); }
.time-night .scan-ring { border-color: rgba(224,230,240,0.3) !important; }
.time-night .scan-line { background: linear-gradient(90deg, transparent, rgba(224,230,240,0.7), transparent) !important; box-shadow: 0 0 15px rgba(224,230,240,0.3) !important; }
.time-night .logo-glow { background: radial-gradient(circle, rgba(224,230,240,0.1) 0%, transparent 70%) !important; }
.time-night .logo-container img { filter: drop-shadow(0 0 20px rgba(224,230,240,0.2)); }

/* ── Status Bar ── */
.status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 32px;
  position: absolute;
  top: 0; left: 0; right: 0;
  z-index: 10;
}

.system-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: rgba(255,255,255,0.7);
}

.status-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background-color: #28a745;
  animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.clock {
  font-size: 24px;
  font-weight: 700;
  letter-spacing: 1px;
  color: rgba(255,255,255,0.9);
}

.station-label {
  font-size: 11px;
  color: rgba(255,255,255,0.5);
  letter-spacing: 1px;
  text-align: right;
}

/* ── Main Content ── */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 1;
}

/* ── Logo Container ── */
.logo-container {
  position: relative;
  width: 220px; height: 220px;
  margin-bottom: 40px;
}
.logo-container img {
  width: 180px; height: 180px; object-fit: contain;
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  z-index: 3;
}

/* Scanning Rings */
.scan-ring {
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 200px; height: 200px;
  border-radius: 50%;
  border: 2px solid rgba(224,230,240,0.3);
  animation: scan-pulse 2.5s ease-out infinite;
}
.scan-ring:nth-child(2) { animation-delay: 0.5s; }
.scan-ring:nth-child(3) { animation-delay: 1s; }

@keyframes scan-pulse {
  0% { width: 200px; height: 200px; opacity: 0.8; border-color: rgba(224,230,240,0.5); }
  100% { width: 320px; height: 320px; opacity: 0; border-color: rgba(224,230,240,0); }
}

/* Scan Line */
.scan-line {
  position: absolute; top: 0; left: 50%;
  transform: translateX(-50%);
  width: 180px; height: 3px;
  background: linear-gradient(90deg, transparent, rgba(224,230,240,0.7), transparent);
  border-radius: 2px;
  animation: scan-sweep 2.5s ease-in-out infinite;
  z-index: 4;
  box-shadow: 0 0 15px rgba(224,230,240,0.3);
}
@keyframes scan-sweep {
  0% { top: 15px; opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { top: 200px; opacity: 0; }
}

/* Logo Glow */
.logo-glow {
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 180px; height: 180px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(224,230,240,0.1) 0%, transparent 70%);
  z-index: 1;
  animation: glow-pulse 3s ease-in-out infinite;
}
@keyframes glow-pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
  50% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
}

/* ── Titles ── */
.main-title {
  font-size: 48px; font-weight: 900;
  text-transform: uppercase; letter-spacing: 3px;
  text-align: center; margin-bottom: 0;
}
.sub-title {
  font-size: 42px; font-weight: 900;
  text-transform: uppercase; letter-spacing: 3px;
  text-align: center; margin-bottom: 16px;
}

.instruction-text {
  display: flex; align-items: center; gap: 10px;
  font-size: 16px; color: rgba(255,255,255,0.6);
  margin-bottom: 40px; letter-spacing: 0.5px;
}

/* ── Auth Button ── */
.auth-btn {
  display: flex; flex-direction: column;
  align-items: center; gap: 8px;
  cursor: pointer; text-decoration: none;
  color: rgba(255,255,255,0.8);
  transition: all 0.3s ease;
  padding: 12px 24px;
  border: none; background: none;
}
.auth-btn:hover { color: #ffffff; transform: translateY(-2px); }
.auth-btn .icon-circle {
  width: 56px; height: 56px; border-radius: 50%;
  border: 2px solid rgba(224,230,240,0.4);
  display: flex; align-items: center; justify-content: center;
  transition: all 0.3s ease;
  background: rgba(224,230,240,0.08);
}
.auth-btn:hover .icon-circle {
  border-color: #e0e6f0;
  background: rgba(224,230,240,0.15);
  box-shadow: 0 0 25px rgba(224,230,240,0.15);
}
.auth-btn .icon-circle i { font-size: 22px; color: #e0e6f0; }
.auth-btn span {
  font-size: 11px; font-weight: 600;
  letter-spacing: 2px; text-transform: uppercase;
}

/* ── Time Indicator ── */
.time-indicator {
  position: absolute; bottom: 20px; right: 32px;
  z-index: 10; font-size: 12px;
  color: rgba(255,255,255,0.4);
  letter-spacing: 1px;
  display: flex; align-items: center; gap: 6px;
}

/* ── Welcome Toast ── */
.welcome-toast {
  position: fixed; bottom: 12px; left: 50%;
  transform: translateX(-50%);
  max-width: 460px; width: 90%;
  background: rgba(15,52,96,0.95);
  border: 1px solid rgba(40,167,69,0.5);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
  padding: 16px 20px;
  display: flex; align-items: center; gap: 14px;
  animation: slide-up 0.5s ease-out;
  z-index: 100;
}
@keyframes slide-up {
  from { transform: translateX(-50%) translateY(100px); opacity: 0; }
  to { transform: translateX(-50%) translateY(0); opacity: 1; }
}

.toast-icon {
  width: 36px; height: 36px; border-radius: 50%;
  background: rgba(40,167,69,0.2);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.toast-icon i { color: #28a745; font-size: 18px; }

.toast-content { flex: 1; }
.toast-label {
  font-size: 11px; font-weight: 700; color: #28a745;
  letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 2px;
}
.toast-title { font-size: 15px; font-weight: 700; color: #ffffff; }
.toast-detail { font-size: 12px; color: rgba(255,255,255,0.5); }
.toast-detail .text-green { color: #28a745; font-weight: 700; }

.toast-avatar {
  width: 40px; height: 40px; border-radius: 10px;
  background: rgba(255,255,255,0.1);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.toast-avatar i { font-size: 20px; color: rgba(255,255,255,0.5); }

/* ── Particles ── */
.particles {
  position: fixed; top: 0; left: 0;
  width: 100%; height: 100%;
  pointer-events: none; z-index: 0;
  overflow: hidden;
}
.particle {
  position: absolute; width: 2px; height: 2px;
  background: rgba(224,230,240,0.2);
  border-radius: 50%;
  animation: float-up linear infinite;
}
@keyframes float-up {
  0% { transform: translateY(100vh) scale(0); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateY(-10vh) scale(1); opacity: 0; }
}
</style>
