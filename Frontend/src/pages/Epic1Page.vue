<template>
  <div class="epic1-container">
    <!-- Header -->
    <Header
        :title="'Marine Environment Data Hub'"
        :subtitle="'Port Phillip Bay Marine Health Monitoring'"
    />

    <!-- Navigation Tabs -->
    <div class="bg-white shadow-md sticky top-0 z-40">
      <div class="container mx-auto px-4">
        <div class="flex gap-1">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'px-6 py-4 font-semibold transition-all border-b-3',
              activeTab === tab.id
                ? 'border-blue-500 text-blue-600 bg-blue-50'
                : 'border-transparent text-gray-600 hover:bg-gray-50'
            ]"
          >
            {{ tab.icon }} {{ tab.name }}
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <p class="text-red-600">{{ error }}</p>
        <button @click="retryConnection" class="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
          Retry Connection
        </button>
      </div>

      <!-- Content Sections -->
      <div v-else>
        <!-- Dashboard Tab -->
        <section v-show="activeTab === 'dashboard'" class="space-y-6">
          <div class="bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-2xl font-bold mb-4">Quick Stats</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div v-for="stat in quickStats" :key="stat.label" 
                   class="bg-gray-50 rounded-lg p-4">
                <div class="text-sm text-gray-600">{{ stat.label }}</div>
                <div class="text-2xl font-bold text-blue-600">{{ stat.value }}</div>
              </div>
            </div>
          </div>

          <!-- Simple Heatmap -->
          <div class="bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-2xl font-bold mb-4">Water Quality Heatmap</h2>
            <div class="grid grid-cols-8 gap-1 max-w-md">
              <div v-for="(cell, index) in heatmapData" :key="index"
                   :style="{ backgroundColor: getHeatmapColor(cell) }"
                   class="aspect-square rounded cursor-pointer"
                   :title="`Value: ${cell}`">
              </div>
            </div>
            <div class="mt-4 flex justify-between text-sm text-gray-600">
              <span>Low</span>
              <span>High</span>
            </div>
          </div>
        </section>

        <!-- Map Tab -->
        <section v-show="activeTab === 'map'" class="space-y-6">
          <div class="bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-2xl font-bold mb-4">Monitoring Stations</h2>
            <div id="marineMap" style="height: 400px;" class="rounded-lg bg-gray-100"></div>
            
            <!-- Station Info -->
            <div v-if="selectedStation" class="mt-4 p-4 bg-blue-50 rounded-lg">
              <h3 class="font-bold">{{ selectedStation.name }}</h3>
              <p>Status: <span :class="getStatusColor(selectedStation.status)">{{ selectedStation.status }}</span></p>
              <p>Temperature: {{ selectedStation.temperature }}°C</p>
            </div>
          </div>
        </section>

        <!-- Time Series Tab -->
        <section v-show="activeTab === 'timeseries'" class="space-y-6">
          <div class="bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-2xl font-bold mb-4">Historical Trends</h2>
            <div class="mb-4">
              <button v-for="range in timeRanges" :key="range"
                      @click="selectedTimeRange = range; updateChart()"
                      :class="[
                        'px-4 py-2 mr-2 rounded',
                        selectedTimeRange === range
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 hover:bg-gray-300'
                      ]">
                {{ range }}
              </button>
            </div>
            <div style="height: 400px;">
              <canvas id="timeSeriesChart"></canvas>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, reactive, onMounted, watch, nextTick } from 'vue'
import axios from 'axios'
import L from 'leaflet'
import Chart from 'chart.js/auto'
import Header from "@/components/Header.vue";

// Fix Leaflet markers
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png'
})

