<!-- src/pages/NearbyBeach.vue -->
<script setup lang="ts">
import {ref, onMounted, onBeforeUnmount, computed} from 'vue'
import {fetch_image} from "@/assets/ts/fetch_image";
import {fetch_nearby_beach} from "@/assets/ts/fetch_nearby_beach";

type Activity = { img: string; name: string; reason: string }
type Attraction = { name: string; rating: number }
type Restaurant = { name: string; rating: number, address: string }


// Example activities (replace with API data if available)
const activities = ref<Activity[]>([
  {
    img: 'diving.png',
    name: 'Diving',
    reason: '',
  },
  {
    img: 'swimming.png',
    name: 'Swimming',
    reason: '',
  },
  {
    img: 'fishing.png',
    name: 'Fishing',
    reason: '',
  },
])

const attractions = ref<Attraction[]>([])

const restaurants = ref<Restaurant[]>([])

// Top gallery images
const gallery = ref<string[]>(new Array(3))

const userLat = ref<number | null>(null)
const userLng = ref<number | null>(null)
const errorMsg = ref<string | null>(null)
const nearest = ref<string | null>(null)
const loading = ref(true)

const nearestName = computed(() => {
  if (nearest.value) return nearest.value
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
        fetch_nearby_beach(pos.coords.latitude, pos.coords.longitude)
            .then(async r => {
              nearest.value = r.name
              for (const i in r.photos) {
                gallery.value[i] = r.photos[i]
              }

              for (const i in activities.value) {
                activities.value[i].img = await fetch_image(activities.value[i].img)
                activities.value[i].reason = r.assessment.recommendations[i]
              }

              for (const i in r.recommendations.attractions) {
                let attraction: Attraction = {
                  name: r.recommendations.attractions[i].name,
                  rating: r.recommendations.attractions[i].rating,
                }
                attractions.value.push(attraction)
              }

              for (const i in r.recommendations.restaurants) {
                let restaurant: Restaurant = {
                  name: r.recommendations.restaurants[i].name,
                  rating: r.recommendations.restaurants[i].rating,
                  address: r.recommendations.restaurants[i].address,
                }
                restaurants.value.push(restaurant)
              }
              loading.value = false
            });
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
        <div v-if="loading" class="w-full h-[50vh] object-cover animate-pulse">
          <div class="w-full h-full bg-gray-200"></div>
        </div>
        <img v-else :src="src" alt="" class="w-full h-[50vh] object-cover"/>
      </button>
    </section>

    <section class="flex items-center gap-3 border-b-2"></section>

    <!-- Activity cards -->
    <section id="content" class="grid md:grid-cols-3 gap-4">
      <article v-for="(a, i) in activities" :key="i"
               class="bg-white border rounded-xl overflow-hidden shadow-sm flex flex-col">
        <div v-if="loading" class="w-full h-44 object-cover overflow-hidden">
          <div class="w-full h-full animate-pulse bg-gray-200"></div>
        </div>
        <img v-else :src="a.img" :alt="a.name" class="w-full h-44 object-cover">
        <div class="p-4 flex-1 flex flex-col">
          <div v-if="loading" class="font-semibold text-lg mb-1 line-clamp-2">
            <div class="w-full h-6 animate-pulse bg-gray-200"></div>
          </div>
          <h3 v-else class="font-semibold text-lg mb-1 line-clamp-2">{{ a.name }}</h3>
          <p class="text-slate-600 text-sm flex-1">{{ a.reason }}</p>
        </div>
      </article>
    </section>

    <section v-if="attractions.length > 0" class="flex items-center gap-3 border-b-2"></section>

    <!-- Attraction -->
    <h2 v-if="attractions.length > 0" class="font-semibold text-2xl mb-1 line-clamp-2">🖼️ Attractions</h2>
    <section id="content" class="grid md:grid-cols-3 gap-4">
      <article v-for="(a, i) in attractions" :key="i"
               class="bg-white border rounded-xl overflow-hidden shadow-sm flex flex-col">
        <div class="p-4 flex-1 flex flex-col">
          <h3 class="font-semibold text-lg mb-1 line-clamp-2">{{ a.name }}</h3>
          <p class="text-slate-600 text-sm flex-1">
            <span class="font-semibold">Rating:</span>
            {{ a.rating }}</p>
        </div>
      </article>
    </section>

    <section v-if="restaurants.length > 0" class="flex items-center gap-3 border-b-2"></section>

    <!-- Restaurant -->
    <h2 v-if="restaurants.length > 0" class="font-semibold text-2xl mb-1 line-clamp-2">🍽️ Restaurants</h2>
    <section id="content" class="grid md:grid-cols-3 gap-4">
      <article v-for="(r, i) in restaurants" :key="i"
               class="bg-white border rounded-xl overflow-hidden shadow-sm flex flex-col">
        <div class="p-4 flex-1 flex flex-col">
          <h3 class="font-semibold text-lg mb-1 line-clamp-2">{{ r.name }}</h3>
          <h4 class="text-sm mb-1"><span class="font-semibold">Address: </span>{{ r.address }}</h4>
          <p class="text-slate-600 text-sm flex-1">
            <span class="font-semibold">Rating: </span>
            {{ r.rating }}</p>
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
