// FRONTEND/src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'leaflet/dist/leaflet.css'

import OceanDecals from '@/components/decorations/OceanDecals.vue'

import './style.css'
import './assets/global.css'



const app = createApp(App)


app.use(router)


app.config.errorHandler = (err, instance, info) => {
  console.error('[Vue Error]', err, info)
  // Add user-friendly error notifications here
  if (err.message && err.message.includes('Failed to fetch')) {
    console.error('Network error: Failed to load component')
  }
}

// Handle router errors
router.onError((error) => {
  console.error('[Router Error]', error)
  // If component loading fails, retry or show error page
  if (error.message.includes('Failed to fetch dynamically imported module')) {
    console.error('Failed to load page component. Reloading...')
    window.location.reload()
  }
})


if (import.meta.env.DEV) {
  console.log('App running in DEV mode')
}

app.component('OceanDecals', OceanDecals)

app.mount('#app')