export default {
  name: 'Epic1Page',
  components: {Header},
  setup() {
    // API Configuration
    const API_BASE_URL = import.meta.env.VITE_APP_API_URL || 'http://localhost:3000/api'
    
    // State
    const loading = ref(false)
    const error = ref(null)
    const activeTab = ref('dashboard')
    const selectedStation = ref(null)
    const selectedTimeRange = ref('1 Month')
    
    // Configuration
    const tabs = [
      { id: 'dashboard', name: 'Dashboard', icon: '📊' },
      { id: 'map', name: 'Map', icon: '🗺️' },
      { id: 'timeseries', name: 'Trends', icon: '📈' }
    ]
    
    const timeRanges = ['1 Month']
    
    // Demo Data
    const quickStats = ref([
      { label: 'Temperature', value: '18.5°C' },
      { label: 'pH Level', value: '7.8' },
      { label: 'Water Quality', value: '85%' },
      { label: 'Active Stations', value: '5' }
    ])
    
    // Simple 8x8 heatmap data
    const heatmapData = ref(Array(64).fill(0).map(() => Math.random() * 100))
    
    // Demo station data
    const stations = [
      { id: 1, lat: -38.15, lng: 144.85, name: 'Central Bay', status: 'Active', temperature: 18.5 },
      { id: 2, lat: -38.10, lng: 144.90, name: 'North Monitor', status: 'Warning', temperature: 19.2 },
      { id: 3, lat: -38.20, lng: 144.80, name: 'West Station', status: 'Active', temperature: 17.8 }
    ]
    
    // Map and Chart refs
    const map = ref(null)
    const chart = ref(null)
    
    // Methods
    const getHeatmapColor = (value) => {
      const colors = ['#10b981', '#84cc16', '#eab308', '#f97316', '#ef4444']
      const index = Math.floor((value / 100) * colors.length)
      return colors[Math.min(index, colors.length - 1)]
    }
    
    const getStatusColor = (status) => {
      const colors = {
        'Active': 'text-green-600',
        'Warning': 'text-yellow-600',
        'Critical': 'text-red-600'
      }
      return colors[status] || 'text-gray-600'
    }
    
    const initMap = () => {
      nextTick(() => {
        const mapElement = document.getElementById('marineMap')
        if (!mapElement) return
        
        if (map.value) {
          map.value.remove()
        }
        
        map.value = L.map('marineMap').setView([-38.15, 144.85], 10)
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap contributors'
        }).addTo(map.value)
        
        // Add demo markers
        stations.forEach(station => {
          const color = station.status === 'Warning' ? 'red' : 'green'
          const marker = L.circleMarker([station.lat, station.lng], {
            radius: 8,
            fillColor: color,
            color: 'white',
            weight: 2,
            fillOpacity: 0.8
          }).addTo(map.value)
          
          marker.bindPopup(`<b>${station.name}</b><br>Status: ${station.status}`)
          marker.on('click', () => {
            selectedStation.value = station
          })
        })
      })
    }
    
    const updateChart = () => {
      nextTick(() => {
        const ctx = document.getElementById('timeSeriesChart')
        if (!ctx) return
        
        if (chart.value) {
          chart.value.destroy()
        }
        
        // Generate demo data based on selected time range
        const dataPoints = selectedTimeRange.value === '1 Week' ? 7 : 
                          selectedTimeRange.value === '1 Month' ? 30 : 90
        
        const labels = Array(dataPoints).fill(0).map((_, i) => `Day ${i + 1}`)
        const data = Array(dataPoints).fill(0).map(() => Math.random() * 10 + 15)
        
        chart.value = new Chart(ctx, {
          type: 'line',
          data: {
            labels,
            datasets: [{
              label: 'Temperature (°C)',
              data,
              borderColor: 'rgb(59, 130, 246)',
              backgroundColor: 'rgba(59, 130, 246, 0.1)',
              tension: 0.4
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { position: 'top' }
            },
            scales: {
              y: { beginAtZero: false }
            }
          }
        })
      })
    }
    
    // API Methods (kept for future use)
    const fetchData = async (endpoint) => {
      try {
        loading.value = true
        error.value = null
        const response = await axios.get(`${API_BASE_URL}${endpoint}`)
        return response.data
      } catch (err) {
        console.error('API Error:', err)
        error.value = 'Failed to load data. Using demo data.'
        return null
      } finally {
        loading.value = false
      }
    }
    
    const retryConnection = () => {
      error.value = null
      // Retry logic here
    }
    
    // Watchers
    watch(activeTab, (newTab) => {
      if (newTab === 'map') {
        setTimeout(initMap, 100) // Small delay to ensure DOM is ready
      } else if (newTab === 'timeseries') {
        setTimeout(updateChart, 100)
      }
    })
    
    // Lifecycle
    onMounted(() => {
      // Initialize with dashboard
      console.log('Marine Hub initialized')
    })
    
    return {
      // State
      loading,
      error,
      activeTab,
      selectedStation,
      selectedTimeRange,
      tabs,
      timeRanges,
      quickStats,
      heatmapData,
      
      // Methods
      getHeatmapColor,
      getStatusColor,
      updateChart,
      fetchData,
      retryConnection
    }
  }
}
</script>

<style scoped>
.epic1-container {
  min-height: 100vh;
}

.border-b-3 {
  border-bottom-width: 3px;
}

.aspect-square {
  aspect-ratio: 1 / 1;
}

#marineMap {
  z-index: 10;
}

#timeSeriesChart {
  width: 100% !important;
  height: 100% !important;
}
</style>