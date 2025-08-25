import { createApp } from 'vue'
import App from './App.vue'
import './style.css'

// Create Vue application
const app = createApp(App)

// Global error handler
app.config.errorHandler = (err, instance, info) => {
  console.error('Global error:', err)
  console.error('Error info:', info)
}

// Mount the application
app.mount('#app')