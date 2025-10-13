<script setup>
import {fetch_activity} from "@/assets/ts/fetch_activity";
import {onMounted, ref, onUnmounted, nextTick, onActivated, onDeactivated, watch, computed} from "vue";
import {useRoute} from "vue-router";
import {fetch_image} from "@/assets/ts/fetch_image";

const route = useRoute();
const activities = ref([]);
const covers = ref([]);
const isLoading = ref(true); // Start with loading true
const hasInitialLoad = ref(false);
const error = ref(null);

// Force refresh flag - use timestamp for uniqueness
const refreshKey = ref(Date.now());

// Component key for forcing re-render
const componentKey = computed(() => `epic2-${refreshKey.value}`);

const loadActivities = async () => {
  // Always start fresh
  isLoading.value = true;
  error.value = null;
  activities.value = [];
  covers.value = [];
  refreshKey.value = Date.now();
  
  try {
    // Force a small delay to ensure clean state
    await new Promise(resolve => setTimeout(resolve, 100));
    
    const response = await fetch_activity();
    
    if (!response || !Array.isArray(response)) {
      activities.value = [];
      covers.value = [];
      return;
    }
    
    if (response.length === 0) {
      activities.value = [];
      covers.value = [];
      return;
    }
    
    // Process activities data
    const processedActivities = response.map((activity, index) => {
      const processed = { ...activity };
      try {
        processed.date = new Date(activity.date).toLocaleDateString();
        processed.start = new Date(activity.start).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
        processed.end = new Date(activity.end).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
        
        // Process tags safely
        if (activity.tags) {
          let tags = activity.tags.replace(/[\[\]]/g, "").split(",");
          processed.tags = tags.map(tag => tag.trim().replace(/['"]/g, ""));
        } else {
          processed.tags = [];
        }
      } catch (e) {
        processed.date = 'Invalid Date';
        processed.start = 'Invalid Time';
        processed.end = 'Invalid Time';
        processed.tags = [];
      }
      return processed;
    });
    
    // Load cover images in parallel with error handling
    const coverPromises = processedActivities.map(async (activity, index) => {
      try {
        if (activity.image) {
          const coverImage = await get_cover(activity.image);
          return coverImage || '';
        }
        return '';
      } catch (e) {
        return '';
      }
    });
    
    const coverImages = await Promise.all(coverPromises);
    
    // Ensure we have the same number of covers as activities
    while (coverImages.length < processedActivities.length) {
      coverImages.push('');
    }
    
    // Update reactive data
    await nextTick();
    activities.value = processedActivities;
    covers.value = coverImages;
    
  } catch (err) {
    console.error('Failed to load activities:', err);
    error.value = err.message || 'Failed to load activities';
    activities.value = [];
    covers.value = [];
  } finally {
    isLoading.value = false;
    hasInitialLoad.value = true;
  }
}

const get_cover = async (name) => {
  return await fetch_image(name);
}

// Simple and reliable loading strategy
onMounted(async () => {
  await nextTick();
  await loadActivities();
});

// Force refresh on route activation (when coming from other pages)
onActivated(async () => {
  await nextTick();
  await loadActivities();
});

// Watch for route changes to force refresh
watch(() => route.path, async (newPath) => {
  if (newPath === '/epic2') {
    // Add a small delay to ensure previous component is fully unmounted
    await new Promise(resolve => setTimeout(resolve, 100));
    await nextTick();
    await loadActivities();
  }
}, { immediate: false });

// Clean up when component is deactivated
onDeactivated(() => {
  // Reset state when leaving the component
  hasInitialLoad.value = false;
  isLoading.value = true;
});
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-blue-50 to-cyan-50 p-8">
    <div class="max-w-6xl mx-auto">
      <!-- Title -->
      <header class="mb-6">
        <div class="flex justify-between items-start">
          <div>
            <h1 class="text-2xl font-bold text-slate-800">Volunteer Activity Participation</h1>
            <p class="text-slate-600">
              Browse upcoming activities. Click an activity to open the registration form.
            </p>
          </div>
          <button
            @click="loadActivities()"
            :disabled="isLoading"
            class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <svg 
              :class="{ 'animate-spin': isLoading }" 
              width="16" 
              height="16" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor"
            >
              <path d="M21 12a9 9 0 11-6.219-8.56" stroke-width="2"/>
            </svg>
            {{ isLoading ? 'Refreshing...' : 'Refresh' }}
          </button>
        </div>
      </header>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex justify-center items-center py-12">
        <div class="text-center">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
          <p class="mt-4 text-slate-600">Loading activities...</p>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="flex justify-center items-center py-12">
        <div class="text-center">
          <div class="text-6xl mb-4">⚠️</div>
          <h3 class="text-xl font-semibold text-slate-700 mb-2">Error Loading Activities</h3>
          <p class="text-slate-600 mb-4">{{ error }}</p>
          <button
            @click="loadActivities()"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="!isLoading && activities.length === 0" class="flex justify-center items-center py-12">
        <div class="text-center">
          <div class="text-6xl mb-4">📋</div>
          <h3 class="text-xl font-semibold text-slate-700 mb-2">No Activities Available</h3>
          <p class="text-slate-600">There are currently no volunteer activities to display.</p>
          <button
            @click="loadActivities()"
            class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>

      <!-- Activity Cards -->
      <div v-else-if="!isLoading && activities.length > 0" :key="componentKey" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <article
            v-for="(a, index) in activities"
            :key="`${a.id}-${refreshKey}`"
            class="bg-white rounded-xl shadow-lg overflow-hidden flex flex-col"
        >
          <div class="h-44 w-full bg-gray-200 relative overflow-hidden">
            <img
                :src="covers[index]"
                :alt="a.name"
                class="h-full w-full object-cover transition-opacity duration-300"
                loading="lazy"
                referrerpolicy="no-referrer"
                @error="$event.target.style.opacity = '0.5'"
                @load="$event.target.style.opacity = '1'"
            />
            <div v-if="!covers[index]" class="absolute inset-0 flex items-center justify-center bg-gray-100">
              <span class="text-gray-400 text-sm">No Image</span>
            </div>
          </div>

          <div class="p-5 flex-1 flex flex-col">
            <h3 class="text-lg font-semibold text-slate-800 mb-1">{{ a.name }}</h3>
            <p class="text-slate-600 text-sm line-clamp-3">
              {{ a.description }}
            </p>

            <ul class="mt-3 text-sm text-slate-700 space-y-1">
              <li>📍 {{ a.location }}</li>
              <li>📅 {{ a.date }}</li>
              <li>🕒 {{ a.start }} - {{ a.end }}</li>
            </ul>

            <div class="mt-3 flex flex-wrap gap-2">
              <span
                  v-for="t in a.tags"
                  :key="t"
                  class="text-xs px-2 py-1 rounded-full bg-slate-100"
              >
                #{{ t }}
              </span>
            </div>

<!--            <div class="mt-4">-->

<!--              <RouterLink-->
<!--                  class="block w-full text-center bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded-lg transition"-->
<!--                  :to="{ name: 'activity_register', params: { id: a.id } }"-->
<!--              >-->
<!--                Join-->
<!--              </RouterLink>-->
<!--            </div>-->
          </div>
        </article>
      </div>
    </div>
  </div>
</template>
