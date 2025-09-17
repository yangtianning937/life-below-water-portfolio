<!-- src/pages/NearbyBeach.vue -->
<script setup lang="ts">
import {ref, onMounted, onBeforeUnmount, computed} from 'vue'
import {fetch_image} from "@/assets/ts/fetch_image";

type Beach = { name: string; lat: number; lng: number }
type Activity = { img: string; name: string; reason: string }

// Common Port Phillip Bay beaches (adjust or extend as needed)
const beaches: Beach[] = [
  {name: 'St Kilda Beach', lat: -37.8676, lng: 144.9730},
  {name: 'Brighton Beach', lat: -37.9179, lng: 144.9869},
  {name: 'Port Melbourne Beach', lat: -37.8393, lng: 144.9423},
  {name: 'Mordialloc Beach', lat: -38.0067, lng: 145.0884},
  {name: 'Dromana Beach', lat: -38.3347, lng: 144.9644},
  {name: 'Capel Sound Beach', lat: -38.3696, lng: 144.8845},
  {name: 'Mornington Beach', lat: -38.2158, lng: 145.0399},
  {name: 'Altona Foreshore', lat: -37.8670, lng: 144.8260},
  {name: 'Frankston Foreshore', lat: -38.1448, lng: 145.1263},
  {name: 'Newport Coastal Reserve', lat: -37.8596, lng: 144.8857},
]

// Example activities (replace with API data if available)
const activities = ref<Activity[]>([
  {
    img: 'swimming.png',
    name: 'Beach Safety Patrol – Port Melbourne',
    reason: 'Learn lifeguard safety tips and why clean water matters.',
  },
  {
    img: 'diving.png',
    name: 'Seagrass Discovery Snorkel – Mordialloc',
    reason: 'See seagrass meadows and small fish with beginner-friendly snorkeling.',
  },
  {
    img: 'fishing.png',
    name: 'Rock Pool Explorer – Dromana',
    reason: 'Find starfish and tiny crabs—perfect for family learning.',
  },
])

// Top gallery images
const gallery = ref<string[]>([
  "https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference=AciIO2c22pTwKoRBmAk-3V8q_5l7RhFMq4j8XbVtki1JoRRMB6WO0diKvRLairozYXzVs-swtVOoCCy3sSFQViCU__cuVnrLmpK_Yvd2Hhnco9eWlgO4lFH3ezKJpuFa8WvxNBw1oBe6fOX8ZvxjZ5BZIU72EgOZxw1svXhlZVwo9SMPg400n1ecPGzWiVeJ-BVDIrbMV_y0ZKmo9lZzlKel94Ai3x4hedJf7KAxM497dSQt0H70inFuDYS6Z9MReDL-98lsYIJ06aictBmz0PY-sgaFSYyJ-WSU0Kb6fhsuhFDaUy8Z4jLWGbs4Qil3zl62CGXw4t3q7987rZ7Wn2xjw1bU3_NpAdermQppkwutWkofjyw1nnFZ6_V9jwO0ERT6nYfzBZETzBX6s_MjwgLv1OBYU7NaDhb57u1_G-pZ1tUQ5OJE&key=AIzaSyBlOgil_jAHzwKulAXTeTSxW_WtpQjCicg",
  "https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference=AciIO2fcMfAzDZgCD-JsCVYY7PLfSdZXg1u7YYNF8fayn4Xb5zes7qlqFAlXJ3t67MYhac2wXfZMC4XxzGGo1eIx3KZJPAISye3r__wgb6gjUIfJA7Sie8PzvyRyDE2BuKhsViv9iIJXwMjJxEiJQGdjxQyitns6tcGT-8nOpA2-tMFnE08tbFdUuV95Kkbby68pHRHfZSNxJL8y88w6GR5D17N7vMZ7FoS1JIqNhGmHe7uDmXew3EPsks0euPtBF9RjGsZEeyEkFYykUSbyV1EmYuqFAzakpnQDy1JHMfFNXxEMbJJfAb8ioGgOlF9PS8Yga6VV5Azxd6rJYa6gbeuST4qA4GIqkRG0vKS2kXhKgH4YnnxJ2JatniVwC6igli-58OAKjFH3UUeYS4yajZPbmClpE4pdYSm8d4vqUTlwWeGghQ&key=AIzaSyBlOgil_jAHzwKulAXTeTSxW_WtpQjCicg",
  "https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference=AciIO2eUM27kZ5N6Pt4JHI4OWJJfLJPuwy_KHbjrzPd42nYc6aVuMK3iNw92sA-vZFhQupCElCYrKsR8JAqBdSOyNNT-FfMQv2FJIkWuddKt7Oo9ypmrGjKcSFhqEvMPkVJZ6q8Fi-6JWZmcPfHtnkuCMf9iELT7ydI1n0eCymFVmLCHoyCzRB_YKMW9mHxEZ7sjXa0Y7WP82c_Ome6jxMtvYstpL67-uAFfsWo-crGk5xV1WmaO7dISYJ3DXDMXSm4L0xhSM3cm9O9l7TeICAGGbFIJpW3Nt0-1LBIPrrQLHPHWsQRkOUiBtJnZjCO7LXJWXNo_wWtekN4CJq_fWDZ7j7F17vK4pRgdjBv5mB1MEcXntEIINfnofND3vAQZpBK24r3y1Dwvi1265qV5Kgc5Mp1nAl_h7v0HuFIXqJi1zKn5vQ&key=AIzaSyBlOgil_jAHzwKulAXTeTSxW_WtpQjCicg"
])

