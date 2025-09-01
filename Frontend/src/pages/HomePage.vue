<script setup>
import { RouterLink } from 'vue-router'
import c1 from '@/assets/images/collage1.jpg'
import c2 from '@/assets/images/collage2.jpg'
import c3 from '@/assets/images/collage3.jpg'
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
        <p class="mt-3 text-slate-600">Oceans are the lifeblood of our planet. Become a Water Detective and help protect Port Phillip Bay.</p>
        <p class="mt-3 text-slate-600"></p>

      </div>

      

      <!-- 波浪背景 -->
      <svg class="absolute bottom-0 left-0 right-0 w-full h-[90px]" viewBox="0 0 1440 200" preserveAspectRatio="none" aria-hidden="true">
        <path d="M0,64L60,80C120,96,240,128,360,122.7C480,117,600,75,720,85.3C840,96,960,160,1080,176C1200,192,1320,160,1380,144L1440,128V200H0Z"
              fill="#0e3a8c" opacity="0.9"/>
      </svg>
    </section>

    <!-- Problem / Challenge -->
    <section id="problem" class="bg-gradient-to-b from-blue-900 to-indigo-700 text-white py-12">
      <div class="max-w-6xl mx-auto px-5">
        <h2 class="text-3xl font-bold mb-2">What’s the problem?</h2>
        <p class="text-blue-100">
          Marine education is often missing in school curricula. Kids (8–12) and beachgoers in Melbourne
          lack engaging ways to learn about water quality, local fish species, and real-world conservation.
        </p>
        <p class="text-blue-100 mt-2">
          How might we make marine education engaging and accessible so people understand Port Phillip Bay
          and are willing to protect it?
        </p>
        <ul class="list-disc pl-6 mt-3 space-y-1 text-blue-100">
          <li><strong>Awareness gap</strong>: Hard to connect textbooks with real bay data.</li>
          <li><strong>Action gap</strong>: Few easy entries to participate (e.g., cleanups, citizen science).</li>
        </ul>
      </div>
    </section>

    <!-- Our Solution + Collage -->
    <section class="py-10">
      <div class="max-w-6xl mx-auto px-5 grid md:grid-cols-2 gap-7 items-center">
        <div class="relative h-[320px]">
          <img :src="c1" alt="Coral Reef" class="absolute top-0 left-4 w-72 h-48 object-cover rounded-xl shadow -rotate-3">
          <img :src="c2" alt="Seagrass & Turtles" class="absolute top-12 left-28 w-72 h-48 object-cover rounded-xl shadow z-10">
          <img :src="c3" alt="Rocky Reef" class="absolute top-24 left-52 w-72 h-48 object-cover rounded-xl shadow rotate-2">
        </div>
        <div>
          <h3 class="text-2xl font-bold mb-2">Our Solution</h3>
          <p class="text-slate-600">
            Interactive data hub (Epic 1), volunteer activities (Epic 2), fish models (Epic 3), and quizzes (Epic 5).
            Learn by exploring real data and take action through community activities.
          </p>
        </div>
      </div>
    </section>

    <!-- Welcome, Water Detectives! + Nutrients -->
    <section class="bg-orange-50 py-10" id="detectives">
      <div class="max-w-5xl mx-auto px-5">
        <h2 class="text-2xl font-extrabold">Welcome, Water Detectives!</h2>
        <p class="text-slate-700 mt-1">
          Get ready to explore Port Phillip Bay with real data collected since 1984 — it’s your turn to investigate!
          Check water quality, spot changes over time, learn about fish models, and complete real cleanups.
          Then test your knowledge with fun quizzes and unlock fish facts.
        </p>

        <h3 class="text-xl font-bold mt-5">🧪 Nutrients Explained</h3>
        <div class="grid md:grid-cols-3 gap-4 mt-2">
          <div class="bg-white border rounded-xl p-4 shadow"><h4 class="font-semibold">DO_mg (Dissolved Oxygen)</h4><p class="text-slate-600">How much oxygen is in water. Too low can sicken or kill fish/crabs.</p></div>
          <div class="bg-white border rounded-xl p-4 shadow"><h4 class="font-semibold">Sal (Salinity)</h4><p class="text-slate-600">How salty the water is. Too far from normal → sea animals struggle.</p></div>
          <div class="bg-white border rounded-xl p-4 shadow"><h4 class="font-semibold">TSS (Total Suspended Solids)</h4><p class="text-slate-600">Cloudiness level. Too much dirt/algae blocks sunlight for plants.</p></div>
          <div class="bg-white border rounded-xl p-4 shadow"><h4 class="font-semibold">N_TOTAL (Total Nitrogen)</h4><p class="text-slate-600">Too much → algal blooms turn water green and harm life.</p></div>
          <div class="bg-white border rounded-xl p-4 shadow"><h4 class="font-semibold">P_TOTAL (Total Phosphorus)</h4><p class="text-slate-600">Tracks pollution from farms/cities — critical for bay health.</p></div>
        </div>
      </div>
    </section>

    <!-- Footer CTA -->
    <section class="py-12 bg-gradient-to-b from-blue-50 to-white">
      <div class="max-w-6xl mx-auto px-5 text-center">
        <h3 class="text-2xl font-bold">Ready to start your investigation?</h3>
        <RouterLink :to="{ name: 'data_hub' }" class="inline-block mt-3 px-6 py-3 rounded-xl bg-blue-900 text-white font-semibold shadow">
          Become a Water Detective
        </RouterLink>
      </div>
    </section>
  </main>
</template>

<style scoped>
.homepage :where(img){pointer-events:none}
</style>
