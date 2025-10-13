<!-- src/pages/NearbyBeach.vue -->
<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed, watch } from 'vue'
import { fetch_image } from '@/assets/ts/fetch_image'
import { fetch_nearby_beach } from '@/assets/ts/fetch_nearby_beach'
import { fetch_suburb } from '@/assets/ts/fetch_suburb'
import { fetch_places_autocomplete } from '@/assets/ts/fetch_places_autocomplete'
import { fetch_place_details } from '@/assets/ts/fetch_place_details'

type Activity = { img: string; name: string; reason: string }
type Attraction = { name: string; rating: number }
type Restaurant = { name: string; rating: number; address: string }

const GALLERY_SIZE = 3
const MAX_ATTRACTIONS = 3
const MAX_RESTAURANTS = 3
const MAX_ACTIVITIES = 3

// activities
const activities = ref<Activity[]>([
  { img: 'diving.png', name: 'Diving', reason: '' },
  { img: 'swimming.png', name: 'Swimming', reason: '' },
  { img: 'fishing.png', name: 'Fishing', reason: '' },
])

const attractions = ref<Attraction[]>([])
const restaurants = ref<Restaurant[]>([])

// gallery
const gallery = ref<string[]>(Array(GALLERY_SIZE).fill(''))

// state
const userLat = ref<number | null>(null)
const userLng = ref<number | null>(null)
const userSuburb = ref<string | null>(null)          // suburb for searched place
const userCurrentSuburb = ref<string | null>(null)   // suburb for "Use my location"
const errorMsg = ref<string | null>(null)
const nearest = ref<string | null>(null)
const loading = ref<boolean>(true)

// search/filter states
const query = ref<string>('')
const recentSearches = ref<string[]>([])
const useFilters = ref<{ activities: boolean; attractions: boolean; restaurants: boolean }>({
  activities: true,
  attractions: true,
  restaurants: true,
})
const inputHint = ref<string>('Type a place name and choose from suggestions')

// Places autocomplete
const suggestions = ref<any[]>([])
const isSearching = ref<boolean>(false)
let acAbort: AbortController | null = null
const selectedPlace = ref<any | null>(null) // { label, place_id }

// Derived
const nearestName = computed(() => {
  if (nearest.value) return nearest.value
  if (loading.value) return 'Finding your nearest beach…'
  return errorMsg.value ? 'Location unavailable' : 'Nearby Beach'
})

function fillGallery(srcs: string[]) {
  for (let i = 0; i < GALLERY_SIZE; i++) gallery.value[i] = srcs[i] ?? ''
}

function resetActivities() {
  activities.value = [
    { img: 'diving.png', name: 'Diving', reason: '' },
    { img: 'swimming.png', name: 'Swimming', reason: '' },
    { img: 'fishing.png', name: 'Fishing', reason: '' },
  ]
}

async function hydrateActivities(recos: string[]) {
  resetActivities()
  const n = Math.min(activities.value.length, recos.length)
  for (let i = 0; i < n; i++) {
    activities.value[i].img = await fetch_image(activities.value[i].img)
    activities.value[i].reason = recos[i] ?? ''
  }
}

function resetLists() {
  attractions.value = []
  restaurants.value = []
}

async function loadByCoords(lat: number, lng: number) {
  loading.value = true
  errorMsg.value = null
  try {
    const r = await fetch_nearby_beach(lat, lng)
    nearest.value = r?.name ?? null
    fillGallery(r?.photos ?? [])
    await hydrateActivities(r?.assessment?.recommendations ?? [])
    resetLists()
    if (Array.isArray(r?.recommendations?.attractions)) {
      for (let i = 0; i < r.recommendations.attractions.length; i++) {
        const it = r.recommendations.attractions[i]
        if (!it) continue
        attractions.value.push({
          name: it.name,
          rating: Number(it.rating) || 0,
        })
      }
    }
    if (Array.isArray(r?.recommendations?.restaurants)) {
      for (let i = 0; i < r.recommendations.restaurants.length; i++) {
        const it = r.recommendations.restaurants[i]
        if (!it) continue
        restaurants.value.push({
          name: it.name,
          rating: Number(it.rating) || 0,
          address: it.address,
        })
      }
    }
  } catch (e: any) {
    errorMsg.value = e?.message || 'Failed to load beach data.'
  } finally {
    loading.value = false
  }
}