// Activity covers
const coverNames = [
  "swimming.png",
  "diving.png",
  "fishing.png"
]
const covers = ref([]);

for (const i in coverNames) {
  fetch_image(coverNames[i]).then(img => covers.value.push(img));
}

const userLat = ref<number | null>(null)
const userLng = ref<number | null>(null)
const errorMsg = ref<string | null>(null)
const nearest = ref<Beach | null>(null)
const loading = ref(true)

// Haversine distance (km)
function haversine(lat1: number, lon1: number, lat2: number, lon2: number) {
  const toRad = (d: number) => d * Math.PI / 180
  const R = 6371
  const dLat = toRad(lat2 - lat1)
  const dLon = toRad(lon2 - lon1)
  const a = Math.sin(dLat / 2) ** 2 + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

const nearestName = computed(() => {
  if (nearest.value) return nearest.value.name
  if (loading.value) return 'Finding your nearest beach…'
  return errorMsg.value ? 'Location not available' : 'Nearby Beach'
})

onMounted(() => {
  if (!('geolocation' in navigator)) {
    errorMsg.value = 'Geolocation is not supported in this environment.'
    loading.value = false
    return
  }
  navigator.geolocation.getCurrentPosition(
      (pos) => {
        userLat.value = pos.coords.latitude
        userLng.value = pos.coords.longitude
        // Find the nearest beach
        let best: Beach | null = null
        let bestDist = Number.POSITIVE_INFINITY
        for (const b of beaches) {
          const d = haversine(userLat.value!, userLng.value!, b.lat, b.lng)
          if (d < bestDist) {
            bestDist = d;
            best = b
          }
        }
        nearest.value = best
        loading.value = false
      },
      (err) => {
        errorMsg.value = err.message || 'Unable to access location.'
        loading.value = false
      },
      {enableHighAccuracy: true, timeout: 8000, maximumAge: 60000}
  )
})


const isLightboxOpen = ref(false)
const currentIndex = ref<number>(0)

function openImageAt(i: number) {
  currentIndex.value = i
  isLightboxOpen.value = true
  // prevent body scroll
  document.documentElement.style.overflow = 'hidden'
}

function closeLightbox() {
  isLightboxOpen.value = false
  document.documentElement.style.overflow = ''
}

function nextImage() {
  if (!gallery.value.length) return
  currentIndex.value = (currentIndex.value + 1) % gallery.value.length
}

function prevImage() {
  if (!gallery.value.length) return
  currentIndex.value = (currentIndex.value - 1 + gallery.value.length) % gallery.value.length
}

function onKey(e: KeyboardEvent) {
  if (!isLightboxOpen.value) return
  if (e.key === 'Escape') closeLightbox()
  if (e.key === 'ArrowRight') nextImage()
  if (e.key === 'ArrowLeft') prevImage()
}

onMounted(() => window.addEventListener('keydown', onKey))
onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKey)
  document.documentElement.style.overflow = ''
})
</script>

