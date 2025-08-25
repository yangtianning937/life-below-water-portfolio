<template>
  <div id="app" class="min-h-screen bg-gradient-to-b from-blue-50 to-cyan-50">
    <!-- Top Bar -->
    <Hearder :currentLabel="currentLabel"/>

    <!-- Route Outlet -->
    <main class="max-w-6xl mx-auto px-5 py-6">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import Hearder from '@/components/Header.vue'
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const menuRef = ref(null)


const currentLabel = computed(() => {
  if (route.name === 'epic2' || String(route.name || '').startsWith('epic2')) {
    return 'Volunteer Activity Participation'
  }
  return 'Marine Environment Data Hub'
})

function onClickOutside(e) {
  if (!menuRef.value) return
  if (!menuRef.value.contains(e.target)) close()
}

onMounted(() => document.addEventListener('click', onClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', onClickOutside))
</script>

<style>
/* Global styles */
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Custom scrollbar */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 10px; }
::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #2563eb; }
</style>
