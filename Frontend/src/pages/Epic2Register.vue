<template>
  <div class="min-h-screen bg-gradient-to-b from-blue-50 to-cyan-50 p-8">
    <div class="max-w-3xl mx-auto bg-white rounded-xl shadow-lg p-7">
      <!-- Title -->
      <header class="mb-5">
        <h1 class="text-2xl font-bold text-slate-800">Register for Activity</h1>
        <p class="text-slate-600" v-if="activity">
          You’re registering for: <strong>{{ activity.title }}</strong>
          ({{ activity.location }} · {{ activity.date }} · {{ activity.time }})
        </p>
      </header>

      <!-- Not Found -->
      <div v-if="!activity" class="text-slate-600">
        Activity not found.
        <RouterLink class="text-blue-600 hover:underline" :to="{ name: 'activity' }">
          Back to list
        </RouterLink>
      </div>

      <!-- Form -->
      <form v-else @submit.prevent="handleSubmit" class="space-y-5">
        <div>
          <label class="block font-semibold mb-1 text-slate-700">Full Name</label>
          <input
              v-model="form.name"
              required
              class="w-full border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              placeholder="Enter your name"
          />
        </div>

        <div>
          <label class="block font-semibold mb-1 text-slate-700">Email Address</label>
          <input
              type="email"
              v-model="form.email"
              required
              class="w-full border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              placeholder="Enter your email"
          />
        </div>

        <div>
          <label class="block font-semibold mb-1 text-slate-700">
            Any special requirements? (optional)
          </label>
          <textarea
              v-model="form.notes"
              rows="3"
              class="w-full border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              placeholder="e.g., bringing kids, accessibility needs…"
          ></textarea>
        </div>

        <div class="flex items-center gap-3">
          <button
              type="submit"
              class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-5 py-2 rounded-lg"
          >
            Submit
          </button>
          <RouterLink :to="{ name: 'activity' }"
                      class="bg-red-600 hover:bg-red-700 text-white font-semibold px-5 py-2 rounded-lg">
            Cancel
          </RouterLink>
        </div>
      </form>

      <!-- Success banner -->
      <div v-if="submitted" class="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
        <p class="text-green-700 font-medium">
          Thanks, {{ form.name }}! Your registration for
          <strong>{{ activity.title }}</strong> has been recorded.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import {computed, reactive, ref} from 'vue'
import {useRoute} from 'vue-router'
import {activities} from '@/data/activities'

const route = useRoute()
const currentId = route.params.id // string

const activity = computed(() => activities.find(a => a.id === currentId))

const form = reactive({name: '', email: '', notes: ''})
const submitted = ref(false)

function handleSubmit() {
  submitted.value = true

  console.log('Registration payload:', {activityId: currentId, ...form})
}
</script>
