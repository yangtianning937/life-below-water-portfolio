<!-- FRONTEND/src/App.vue -->
<template>
  <!-- Accessibility: Keyboard users can skip to main content -->
  <a class="skip-link" href="#main-content">Skip to content</a>

  <!-- Sticky footer layout: content area takes full height, footer sticks to bottom -->
  <div class="min-h-screen flex flex-col bg-white text-slate-900">
    <AppHeader />

    <!-- Global ocean decorations -->
     <OceanDecals density="high" :opacity="0.9" :zIndex="99999" :followFullscreen="true" />

    <main id="main-content" class="flex-1">
      <RouterView v-slot="{ Component, route }">
        <transition name="fade" mode="out-in" appear>
          <div v-if="Component" :key="route.path">
            <Suspense>
              <template #default>
                <component :is="Component" />
              </template>
              <template #fallback>
                <div class="min-h-[60vh] flex items-center justify-center">
                  <div class="text-center">
                    <div class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
                    <p class="mt-4 text-slate-600">Loading...</p>
                  </div>
                </div>
              </template>
            </Suspense>
          </div>
        </transition>
      </RouterView>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import { Suspense } from 'vue'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import OceanDecals from '@/components/decorations/OceanDecals.vue'
</script>

<style>
/* Page fade in/out transition */
.fade-enter-active, .fade-leave-active { transition: opacity .18s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* Skip link: visible when focused */
.skip-link {
  position: absolute; left: -9999px; top: 8px; z-index: 1000;
  background: #0d9488; color: #fff; padding: 8px 12px; border-radius: 8px;
}
.skip-link:focus { left: 8px; }
</style>
