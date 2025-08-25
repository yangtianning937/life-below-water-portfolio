<template>
  <div id="app" class="min-h-screen bg-gradient-to-b from-blue-50 to-cyan-50">
    <!-- Main Application Container -->
    <Epic1Page />
  </div>
</template>

<script>
import Epic1Page from './components/Epic1Page.vue'

export default {
  name: 'App',
  components: {
    Epic1Page
  },
  mounted() {
    console.log('Marine Environment Data Hub App initialized')
  }
}
</script>

<style>
/* Global styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}


body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #3b82f6;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #2563eb;
}
</style>