<template>
  <a href="#content" class="skip-link">Skip to content</a>

  <section class="container mx-auto px-4 py-6 space-y-5">
    <!-- Top badge: nearest beach -->
    <header class="flex items-center gap-3">
      <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full border bg-white shadow-sm">
        <span class="text-xl">🏖️</span>
        <span class="font-semibold">
          {{ nearestName }}
        </span>
      </span>

      <p v-if="!loading && userLat!=null" class="text-slate-500 text-sm">
        Your location: {{ userLat.toFixed(4) }}, {{ userLng!.toFixed(4) }}
      </p>
      <p v-if="errorMsg" class="text-red-600 text-sm">{{ errorMsg }}</p>
    </header>

    <!-- Three-image gallery: 50vh height, full-bleed cover -->
    <section aria-label="nearby gallery" class="grid grid-cols-1 sm:grid-cols-3 gap-3">
      <button
          v-for="(src, i) in gallery"
          :key="i"
          type="button"
          class="rounded-xl overflow-hidden border focus:outline-none focus:ring-2 focus:ring-marine-400 cursor-zoom-in"
          @click="openImageAt(i)"
          :aria-label="`Open image ${i+1} of ${gallery.length}`"
      >
        <img :src="src" alt="" class="w-full h-[50vh] object-cover"/>
      </button>
    </section>

    <!-- Activity cards -->
    <section id="content" class="grid md:grid-cols-3 gap-4">
      <article v-for="(a, i) in activities" :key="i"
               class="bg-white border rounded-xl overflow-hidden shadow-sm flex flex-col">
        <img :src="covers[i]" :alt="a.name" class="w-full h-44 object-cover">
        <div class="p-4 flex-1 flex flex-col">
          <h3 class="font-semibold text-lg mb-1 line-clamp-2">{{ a.name }}</h3>
          <p class="text-slate-600 text-sm flex-1">{{ a.reason }}</p>
          <div class="mt-3">
            <button class="px-3 py-2 rounded-lg bg-marine-500 text-white hover:bg-marine-600">
              View Details
            </button>
          </div>
        </div>
      </article>
    </section>
  </section>

  <!-- Lightbox Modal -->
  <div
      v-if="isLightboxOpen"
      class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4"
      role="dialog" aria-modal="true" aria-label="Image preview"
      @click.self="closeLightbox"
  >
    <div class="relative max-w-6xl w-full">
      <!-- Close -->
      <button
          class="absolute -top-3 -right-3 bg-white rounded-full shadow px-3 py-2 text-sm font-semibold hover:bg-slate-100"
          @click="closeLightbox"
          aria-label="Close"
      >
        ✕
      </button>

      <!-- Prev / Next -->
      <button
          class="absolute left-0 top-1/2 -translate-y-1/2 p-3 bg-white/80 hover:bg-white rounded-l focus:outline-none"
          @click.stop="prevImage" aria-label="Previous image"
      >←
      </button>
      <button
          class="absolute right-0 top-1/2 -translate-y-1/2 p-3 bg-white/80 hover:bg-white rounded-r focus:outline-none"
          @click.stop="nextImage" aria-label="Next image"
      >→
      </button>

      <!-- Image -->
      <img
          :src="gallery[currentIndex]"
          alt=""
          class="mx-auto max-h-[85vh] w-auto object-contain rounded shadow-2xl"
          @click.stop
      />
      <div class="mt-3 text-center text-white/90 text-sm">
        Image {{ currentIndex + 1 }} / {{ gallery.length }} — Press Esc to close
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Accessible “skip to content” link (if you already have a global version, you can remove this) */
.skip-link {
  position: absolute;
  left: -9999px;
  top: 8px;
  z-index: 1000;
  background: #0d9488;
  color: #fff;
  padding: 8px 12px;
  border-radius: 8px;
}

.skip-link:focus {
  left: 8px;
}
</style>