// ---------- Autocomplete flow ----------

// typing → fetch suggestions (names only)
watch(query, async (q) => {
  // When user types, invalidate previously selected place
  selectedPlace.value = null

  const text = q?.trim() || ''
  if (text.length < 2) {
    suggestions.value = []
    acAbort?.abort()
    return
  }
  acAbort?.abort()
  acAbort = new AbortController()
  const signal = acAbort.signal
  isSearching.value = true
  const data = await fetch_places_autocomplete(text, 'AU', 8, 'en')
  if (!signal.aborted) {
    suggestions.value = data?.suggestions || []
    isSearching.value = false
  }
})

// choose a suggestion → sync input to label → load
async function selectSuggestion(s: any) {
  selectedPlace.value = s
  query.value = s.label            // sync input to chosen place name
  suggestions.value = []           // close dropdown

  const d = await fetch_place_details(s.place_id, 'en')
  if (d && Number.isFinite(d.lat) && Number.isFinite(d.lng)) {
    userLat.value = d.lat
    userLng.value = d.lng
    const sub = await fetch_suburb(d.lat, d.lng)
    userSuburb.value = (sub && sub.suburbName) || d.name || s.label
    await loadByCoords(d.lat, d.lng)
    addRecent(s.label)
  } else {
    errorMsg.value = 'No coordinates for this place.'
  }
}

// hit Enter / click Search: require a place selection or auto-pick top suggestion
async function onEnterSearch() {
  const text = query.value.trim()
  if (!text) return

  // If user already selected a suggestion, use it
  if (selectedPlace.value) {
    await selectSuggestion(selectedPlace.value)
    return
  }

  // Otherwise auto-pick the first suggestion if available
  if (suggestions.value.length > 0) {
    await selectSuggestion(suggestions.value[0])
    return
  }
}

function addRecent(text: string) {
  if (!recentSearches.value.includes(text)) {
    recentSearches.value.unshift(text)
    if (recentSearches.value.length > 5) recentSearches.value.pop()
  }
}

const canSearch = computed(() => {
  const text = (query.value || "").trim()
  return !!selectedPlace.value || (text.length >= 2 && suggestions.value.length > 0)
})

// ---------- Use my location ----------
function useMyLocation() {
  errorMsg.value = null
  loading.value = true
  if (typeof window === 'undefined' || !('geolocation' in navigator)) {
    errorMsg.value = 'Geolocation is not supported in this environment.'
    loading.value = false
    return
  }
  navigator.geolocation.getCurrentPosition(
    async (pos) => {
      userLat.value = pos.coords.latitude
      userLng.value = pos.coords.longitude

      await fetch_suburb(pos.coords.latitude, pos.coords.longitude).then((r) => {
        userCurrentSuburb.value = r?.suburbName || null
      })

      await loadByCoords(userLat.value, userLng.value)
    },
    (err) => {
      errorMsg.value = err?.message || 'Unable to access location.'
      loading.value = false
    },
    { enableHighAccuracy: true, timeout: 8000, maximumAge: 60000 }
  )
}

onMounted(() => {
  useMyLocation()
})

const isLightboxOpen = ref(false)
const currentIndex = ref<number>(0)

function openImageAt(i: number) {
  if (!gallery.value[i]) return
  currentIndex.value = i
  isLightboxOpen.value = true
  if (typeof document !== 'undefined') document.documentElement.style.overflow = 'hidden'
}

function closeLightbox() {
  isLightboxOpen.value = false
  if (typeof document !== 'undefined') document.documentElement.style.overflow = ''
}

function nextImage() {
  if (!gallery.value.length) return
  let next = (currentIndex.value + 1) % gallery.value.length
  let guard = 0
  while (!gallery.value[next] && guard++ < gallery.value.length) next = (next + 1) % gallery.value.length
  currentIndex.value = next
}

