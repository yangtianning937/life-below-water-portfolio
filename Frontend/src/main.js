// FRONTEND/src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'leaflet/dist/leaflet.css'


import './style.css'
import './assets/global.css'



const app = createApp(App)


app.use(router)


app.config.errorHandler = (err, instance, info) => {
 
  console.error('[Vue Error]', err, info)
}


if (import.meta.env.DEV) {
  
  console.log('✅ App running in DEV mode')
}


app.mount('#app')
