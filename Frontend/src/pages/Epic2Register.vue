<template>
  <div class="min-h-screen bg-gradient-to-b from-blue-50 to-cyan-50 p-8">
    <div class="max-w-3xl mx-auto bg-white rounded-xl shadow-lg p-7">
      <!-- Title -->
      <header class="mb-5">
        <h1 class="text-2xl font-bold text-slate-800">Register for Activity</h1>
        <p class="text-slate-600" v-if="activity">
          You’re registering for: <strong>{{ activity.name }}</strong>
          ({{ activity.location }} · {{ activity.date }} · {{ activity.start }} - {{ activity.end }})
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
              v-model="form.full_name"
              required
              class="w-full border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              placeholder="Enter your name"
          />
        </div>

        <div>
          <label class="block font-semibold mb-1 text-slate-700">
            Parent's Name
          </label>
          <input
              v-model="form.parent"
              required
              class="w-full border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              placeholder="Enter parent's name"
          />
        </div>

        <div>
          <label class="block font-semibold mb-1 text-slate-700">
            Parent's Name (optional)
          </label>
          <input
              v-model="form.optional_parent"
              class="w-full border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              placeholder="Enter parent's name"
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
              class="w-full resize-none border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              placeholder="e.g., bringing kids, accessibility needs…"
          ></textarea>
        </div>

        <div class="text-slate-600">
          <span class="pr-1">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor"
                 class="bi bi-info-circle-fill text-yellow-400 inline-block" viewBox="0 0 16 16">
            <path
                d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2"/>
          </svg>
          </span>
          <span>Before the activity, parents are requested to confirm that their child is in suitable physical condition to
          participate. If the child has any allergies, chronic illnesses, or other special circumstances, please inform
          the organizer in advance. Parents are also asked to ensure that their child arrives at the meeting point on
          time on the day of the activity and is accompanied by a guardian for drop-off and pick-up.</span>
        </div>

        <div class="flex items-center gap-3">
          <button
              :disabled="submitting"
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
          Thanks, {{ form.full_name }}! Your registration for
          <strong>{{ activity.name }}</strong> has been recorded.
        </p>
      </div>
      <!-- Fail banner -->
      <div v-else class="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
        <p class="text-red-700 font-medium">
          Sorry, {{ form.full_name }}! Your registration for
          <strong>{{ activity.name }}</strong> failed.
        </p>
        <p v-if="errors" class="text-red-700 font-medium">
          Message: {{errors}}.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import {reactive, ref} from 'vue'
import {useRoute} from 'vue-router'
import {fetch_activity} from "@/assets/ts/fetch_activity";
import {post_form} from "@/assets/ts/post_form";
import router from "@/router";

const route = useRoute()
const currentId = route.params.id // string

const activity = ref(null);
fetch_activity(currentId)
    .then(r => {
      r[0].date = new Date(r[0].date).toLocaleDateString()
      r[0].start = new Date(r[0].start).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})
      r[0].end = new Date(r[0].end).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})
      activity.value = r[0]
    })

const form = reactive({full_name: '', email: '', parent: '', optional_parent: '', notes: ''})
const submitting = ref(false)
const submitted = ref(null)
const errors = ref(null)

function handleSubmit() {
  submitting.value = true;
  post_form(
      currentId,
      form.full_name,
      [form.parent, form.optional_parent],
      form.email,
      form.notes
  ).then(r => {
    if (r != null) {
      if (r.msg === "success") {
        submitted.value = true
        console.log('Registration payload:', {activityId: currentId, ...form})
        setTimeout(() => {
          router.push({ name: 'activity'})
        }, 1000)
      } else {
        submitted.value = false
        submitting.value = false
        errors.value = r.msg
      }
    } else {
      submitted.value = false
      submitting.value = false
      errors.value = "Error"
    }
  });
}
</script>