function prevImage() {
  if (!gallery.value.length) return
  let prev = (currentIndex.value - 1 + gallery.value.length) % gallery.value.length
  let guard = 0
  while (!gallery.value[prev] && guard++ < gallery.value.length) prev = (prev - 1 + gallery.value.length) % gallery.value.length
  currentIndex.value = prev
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
  if (typeof document !== 'undefined') document.documentElement.style.overflow = ''
})
</script>

<template>
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <!-- Top toolbar: search + filters + location (compact) -->
  <div class="w-full sticky top-0 z-10 bg-white/80 backdrop-blur border-b">
    <div class="container mx-auto px-3 lg:px-4 py-1 flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
      <!-- Make container relative to anchor the dropdown -->
      <div class="flex-1 flex items-center gap-2 relative">
        <input
          v-model="query"
          type="text"
          :placeholder="inputHint"
          @keyup.enter="onEnterSearch"
          class="w-full md:w-[480px] rounded-lg border px-3 py-1.5 text-sm outline-none focus:ring-2 focus:ring-marine-400"
        />
        <button type="button" class="rounded-lg border px-3 py-1.5 text-sm bg-white hover:bg-slate-50" @click="onEnterSearch" :disabled="loading || !canSearch">
          Search
        </button>
        <button
          type="button"
          class="rounded-lg border px-3 py-1.5 text-sm bg-white hover:bg-slate-50"
          @click="useMyLocation"
          :disabled="loading"
          title="Use my location"
        >
          Use my location
        </button>

        <!-- ▼ Google Places suggestions dropdown (names only) ▼ -->
        <div
          v-if="suggestions.length && query"
          class="absolute left-0 top-full mt-1 w-full md:w-[480px] bg-white border rounded-lg shadow z-20 overflow-hidden"
        >
          <button
            v-for="(s, i) in suggestions"
            :key="s.place_id || i"
            type="button"
            class="w-full text-left px-3 py-2 text-sm hover:bg-slate-50"
            @click="selectSuggestion(s)"
          >
            {{ s.label }}
          </button>
          <div v-if="isSearching" class="px-3 py-2 text-xs text-slate-500 border-t">Searching…</div>
        </div>
        <!-- ▲ Google Places suggestions dropdown ▲ -->
      </div>

      <div class="flex items-center gap-2">
        <label class="inline-flex items-center gap-1 text-sm cursor-pointer select-none">
          <input type="checkbox" v-model="useFilters.activities" class="accent-teal-600" />
          Activities
        </label>
        <label class="inline-flex items-center gap-1 text-sm cursor-pointer select-none">
          <input type="checkbox" v-model="useFilters.attractions" class="accent-teal-600" />
          Attractions
        </label>
        <label class="inline-flex items-center gap-1 text-sm cursor-pointer select-none">
          <input type="checkbox" v-model="useFilters.restaurants" class="accent-teal-600" />
          Restaurants
        </label>
      </div>
    </div>

    <!-- Recent searches -->
    <div v-if="recentSearches.length" class="container mx-auto px-3 lg:px-4 pb-1">
      <div class="flex items-center gap-2 flex-wrap text-xs">
        <span class="text-slate-500">Recent:</span>
        <button
          v-for="(t, i) in recentSearches"
          :key="`rs-${i}-${t}`"
          class="px-2 py-1 rounded-full border bg-white hover:bg-slate-50"
          @click="query = t; onEnterSearch()"
          type="button"
        >
          {{ t }}
        </button>
      </div>
    </div>
  </div>

  <!-- Loading Progress Bar -->
  <div v-if="loading" class="fixed top-0 left-0 right-0 z-50">
    <div class="h-1 bg-gradient-to-r from-blue-100 via-teal-100 to-blue-100 relative overflow-hidden">
      <div class="h-full bg-gradient-to-r from-blue-500 via-cyan-400 to-teal-500 relative"
           style="animation: progress 2s ease-in-out infinite;">
        <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-30"
             style="animation: shimmer 1.5s ease-in-out infinite;"></div>
      </div>
    </div>
  </div>

  <!-- Dashboard -->
  <section id="main-content" class="container mx-auto px-3 lg:px-4 py-2 space-y-2">
    <!-- Status Row -->
    <header class="flex items-center gap-2 text-sm" aria-live="polite">
      <template v-if="loading">
        <span class="inline-flex items-center gap-2 px-2.5 py-1 rounded-full border bg-white shadow-sm">
          <span class="h-4 w-24 bg-gray-200 rounded animate-pulse"></span>
        </span>
        <span class="h-4 w-48 bg-gray-200 rounded animate-pulse"></span>
      </template>
      <template v-else>
        <span class="inline-flex items-center gap-2 px-2.5 py-1 rounded-full border bg-white shadow-sm">
          <span class="text-lg">🏖️</span>
          <span class="font-semibold">{{ nearestName }}</span>
        </span>
        <p v-if="userCurrentSuburb!=null" class="text-slate-500">
          Your location: {{ userCurrentSuburb }}
        </p>
        <p v-if="errorMsg" class="text-red-600" role="alert">{{ errorMsg }}</p>
      </template>
    </header>

    <div id="dashboard-grid" class="grid gap-2 lg:gap-3">
      <!-- Left: Gallery (20vh per tile, image fills cell) -->
      <section aria-label="Nearby gallery" class="grid grid-cols-3 gap-2">
        <button
          v-for="(src, i) in gallery"
          :key="`gallery-${i}`"
          type="button"
          class="relative rounded-lg overflow-hidden border focus:outline-none focus:ring-2 focus:ring-marine-400 cursor-zoom-in"
          @click="openImageAt(i)"
          :disabled="loading || !src"
          :aria-label="`Open image ${i+1} of ${gallery.length}`"
        >
          <div class="relative w-full h-[20vh]">
            <div v-if="loading || !src" class="absolute inset-0 bg-gray-200 animate-pulse"></div>
            <img v-else :src="src" alt="" class="absolute inset-0 w-full h-full object-cover block" loading="lazy" decoding="async" />
          </div>
        </button>
      </section>

      <!-- Middle: Activities -->
      <section v-if="useFilters.activities" class="grid gap-2">
        <h2 class="font-semibold text-base">🎯 Recommended Activities</h2>
        <div class="grid md:grid-cols-3 lg:grid-cols-1 gap-2">
          <article
            v-for="(a, i) in activities.slice(0, MAX_ACTIVITIES)"
            :key="`act-${i}-${a.name}`"
            class="bg-white border rounded-lg overflow-hidden shadow-sm"
          >
            <div class="relative w-full h-[12vh]">
              <div v-if="loading" class="absolute inset-0 bg-gray-200 animate-pulse"></div>
              <img v-else :src="a.img" :alt="a.name" class="absolute inset-0 w-full h-full object-cover block" loading="lazy" decoding="async" />
            </div>
            <div class="p-2">
              <template v-if="loading">
                <div class="h-4 w-24 bg-gray-200 rounded mb-1.5 animate-pulse"></div>
                <div class="h-3 w-10/12 bg-gray-200 rounded animate-pulse"></div>
              </template>
              <template v-else>
                <h3 class="font-semibold text-sm mb-0.5 line-clamp-1">{{ a.name }}</h3>
                <p class="text-slate-600 text-xs leading-snug line-clamp-1">{{ a.reason }}</p>
              </template>
            </div>
          </article>
        </div>
      </section>

      <!-- Right: Attractions + Restaurants -->
      <section class="grid gap-2 lg:gap-3">
        <div v-if="useFilters.attractions" class="space-y-1.5">
          <h2 class="font-semibold text-base">🖼️ Attractions (Top {{ MAX_ATTRACTIONS }})</h2>

          <div v-if="loading" class="grid gap-2">
            <article v-for="i in MAX_ATTRACTIONS" :key="`attr-skel-${i}`" class="bg-white border rounded-lg p-3 shadow-sm">
              <div class="h-4 w-2/3 bg-gray-200 rounded mb-1.5 animate-pulse"></div>
              <div class="h-3 w-24 bg-gray-200 rounded animate-pulse"></div>
            </article>
          </div>

          <div v-else class="grid gap-2">
            <article
              v-for="(a, i) in attractions.slice(0, MAX_ATTRACTIONS)"
              :key="`attr-${i}-${a.name}`"
              class="bg-white border rounded-lg overflow-hidden shadow-sm p-3"
            >
              <h3 class="font-semibold text-sm mb-0.5 line-clamp-1">{{ a.name }}</h3>
              <p class="text-slate-600 text-xs leading-snug">
                <span class="font-semibold">Rating:</span> {{ a.rating }}
              </p>
            </article>
            <p v-if="!attractions.length" class="text-slate-500 text-sm">No attractions found.</p>
          </div>
        </div>

        <div v-if="useFilters.restaurants" class="space-y-1.5">
          <h2 class="font-semibold text-base">🍽️ Restaurants (Top {{ MAX_RESTAURANTS }})</h2>

          <div v-if="loading" class="grid gap-2">
            <article v-for="i in MAX_RESTAURANTS" :key="`rest-skel-${i}`" class="bg-white border rounded-lg p-3 shadow-sm">
              <div class="h-4 w-3/4 bg-gray-200 rounded mb-1.5 animate-pulse"></div>
              <div class="h-3 w-5/6 bg-gray-200 rounded mb-1 animate-pulse"></div>
              <div class="h-3 w-24 bg-gray-200 rounded animate-pulse"></div>
            </article>
          </div>

          <div v-else class="grid gap-2">
            <article
              v-for="(r, i) in restaurants.slice(0, MAX_RESTAURANTS)"
              :key="`rest-${i}-${r.name}`"
              class="bg-white border rounded-lg overflow-hidden shadow-sm p-3"
            >
              <h3 class="font-semibold text-sm mb-0.5 line-clamp-1">{{ r.name }}</h3>
              <p class="text-slate-600 text-xs leading-snug mb-0.5 line-clamp-1">
                <span class="font-semibold">Address:</span> {{ r.address }}
              </p>
              <p class="text-slate-600 text-xs leading-snug">
                <span class="font-semibold">Rating:</span> {{ r.rating }}
              </p>
            </article>
            <p v-if="!restaurants.length" class="text-slate-500 text-sm">No restaurants found.</p>
          </div>
        </div>
      </section>
    </div>
  </section>

  <!-- Lightbox -->
  <div
    v-if="isLightboxOpen"
    class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4"
    role="dialog"
    aria-modal="true"
    aria-label="Image preview"
    @click.self="closeLightbox"
  >
    <div class="relative max-w-6xl w-full">
      <button class="absolute -top-3 -right-3 bg-white rounded-full shadow px-3 py-2 text-sm font-semibold hover:bg-slate-100" @click="closeLightbox" aria-label="Close">
        ✕
      </button>
      <button class="absolute left-0 top-1/2 -translate-y-1/2 p-3 bg-white/80 hover:bg-white rounded-l" @click.stop="prevImage" aria-label="Previous image">
        ←
      </button>
      <button class="absolute right-0 top-1/2 -translate-y-1/2 p-3 bg-white/80 hover:bg-white rounded-r" @click.stop="nextImage" aria-label="Next image">
        →
      </button>
      <img :src="gallery[currentIndex]" alt="" class="mx-auto max-h-[85vh] w-auto object-contain rounded shadow-2xl" @click.stop decoding="async" />
      <div class="mt-3 text-center text-white/90 text-sm">Image {{ currentIndex + 1 }} / {{ gallery.length }} — Press Esc to close</div>
    </div>
  </div>
</template>

<style scoped>
/* Accessible skip link */
.skip-link {
  position: absolute;
  left: -9999px;
  top: 8px;
  z-index: 1000;
  background: #0d9488;
  color: #fff;
  padding: 6px 10px;
  border-radius: 8px;
}
.skip-link:focus { left: 8px; }

/* Text clamping */
.line-clamp-1 { display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden; }
.line-clamp-2 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

/* Loading Progress Bar Animation */
@keyframes progress {
  0% {
    width: 0%;
    background-position: 0% 50%;
  }
  50% {
    width: 70%;
    background-position: 100% 50%;
  }
  100% {
    width: 100%;
    background-position: 0% 50%;
  }
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* Responsive columns (wider first column) */
#dashboard-grid { grid-template-columns: 1fr; }
@media (min-width: 768px) and (max-width: 1023.98px) { #dashboard-grid { grid-template-columns: 1fr 1fr; } }
@media (min-width: 1024px) { #dashboard-grid { grid-template-columns: 1.1fr 1fr 1fr; } }
</style>
