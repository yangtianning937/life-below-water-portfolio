<template>
  <div class="min-h-screen bg-gradient-to-b from-blue-50 to-cyan-50 p-8">
    <div class="max-w-6xl mx-auto">
      <!-- Title -->
      <header class="mb-6">
        <h1 class="text-2xl font-bold text-slate-800">Volunteer Activity Participation</h1>
        <p class="text-slate-600">
          Browse upcoming activities. Click an activity to open the registration form.
        </p>
      </header>

      <!-- Activity Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <article
          v-for="a in activities"
          :key="a.id"
          class="bg-white rounded-xl shadow-lg overflow-hidden flex flex-col"
        >
          <img
            :src="a.image"
            :alt="a.title"
            class="h-44 w-full object-cover"
            loading="lazy"
            referrerpolicy="no-referrer"
          />

          <div class="p-5 flex-1 flex flex-col">
            <h3 class="text-lg font-semibold text-slate-800 mb-1">{{ a.title }}</h3>
            <p class="text-slate-600 text-sm line-clamp-3">
              {{ a.description }}
            </p>

            <ul class="mt-3 text-sm text-slate-700 space-y-1">
              <li>📍 {{ a.location }}</li>
              <li>📅 {{ a.date }}</li>
              <li>🕒 {{ a.time }}</li>
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

            <div class="mt-4">
              
              <RouterLink
                class="block w-full text-center bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded-lg transition"
                :to="{ name: 'epic2-register', params: { id: a.id } }"
              >
                Register
              </RouterLink>
            </div>
          </div>
        </article>
      </div>
    </div>
  </div>
</template>

<script setup>
import { activities } from '@/data/activities'
</script>
