<script setup lang="ts">
import {ref, onMounted, onBeforeUnmount} from 'vue'
import {useRoute} from 'vue-router'
import logo from '@/assets/images/logo.jpg';

const route = useRoute()
const isOpen = ref(false)
const brand = 'Port Philip Protectors'

// 桌面端是否默认展开侧边栏
const openOnDesktop = false
let mq: MediaQueryList | null = null
const syncDrawer = () => {
  if (!mq) return
  if (openOnDesktop && mq.matches) isOpen.value = true
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
  {name: 'Home', to: {name: 'home'}, key: 'home', icon: 'home'},
  {name: 'Marine Environment Data Hub', to: {name: 'data_hub'}, key: 'data_hub', icon: 'db'},
  {name: 'Nearby Beach', to: {name: 'nearby'}, key: 'nearby', icon: 'beach'},
  {name: 'Volunteer Activity', to: {name: 'activity'}, key: 'activity', icon: 'vol'}
]
const close = () => (isOpen.value = openOnDesktop && (mq?.matches ?? false) ? true : false)
</script>

<template>
  <header class="o-header sticky top-0 z-50">
    <div class="ocean-ornaments" aria-hidden="true"></div>

    <nav class="w-full h-[56px] pl-2 pr-2 flex items-center gap-3">
      <button
          class="p-2 rounded text-white hover:bg-white/10"
          :aria-expanded="isOpen"
          aria-label="Toggle menu"
          @click="isOpen = !isOpen"
      >
        ☰
      </button>

      <RouterLink to="/" class="font-extrabold text-base md:text-lg text-white flex justify-center items-center gap-2">
        <div class="w-12 rounded-lg overflow-hidden ring-1 ring-white/15">
          <img :src="logo" class="object-fill rounded-lg" alt="">
        </div>
        <span>{{ brand }}</span>
      </RouterLink>

      <div class="flex-1"></div>
    </nav>

    <svg class="waves" viewBox="0 0 1200 100" preserveAspectRatio="none" aria-hidden="true">
      <path class="wave wave-1" d="M0,40 C200,80 400,0 600,40 C800,80 1000,0 1200,40 L1200,100 L0,100 Z"/>
      <path class="wave wave-2" d="M0,60 C200,100 400,20 600,60 C800,100 1000,20 1200,60 L1200,100 L0,100 Z"/>
    </svg>
  </header>


  <div class="drawer-root" :class="{ open: isOpen }">
    <div class="backdrop" @click="isOpen = openOnDesktop && (mq?.matches ?? false) ? true : false"></div>

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
          <svg v-if="it.icon==='home'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M3 11l9-8 9 8" stroke-width="2"/>
            <path d="M9 22V12h6v10" stroke-width="2"/>
          </svg>
          <svg v-else-if="it.icon==='db'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <ellipse cx="12" cy="5" rx="9" ry="3" stroke-width="2"/>
            <path d="M3 5v6c0 1.7 4 3 9 3s9-1.3 9-3V5" stroke-width="2"/>
            <path d="M3 11v6c0 1.7 4 3 9 3s9-1.3 9-3v-6" stroke-width="2"/>
          </svg>
          <svg v-else-if="it.icon==='beach'" width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
               fill="currentColor" aria-hidden="true">
            <path d="M12 6c-3.5 0-5.6 2.2-6.6 4.6h13.2C17.6 8.2 15.5 6 12 6Z"/>
            <path d="M10.4 6.2c.5.1.9.5.8 1.1l-1.5 10.9a1 1 0 1 1-2-.3l1.5-10.9c.1-.6.7-1 .1.0Z"/>
            <path
                d="M3 17.25c2.2 1.6 4.4 1.6 6.6 0 2.2 1.6 4.4 1.6 6.6 0 2.2 1.6 4.4 1.6 6.6 0v1.2c-2.2 1.6-4.4 1.6-6.6 0-2.2 1.6-4.4 1.6-6.6 0-2.2 1.6-4.4 1.6-6.6 0v-1.2Z"/>
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
/* 海洋渐变 */
.o-header {
  color: #fff;
  background: linear-gradient(
      180deg,
      #1f3b82 0%,
      #1e40af 40%,
      #4338ca 75%,
      #4f46e5 100%
  );
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
  overflow: hidden;
}

.ocean-ornaments {
  pointer-events: none;
  position: absolute;
  inset: 0;
  background: radial-gradient(130px 70px at 18% 0%, rgba(255, 255, 255, .18), transparent 60%),
  radial-gradient(150px 80px at 46% -10%, rgba(255, 255, 255, .15), transparent 70%),
  radial-gradient(170px 90px at 80% 0%, rgba(255, 255, 255, .12), transparent 70%),
  repeating-linear-gradient(125deg, rgba(255, 255, 255, .05) 0 14px, rgba(255, 255, 255, .025) 14px 28px);
  mask-image: linear-gradient(to bottom, rgba(0, 0, 0, .95), rgba(0, 0, 0, .2));
  opacity: .75;
}

/* 海浪 */
.waves {
  position: absolute;
  left: 0;
  right: 0;
  bottom: -1px;
  width: 100%;
  height: 28px;
}

.wave {
  fill: rgba(255, 255, 255, .10);
}

.wave-1 {
  animation: drift 12s linear infinite;
}

.wave-2 {
  animation: drift 9s linear infinite reverse;
  opacity: .7;
}

@keyframes drift {
  0% {
    transform: translateX(0)
  }
  100% {
    transform: translateX(-50%)
  }
}

/* 抽屉保持原样式 */
.drawer-root {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 60;
}

.drawer-root.open {
  pointer-events: auto;
}

.backdrop {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, .4);
  opacity: 0;
  transition: opacity .2s;
}

.drawer-root.open .backdrop {
  opacity: 1;
}

.sidenav {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 272px;
  background: #0d1117;
  color: #fff;
  box-shadow: 0 10px 30px rgba(0, 0, 0, .3);
  transform: translateX(-100%);
  transition: transform .22s ease;
  display: flex;
  flex-direction: column;
}

.drawer-root.open .sidenav {
  transform: translateX(0);
}

.sidenav-head {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  border-bottom: 1px solid rgba(255, 255, 255, .08);
}

.sidenav-nav {
  padding: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  margin: 4px 0;
  border-radius: 10px;
  color: #e6edf3;
  text-decoration: none;
}

.nav-item:hover {
  background: rgba(255, 255, 255, .08);
}

.nav-item.active {
  background: rgba(56, 139, 253, .2);
  color: #58a6ff;
}
</style>
