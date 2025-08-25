<template>
  <div id="app" class="min-h-screen bg-gradient-to-b from-blue-50 to-cyan-50">
    <!-- Top Bar -->
    <header
      class="w-full px-5 py-4 flex items-center justify-between bg-white/70 backdrop-blur border-b border-slate-200"
      role="banner"
    >
      <h1 class="text-xl font-semibold text-slate-800">
        Life Below Water
        <span class="ml-2 text-slate-500 text-sm">Marine Education Demo</span>
      </h1>

      <!-- Dropdown: Epics -->
      <div class="relative inline-block text-left" ref="menuRef">
        <button
          type="button"
          @click="isOpen = !isOpen"
          @keydown.esc="isOpen = false"
          class="inline-flex items-center justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50"
          aria-haspopup="true"
          :aria-expanded="isOpen ? 'true' : 'false'"
        >
          {{ currentEpicLabel }}
          <svg class="-mr-1 ml-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.06 1.06l-4.24 4.25a.75.75 0 01-1.06 0L5.25 8.27a.75.75 0 01-.02-1.06z" clip-rule="evenodd"/>
          </svg>
        </button>

        <!-- Menu -->
        <div
          v-if="isOpen"
          class="origin-top-right absolute right-0 mt-2 w-72 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50"
          role="menu"
        >
          <div class="py-1">
            <RouterLink
              :to="{ name: 'epic1' }"
              class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              role="menuitem"
              @click="close()"
            >
              Marine Environment Data Hub
            </RouterLink>
            <RouterLink
              :to="{ name: 'epic2' }"
              class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              role="menuitem"
              @click="close()"
            >
              Volunteer Activity Participation
            </RouterLink>
          </div>
        </div>
      </div>
    </header>

    <!-- Route Outlet -->
    <main class="max-w-6xl mx-auto px-5 py-6">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isOpen = ref(false)
const menuRef = ref(null)


const currentEpicLabel = computed(() => {
  if (route.name === 'epic2' || String(route.name || '').startsWith('epic2')) {
    return 'Volunteer Activity Participation'
  }
  return 'Marine Environment Data Hub'
})

function close() {
  isOpen.value = false
}


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
