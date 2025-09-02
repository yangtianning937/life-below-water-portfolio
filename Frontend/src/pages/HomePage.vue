<script setup>
import {RouterLink} from 'vue-router'
import {ref} from "vue";
import {fetch_activity} from "@/assets/ts/fetch_activity";
import {fetch_image} from "@/assets/ts/fetch_image";

const fact = [
    "Port Phillip was named after Captain Arthur Phillip, the first (1788–92) governor of New South Wales.",
    "The large metropolitan area of Melbourne is located at the head of the bay.",
    "Rivers emptying into the bay include the Little, Werribee, and Yarra.",
    "It’s status as Australia's densest catchment area!",
    "One of the largest enclosed spaces of saltwater in the Southern Hemisphere."
]

const activities = ref([]);
const covers = ref([]);

fetch_activity()
    .then(r => {
      if (r != null) {
        r.forEach(r => {
          r.date = new Date(r.date).toLocaleDateString()
          r.start = new Date(r.start).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})
          r.end = new Date(r.end).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})
          let tags = r.tags.replace("[", "").replace("]", "").split(",");
          r.tags = tags.map(tag => {
            return tag.trim().slice(1, -1)
          });
          get_cover(r.image).then(i => covers.value.push(i));
          activities.value.push(r)
        })
      }
    })

const get_cover = async (name) => {
  return await fetch_image(name);
}
</script>

<template>
  <main class="homepage">
    <!-- Hero -->
    <section class="relative bg-gradient-to-b from-blue-50 to-cyan-50 pt-16 pb-10 text-center">
      <div class="max-w-4xl mx-auto px-5">
        <h1 class="font-extrabold leading-tight">
          <span class="block text-3xl md:text-4xl text-slate-800">Our Oceans Need You.</span>
          <span class="block text-4xl md:text-5xl text-slate-900">Help Us <span class="text-blue-600">Save Them.</span></span>
        </h1>
        <p class="mt-3 text-slate-600">Oceans are the lifeblood of our planet. Become a Water Detective and help protect
          Port Phillip Bay.</p>
        <p class="mt-3 text-slate-600"></p>

      </div>


      <!-- 波浪背景 -->
      <svg class="absolute bottom-0 left-0 right-0 w-full h-[90px]" viewBox="0 0 1440 200" preserveAspectRatio="none"
           aria-hidden="true">
        <path
            d="M0,64L60,80C120,96,240,128,360,122.7C480,117,600,75,720,85.3C840,96,960,160,1080,176C1200,192,1320,160,1380,144L1440,128V200H0Z"
            fill="#0e3a8c" opacity="0.9"/>
      </svg>
    </section>

    <!-- Problem / Challenge -->
    <section id="problem" class="bg-gradient-to-b from-blue-900 to-indigo-700 text-white py-12">
      <div class="max-w-6xl mx-auto px-5">
        <h2 class="text-3xl font-bold mb-2">Welcome, Water Detectives!</h2>
        <p class="text-blue-100">
          Get ready to explore Port Phillip Bay with real data collected since 1984 — it’s your turn to investigate!
          Check water quality, spot changes over time, learn about fish models, and complete real cleanups.
          Then test your knowledge with fun quizzes and unlock fish facts.
        </p>

      </div>
    </section>

    <!-- Interesting Fact -->
    <section class="bg-orange-50 py-10">
      <div class="max-w-6xl mx-auto px-5 grid items-center">
        <h3 class="text-3xl font-bold mt-5 mb-2">✨ Interesting Facts</h3>
        <div class="grid md:grid-cols-3 gap-4 mt-2">
          <div v-for="f in fact">
            <div class="bg-white border rounded-xl p-4 shadow min-h-[120px]">
            <p class="text-slate-600">{{f}}</p></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Activity -->
    <section class="py-10">
      <div class="max-w-5xl mx-auto px-5">
        <h3 class="font-bold mt-5 mb-2 flex justify-between">
          <span class="text-xl">📜 Activity</span>
          <RouterLink
              class="flex justify-between items-center w-auto text-center bg-blue-900 text-white font-semibold px-4 py-2 rounded-xl transition"
              :to="{ name: 'activity'}"
          >
            <span class="pr-2">See More</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right"
                 viewBox="0 0 16 16">
              <path fill-rule="evenodd"
                    d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/>
            </svg>
          </RouterLink>
        </h3>
        <!-- Activity Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <article
              v-for="(a, index) in activities.slice(0, 3)"
              :key="a.id"
              class="bg-white rounded-xl shadow-lg overflow-hidden flex flex-col"
          >
            <img
                :src="covers[index]"
                :alt="a.name"
                class="h-44 w-full object-cover"
                loading="lazy"
                referrerpolicy="no-referrer"
            />

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

              <div class="mt-4">

                <RouterLink
                    class="block w-full text-center bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded-lg transition"
                    :to="{ name: 'activity_register', params: { id: a.id } }"
                >
                  Join
                </RouterLink>
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- Welcome, Water Detectives! + Nutrients -->
    <section class="bg-orange-50 py-10" id="detectives">
      <div class="max-w-5xl mx-auto px-5">


        <h3 class="text-xl font-bold mt-5">🧪 Nutrients Explained</h3>
        <div class="grid md:grid-cols-3 gap-4 mt-2">
          <div class="bg-white border rounded-xl p-4 shadow"><h4 class="font-semibold">DO_mg (Dissolved Oxygen)</h4>
            <p class="text-slate-600">How much oxygen is in water. Too low can sicken or kill fish/crabs.</p></div>
          <div class="bg-white border rounded-xl p-4 shadow"><h4 class="font-semibold">Sal (Salinity)</h4>
            <p class="text-slate-600">How salty the water is. Too far from normal → sea animals struggle.</p></div>
          <div class="bg-white border rounded-xl p-4 shadow"><h4 class="font-semibold">TSS (Total Suspended Solids)</h4>
            <p class="text-slate-600">Cloudiness level. Too much dirt/algae blocks sunlight for plants.</p></div>
          <div class="bg-white border rounded-xl p-4 shadow"><h4 class="font-semibold">N_TOTAL (Total Nitrogen)</h4>
            <p class="text-slate-600">Too much → algal blooms turn water green and harm life.</p></div>
          <div class="bg-white border rounded-xl p-4 shadow"><h4 class="font-semibold">P_TOTAL (Total Phosphorus)</h4>
            <p class="text-slate-600">Tracks pollution from farms/cities — critical for bay health.</p></div>
        </div>
      </div>
    </section>

    <!-- Footer CTA -->
    <section class="py-12 bg-gradient-to-b from-blue-50 to-white">
      <div class="max-w-6xl mx-auto px-5 text-center">
        <h3 class="text-2xl font-bold">Ready to start your investigation?</h3>
        <RouterLink :to="{ name: 'data_hub' }"
                    class="inline-block mt-3 px-6 py-3 rounded-xl bg-blue-900 text-white font-semibold shadow">
          Become a Water Detective
        </RouterLink>
      </div>
    </section>
  </main>
</template>

<style scoped>
.homepage :where(img) {
  pointer-events: none
}
</style>
