<!-- FRONTEND/src/App.vue -->
<template>
  <!-- 无障碍：键盘用户可直接跳到主内容 -->
  <a class="skip-link" href="#main-content">Skip to content</a>

  <!-- 吸底布局：内容区占满高度，Footer 贴底 -->
  <div class="min-h-screen flex flex-col bg-white text-slate-900">
    <AppHeader />

    <!-- 全局海洋贴图 -->
     <OceanDecals density="high" :opacity="0.9" :zIndex="99999" :followFullscreen="true" />

    <main id="main-content" class="flex-1">
      <RouterView v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'

import OceanDecals from '@/components/decorations/OceanDecals.vue'
</script>

<style>
/* 页面淡入淡出过渡 */
.fade-enter-active, .fade-leave-active { transition: opacity .18s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* Skip link：聚焦时可见 */
.skip-link {
  position: absolute; left: -9999px; top: 8px; z-index: 1000;
  background: #0d9488; color: #fff; padding: 8px 12px; border-radius: 8px;
}
.skip-link:focus { left: 8px; }
</style>
