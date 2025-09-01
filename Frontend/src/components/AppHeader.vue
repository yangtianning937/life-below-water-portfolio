<!-- src/components/AppHeader.vue -->
<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isOpen = ref(false)

// 需要时可让桌面端默认展开（>=1024px）
const openOnDesktop = false
let mq: MediaQueryList | null = null
function syncDrawer() {
  if (!mq) return
  if (openOnDesktop && mq.matches) {
    isOpen.value = true
  }
}
onMounted(() => {
  mq = window.matchMedia('(min-width: 1024px)')
  syncDrawer()
  mq.addEventListener?.('change', syncDrawer)
})
onBeforeUnmount(() => {
  mq?.removeEventListener?.('change', syncDrawer)
})

const navItems = [
  { name: 'Home', to: { name: 'home' }, key: 'home', icon: 'home' },
  { name: 'Marine Environment Data Hub', to: { name: 'data_hub' }, key: 'data_hub', icon: 'db' },
  { name: 'Volunteer Activity', to: { name: 'activity' }, key: 'activity', icon: 'vol' }
]
const close = () => (isOpen.value = openOnDesktop && (mq?.matches ?? false) ? true : false)
</script>

<template>
  <!-- 顶部条：品牌 + 汉堡按钮（所有分辨率都显示） -->
  <header class="sticky top-0 z-50 bg-white/90 backdrop-blur border-b border-slate-200">
    <nav class="max-w-6xl mx-auto px-4 h-[56px] flex items-center justify-between">
      <RouterLink to="/" class="font-extrabold text-lg text-slate-900">OceanLens</RouterLink>
      <button
        class="p-2 rounded hover:bg-slate-100"
        :aria-expanded="isOpen"
        aria-label="Toggle menu"
        @click="isOpen = !isOpen"
      >☰</button>
    </nav>
  </header>

  <!-- 抽屉式侧边栏：桌面端也使用同样样式 -->
  <div class="drawer-root" :class="{ open: isOpen }">
    <!-- 背景遮罩：仅在非桌面或未默认展开时显示 -->
    <div
      class="backdrop"
      @click="isOpen = openOnDesktop && (mq?.matches ?? false) ? true : false"
    ></div>

    <aside class="sidenav">
      <div class="sidenav-head">
        <span class="font-bold">Menu</span>
        <button class="p-2 rounded hover:bg-white/10" @click="isOpen = false" aria-label="Close">✕</button>
      </div>

      <nav class="sidenav-nav">
        <RouterLink
          v-for="it in navItems"
          :key="it.key"
          :to="it.to"
          class="nav-item"
          :class="{ active: route.name === it.key }"
          @click="close()"
        >
          <!-- 简洁图标 -->
          <svg v-if="it.icon==='home'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M3 11l9-8 9 8" stroke-width="2"/><path d="M9 22V12h6v10" stroke-width="2"/>
          </svg>
          <svg v-else-if="it.icon==='db'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <ellipse cx="12" cy="5" rx="9" ry="3" stroke-width="2"/>
            <path d="M3 5v6c0 1.7 4 3 9 3s9-1.3 9-3V5" stroke-width="2"/>
            <path d="M3 11v6c0 1.7 4 3 9 3s9-1.3 9-3v-6" stroke-width="2"/>
          </svg>
          <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M20 21v-7M4 21v-7M4 10a4 4 0 1 1 6 3.46A5 5 0 0 0 20 18" stroke-width="2"/>
          </svg>
          <span>{{ it.name }}</span>
        </RouterLink>
      </nav>
    </aside>
  </div>
</template>

<style scoped>
/* 抽屉容器 */
.drawer-root { position: fixed; inset: 0; pointer-events: none; z-index: 60; }
.drawer-root.open { pointer-events: auto; }
/* 背景遮罩：默认隐藏；当不是桌面持久展开时显示 */
.backdrop {
  position: absolute; inset: 0; background: rgba(0,0,0,.4);
  opacity: 0; transition: opacity .2s;
}
.drawer-root.open .backdrop { opacity: 1; }
/* 侧边栏本体 */
.sidenav {
  position: absolute; top: 0; left: 0; height: 100%; width: 272px;
  background: #0d1117; color: #fff; box-shadow: 0 10px 30px rgba(0,0,0,.3);
  transform: translateX(-100%); transition: transform .22s ease;
  display: flex; flex-direction: column;
}
.drawer-root.open .sidenav { transform: translateX(0); }

.sidenav-head {
  height: 56px; display: flex; align-items: center; justify-content: space-between;
  padding: 0 16px; border-bottom: 1px solid rgba(255,255,255,.08);
}
.sidenav-nav { padding: 8px; }
.nav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px; margin: 4px 0; border-radius: 10px;
  color: #e6edf3; text-decoration: none;
}
.nav-item:hover { background: rgba(255,255,255,.08); }
.nav-item.active { background: rgba(56,139,253,.2); color: #58a6ff; }
</style>
