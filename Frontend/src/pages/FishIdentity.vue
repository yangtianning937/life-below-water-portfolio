<!-- src/pages/FishIdentity.vue -->
<template>
  <main class="min-h-screen bg-gradient-to-b from-sky-50 to-blue-50">
    <section class="mx-auto max-w-7xl px-6 py-8">
      <!-- Header -->
      <header class="mb-6">
        <h1 class="text-2xl md:text-3xl font-semibold text-slate-800">
          Tell us about you
        </h1>
        <p class="text-slate-600 mt-1">
          With just a few taps, we'll create your personalised <span class="font-semibold">Fish Buddy</span>.
        </p>
      </header>

      <div class="grid lg:grid-cols-2 gap-8">
        <!-- ===== Left: Form ===== -->
        <section class="bg-white rounded-xl shadow-lg p-6 lg:p-8">
          <form @submit.prevent="onGenerate" novalidate>
            <!-- Name -->
            <label for="name" class="block text-sm font-medium text-slate-700">Name <span class="text-rose-600">(required)</span></label>
            <input
              id="name"
              v-model.trim="form.name"
              type="text"
              required
              placeholder="e.g., Sunny"
              class="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 outline-none focus:ring-2 focus:ring-sky-300"
              :aria-invalid="!!errors.name"
              @keydown.enter.prevent="onGenerate"
            />
            <p v-if="errors.name" class="mt-1 text-sm text-rose-600" role="alert">{{ errors.name }}</p>

            <!-- Energy -->
            <div class="mt-6">
              <p class="text-sm font-medium text-slate-700">Energy level</p>
              <div class="mt-3 flex gap-2">
                <button
                  v-for="lvl in energyLevels" :key="lvl"
                  type="button"
                  class="px-3 py-2 rounded-full border transition
                         hover:border-sky-300"
                  :class="form.energy===lvl ? 'bg-sky-50 border-sky-300' : 'border-slate-200'"
                  @click="form.energy = lvl"
                  :aria-pressed="form.energy===lvl"
                >
                  {{ lvl }}
                </button>
              </div>
            </div>

            <!-- Traits -->
            <div class="mt-6">
              <p class="text-sm font-medium text-slate-700">
                My traits <span class="text-slate-500">(pick 1–3)</span>
              </p>
              <div class="mt-3 flex flex-wrap gap-2">
                <button
                  v-for="t in allTraits" :key="t"
                  type="button"
                  class="px-3 py-2 rounded-full border transition select-none"
                  :class="selected(t)
                    ? 'bg-emerald-50 border-emerald-300'
                    : 'border-slate-200 hover:border-sky-300'"
                  @click="toggleTrait(t)"
                  :disabled="!selected(t) && form.traits.length>=3"
                  :aria-pressed="selected(t)"
                >
                  {{ t }}
                </button>
              </div>
              <p class="mt-2 text-xs text-slate-500">
                Options: {{ allTraits.join(', ') }}
              </p>
              <p v-if="errors.traits" class="mt-1 text-sm text-rose-600" role="alert">{{ errors.traits }}</p>
            </div>

            <!-- Actions -->
            <div class="mt-6 flex items-center gap-3">
              <button
                type="submit"
                class="inline-flex items-center gap-2 rounded-2xl px-4 py-3 font-semibold shadow
                       bg-gradient-to-r from-emerald-400 to-sky-400 text-white
                       hover:opacity-95 disabled:opacity-50 disabled:cursor-not-allowed">
                <span>✨ Generate</span>
              </button>

              <button
                type="button"
                class="rounded-2xl px-4 py-3 font-medium border border-slate-200 hover:border-sky-300"
                @click="onSurprise"
              >
                Surprise me
              </button>
            </div>
          </form>
        </section>

        <!-- ===== Right: Result ===== -->
        <section class="bg-white rounded-xl shadow-lg p-6 lg:p-8 relative">
          <!-- Loading skeleton -->
          <div v-if="ui.loading" class="absolute inset-0 rounded-2xl bg-white/70 backdrop-blur-sm z-10">
            <div class="h-1 w-full bg-slate-100 rounded-full overflow-hidden mt-4">
              <div class="h-full bg-sky-400 transition-all" :style="{ width: ui.progress + '%' }"></div>
            </div>
            <div class="p-6 animate-pulse">
              <div class="h-56 rounded-2xl bg-slate-100 mb-4"></div>
              <div class="h-4 w-2/3 bg-slate-100 rounded mb-2"></div>
              <div class="h-4 w-1/2 bg-slate-100 rounded mb-6"></div>
              <div class="grid grid-cols-2 gap-4">
                <div class="h-20 bg-slate-100 rounded"></div>
                <div class="h-20 bg-slate-100 rounded"></div>
              </div>
            </div>
          </div>

          <!-- Result -->
          <template v-if="result">
            <!-- Progress bar (completed) -->
            <div class="h-2 w-full bg-slate-100 rounded-full mb-4 overflow-hidden">
              <div class="h-full bg-emerald-400 transition-all duration-500" style="width: 100%"></div>
            </div>

            <!-- Avatar Gallery -->
            <div class="rounded-xl bg-gradient-to-br from-slate-50 to-blue-50 p-6 shadow-md border border-slate-200">
              <!-- Gallery Header -->
              <div class="text-center mb-6">
                <h3 class="text-xl font-bold text-slate-800 mb-2">Your Fish Buddy Gallery</h3>
                <p class="text-slate-600 text-sm">Compare the real fish with your personalized cartoon avatar</p>
              </div>

              <!-- Image Comparison -->
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Real Fish Card -->
                <div class="group">
                  <div class="relative aspect-[4/3] rounded-2xl overflow-hidden bg-gradient-to-br from-slate-100 to-slate-200 shadow-lg border-2 border-white/50 group-hover:shadow-xl transition-all duration-300">
                    <img 
                      v-if="realImageUrl && !realImageUrl.includes('placeholder')"
                      :src="realImageUrl"
                      alt="Real fish image"
                      class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      @error="realImageError = true"
                    />
                    <div v-else class="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-slate-100 to-slate-200">
                      <div class="w-16 h-16 rounded-full bg-slate-300 flex items-center justify-center mb-3">
                        <svg class="w-8 h-8 text-slate-500" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd"/>
                        </svg>
                      </div>
                      <span class="text-slate-500 text-sm font-medium">Loading Real Image...</span>
                    </div>
                    
                    <!-- Image Badge -->
                    <div class="absolute top-3 left-3 bg-blue-600 text-white px-3 py-1 rounded-full text-xs font-semibold shadow-lg">
                      Real Fish
                    </div>
                  </div>
                  
                  <!-- Real Image Info -->
                  <div class="mt-4 text-center">
                    <h4 class="font-semibold text-slate-800 mb-1">{{ result?.commonName }}</h4>
                    <p class="text-sm text-slate-600">From Wikipedia</p>
                  </div>
                </div>
                
                <!-- Cartoon Avatar Card -->
                <div class="group">
                  <div class="relative aspect-[4/3] rounded-2xl overflow-hidden bg-gradient-to-br from-cyan-100 to-teal-200 shadow-lg border-2 border-white/50 group-hover:shadow-xl transition-all duration-300">
                    <img 
                      v-if="cartoonImageBase64"
                      :src="cartoonImageBase64"
                      alt="Cartoon fish avatar"
                      class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <svg
                      v-else
                  ref="avatarSvg"
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-full h-full"
                  viewBox="0 0 800 450"
                  role="img"
                  :aria-label="`Cartoon avatar of ${result.commonName}`"
                >
                  <!-- water -->
                  <defs>
                    <linearGradient id="gWater" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stop-opacity="0"/>
                      <stop offset="60%" stop-color="#E6F4FF"/>
                      <stop offset="100%" stop-color="#DFF2FF"/>
                    </linearGradient>
                    <linearGradient id="gBody" x1="0" y1="0" x2="1" y2="0">
                      <stop :stop-color="avatarPalette.bodyFrom" offset="0%"/>
                      <stop :stop-color="avatarPalette.bodyTo" offset="100%"/>
                    </linearGradient>
                  </defs>

                  <rect x="0" y="0" width="800" height="450" fill="url(#gWater)"/>
                  <!-- bubbles -->
                  <circle v-for="(b,i) in bubbles" :key="i"
                          :cx="b.x" :cy="b.y" :r="b.r" fill="#BFE9FF" fill-opacity="0.55"/>
                  <!-- fish body -->
                  <ellipse :cx="400" :cy="260" :rx="190" :ry="110" fill="url(#gBody)"/>
                  <!-- stripes/dots by energy -->
                  <template v-if="form.energy==='High'">
                    <rect v-for="i in 5" :key="'s'+i" :x="250+i*35" :y="190" width="10" height="140" opacity="0.18"/>
                  </template>
                  <template v-else-if="form.energy==='Low'">
                    <circle v-for="i in 10" :key="'d'+i" :cx="270+i*23" :cy="230+(i%2)*20" r="6" opacity="0.18"/>
                  </template>
                  <!-- tail -->
                  <polygon :points="tailPoints" :fill="avatarPalette.tail"/>
                  <!-- fins -->
                  <ellipse :cx="330" :cy="260" :rx="55" :ry="18" :fill="avatarPalette.fin" opacity="0.7"/>
                  <ellipse :cx="470" :cy="260" :rx="55" :ry="18" :fill="avatarPalette.fin" opacity="0.7"/>
                  <!-- eye -->
                  <circle cx="560" cy="240" r="22" fill="#FFFFFF"/>
                  <circle cx="566" cy="246" r="9" fill="#1F2937"/>
                </svg>
                    
                    <!-- Cartoon Badge -->
                    <div class="absolute top-3 left-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-3 py-1 rounded-full text-xs font-semibold shadow-lg">
                      AI Cartoon
                    </div>
                  </div>
                  
                  <!-- Cartoon Info -->
                  <div class="mt-4 text-center">
                    <h4 class="font-semibold text-slate-800 mb-1">{{ result?.subtitle || 'Your Avatar' }}</h4>
                    <p class="text-sm text-slate-600">AI Generated</p>
                  </div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="mt-8 flex flex-wrap justify-center gap-3">
                <button v-if="realImageUrl && !realImageUrl.includes('placeholder')" 
                        class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600 text-white hover:bg-blue-700 transition-colors shadow-md hover:shadow-lg">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"/>
                  </svg>
                  Download Real
                </button>
                
                <button v-if="cartoonImageBase64" 
                        class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:from-purple-700 hover:to-pink-700 transition-all shadow-md hover:shadow-lg">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"/>
                  </svg>
                  Download Cartoon
                </button>
                
                <button v-else class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-600 text-white hover:bg-slate-700 transition-colors shadow-md hover:shadow-lg"
                        @click="download('png')">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"/>
                  </svg>
                  Download PNG
                </button>
                
                <button v-if="!cartoonImageBase64" class="inline-flex items-center gap-2 px-4 py-2 rounded-xl border-2 border-slate-300 text-slate-700 hover:border-slate-400 hover:bg-slate-50 transition-colors"
                        @click="download('svg')">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"/>
                  </svg>
                  Download SVG
                </button>
                
                <button v-if="canShare" class="inline-flex items-center gap-2 px-4 py-2 rounded-xl border-2 border-emerald-300 text-emerald-700 hover:border-emerald-400 hover:bg-emerald-50 transition-colors"
                        @click="shareIt">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z"/>
                  </svg>
                  Share
                </button>
              </div>
            </div>

            <!-- Two Column Layout -->
            <div class="mt-8 grid grid-cols-1 xl:grid-cols-2 gap-8">
              
              <!-- Feature 1: Personified Fish ID Card -->
              <div class="bg-white rounded-xl p-6 shadow-md border border-slate-200">
                <div class="text-center mb-6">
                  <div class="inline-flex items-center gap-3 bg-gradient-to-r from-purple-100 to-pink-100 px-6 py-3 rounded-full">
                    <div class="w-4 h-4 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 animate-pulse"></div>
                    <h2 class="text-lg font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                      Personified Fish ID Card
                </h2>
              </div>
                </div>

                <!-- Personal Info -->
                <div class="space-y-4">
                  <!-- Name and Age -->
                  <div class="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-4 border border-purple-200">
                    <div class="flex items-center gap-3 mb-2">
                      <div class="w-8 h-8 rounded-lg bg-purple-500 flex items-center justify-center">
                        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"/>
                        </svg>
                      </div>
                      <h3 class="font-bold text-slate-800">Personal Info</h3>
                    </div>
                    <div class="space-y-2 text-sm">
                      <p><span class="font-semibold text-purple-600">Name:</span> {{ result.personInfo?.Name }}</p>
                      <p><span class="font-semibold text-purple-600">Species:</span> {{ result.personInfo?.Species }}</p>
                      <p><span class="font-semibold text-purple-600">Age:</span> {{ result.personInfo?.Age }}</p>
                    </div>
                  </div>

                  <!-- Personality -->
                  <div class="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-xl p-4 border border-emerald-200">
                    <div class="flex items-center gap-3 mb-2">
                      <div class="w-8 h-8 rounded-lg bg-emerald-500 flex items-center justify-center">
                        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                      </div>
                      <h3 class="font-bold text-slate-800">Personality</h3>
                    </div>
                    <p class="text-sm text-slate-700">{{ result.personInfo?.Personality }}</p>
                  </div>

                  <!-- Hobbies -->
                  <div class="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl p-4 border border-blue-200">
                    <div class="flex items-center gap-3 mb-2">
                      <div class="w-8 h-8 rounded-lg bg-blue-500 flex items-center justify-center">
                        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
                        </svg>
                      </div>
                      <h3 class="font-bold text-slate-800">Hobbies</h3>
                    </div>
                    <p class="text-sm text-slate-700">{{ result.personInfo?.Hobbies }}</p>
                  </div>

                  <!-- Special Feature -->
                  <div class="bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl p-4 border border-amber-200">
                    <div class="flex items-center gap-3 mb-2">
                      <div class="w-8 h-8 rounded-lg bg-amber-500 flex items-center justify-center">
                        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/>
                        </svg>
                      </div>
                      <h3 class="font-bold text-slate-800">Special Feature</h3>
                    </div>
                    <p class="text-sm text-slate-700">{{ result.personInfo?.Special_Feature }}</p>
                  </div>
                </div>
              </div>

              <!-- Feature 2: Complete Base Marine Identity -->
              <div class="bg-white rounded-xl p-6 shadow-md border border-slate-200">
                <div class="text-center mb-6">
                  <div class="inline-flex items-center gap-3 bg-gradient-to-r from-blue-100 to-cyan-100 px-6 py-3 rounded-full">
                    <div class="w-4 h-4 rounded-full bg-gradient-to-r from-blue-500 to-cyan-500 animate-pulse"></div>
                    <h2 class="text-lg font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
                      Complete Base Marine Identity
                    </h2>
                  </div>
                </div>

                <!-- Marine Info -->
                <div class="space-y-4">
                  <!-- Species Names -->
                  <div class="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl p-4 border border-blue-200">
                    <div class="flex items-center gap-3 mb-2">
                      <div class="w-8 h-8 rounded-lg bg-blue-500 flex items-center justify-center">
                        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/>
                        </svg>
                      </div>
                      <h3 class="font-bold text-slate-800">Species Names</h3>
                    </div>
                    <div class="text-sm">
                      <p class="font-semibold text-blue-600">{{ result.baseInfo?.Species_Name_EN }}</p>
                    </div>
                  </div>

                  <!-- Core Feature -->
                  <div class="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-4 border border-purple-200">
                    <div class="flex items-center gap-3 mb-2">
                      <div class="w-8 h-8 rounded-lg bg-purple-500 flex items-center justify-center">
                        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/>
                        </svg>
                      </div>
                      <h3 class="font-bold text-slate-800">Core Feature</h3>
                    </div>
                    <p class="text-sm text-slate-700">{{ result.baseInfo?.Core_Feature_CN }}</p>
                  </div>

                  <!-- Age & Size -->
                  <div class="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-xl p-4 border border-emerald-200">
                    <div class="flex items-center gap-3 mb-2">
                      <div class="w-8 h-8 rounded-lg bg-emerald-500 flex items-center justify-center">
                        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/>
                        </svg>
                      </div>
                      <h3 class="font-bold text-slate-800">Age & Size</h3>
                    </div>
                    <p class="text-sm text-slate-700">{{ result.baseInfo?.Age_Size_Description_CN }}</p>
                  </div>

                  <!-- Personality -->
                  <div class="bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl p-4 border border-amber-200">
                    <div class="flex items-center gap-3 mb-2">
                      <div class="w-8 h-8 rounded-lg bg-amber-500 flex items-center justify-center">
                        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                      </div>
                      <h3 class="font-bold text-slate-800">Personality</h3>
                    </div>
                    <p class="text-sm text-slate-700">{{ result.baseInfo?.Personality_CN }}</p>
                  </div>

                  <!-- Habitat -->
                  <div class="bg-gradient-to-br from-teal-50 to-cyan-50 rounded-xl p-4 border border-teal-200">
                    <div class="flex items-center gap-3 mb-2">
                      <div class="w-8 h-8 rounded-lg bg-teal-500 flex items-center justify-center">
                        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
                        </svg>
                      </div>
                      <h3 class="font-bold text-slate-800">Habitat</h3>
                    </div>
                    <p class="text-sm text-slate-700">{{ result.baseInfo?.Habitat_CN }}</p>
                  </div>

                  <!-- Fun Story -->
                  <div class="bg-gradient-to-br from-rose-50 to-pink-50 rounded-xl p-4 border border-rose-200">
                    <div class="flex items-center gap-3 mb-2">
                      <div class="w-8 h-8 rounded-lg bg-rose-500 flex items-center justify-center">
                        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M18 13V5a2 2 0 00-2-2H4a2 2 0 00-2 2v8a2 2 0 002 2h3l3 3 3-3h3a2 2 0 002-2zM5 7a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1zm1 3a1 1 0 100 2h3a1 1 0 100-2H6z" clip-rule="evenodd"/>
                        </svg>
                      </div>
                      <h3 class="font-bold text-slate-800">Fun Story</h3>
                    </div>
                    <p class="text-sm text-slate-700">{{ result.baseInfo?.Fun_Story_CN }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Action Panel -->
            <div class="mt-6 bg-gradient-to-br from-emerald-50 to-teal-50 rounded-xl p-6 shadow-md border border-emerald-200">
              <div class="flex items-center gap-3 mb-4">
                <div class="w-8 h-8 rounded-lg bg-emerald-500 flex items-center justify-center">
                  <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <h3 class="font-bold text-slate-800">Take Action</h3>
                </div>
              <div class="bg-emerald-500 text-white p-4 rounded-lg">
                <p class="text-sm font-medium">{{ result.action }}</p>
              </div>
            </div>
          </template>

          <!-- Empty state -->
          <div v-else class="text-slate-500">
            <p>Fill the form and press <span class="font-semibold">Generate</span> to meet your Fish Buddy.</p>
          </div>
        </section>
      </div>
    </section>

    <!-- Error Message -->
    <FullscreenMessage
      v-model="errorMessage.show"
      :title="errorMessage.title"
      :icon="'⚠️'"
      confirm-text="Try Again"
      cancel-text="Cancel"
      :persistent="false"
      @confirm="retryGeneration"
      @close="closeErrorMessage"
    >
      <p>{{ errorMessage.message }}</p>
    </FullscreenMessage>
  </main>
</template>

<script setup lang="ts">
import { nextTick, onMounted, reactive, ref, computed } from 'vue'
import { fetch_fish_info } from '../assets/ts/fetch_fish_info'
import { fetch_fish_avatar } from '../assets/ts/fetch_fish_avatar'
import FullscreenMessage from '../components/FullscreenMessage.vue'

type EnergyLevel = 'Low' | 'Medium' | 'High'
type Trait = 'Curious' | 'Careful' | 'Shy' | 'Brave' | 'Explorer' | 'Gentle' | 'Steady' | 'Lively'

const energyLevels: EnergyLevel[] = ['Low', 'Medium', 'High']
const allTraits: Trait[] = ['Curious','Careful','Shy','Brave','Explorer','Gentle','Steady','Lively']

const form = reactive<{ name: string; energy: EnergyLevel; traits: Trait[] }>({
  name: '',
  energy: 'Medium',
  traits: []
})

const errors = reactive<{ name?: string; traits?: string }>({})

const ui = reactive({ loading: false, progress: 0 })
const result = ref<any | null>(null)
const avatarSvg = ref<SVGSVGElement | null>(null)
const avatarWrap = ref<HTMLDivElement | null>(null)
const cartoonImageBase64 = ref<string>('')
const realImageUrl = ref<string>('')
const realImageError = ref<boolean>(false)

// Error message state
const errorMessage = ref<{ show: boolean; title: string; message: string }>({
  show: false,
  title: '',
  message: ''
})

// Cache for fish info to avoid repeated API calls
const fishInfoCache = ref<Map<string, any>>(new Map())

const canShare = 'share' in navigator

function selected(t: Trait) { return form.traits.includes(t) }
function toggleTrait(t: Trait) {
  if (selected(t)) {
    form.traits = form.traits.filter(x => x !== t)
  } else if (form.traits.length < 3) {
    form.traits = [...form.traits, t]
  }
}

function validate() {
  errors.name = form.name ? '' : 'Please enter your name.'
  errors.traits = form.traits.length >= 1 ? '' : 'Pick at least one trait (up to three).'
  return !errors.name && !errors.traits
}

/** Seeded PRNG so same inputs => same fish */
function seededRandom(seed: string) {
  let h = 2166136261
  for (let i = 0; i < seed.length; i++) h = (h ^ seed.charCodeAt(i)) * 16777619
  return () => {
    // xorshift
    h ^= h << 13; h ^= h >>> 17; h ^= h << 5
    return Math.abs(h) / 0xffffffff
  }
}

type Species = {
  key: string
  commonName: string
  scientific: string
  palette: { from: string; to: string; fin: string; tail: string }
  facts: string[]
  habitat: string
}

const SPECIES: Species[] = [
  { key:'weedy-seadragon', commonName:'Little Seadragon', scientific:'Weedy Seadragon',
    palette:{ from:'#7dd3fc', to:'#34d399', fin:'#67e8f9', tail:'#10b981' },
    facts:['Patient observer','Loves seagrass','Gentle swimmer'], habitat:'seagrass beds' },
  { key:'port-jackson-shark', commonName:'Port Jackson Shark', scientific:'Heterodontus portusjacksoni',
    palette:{ from:'#93c5fd', to:'#60a5fa', fin:'#a7f3d0', tail:'#3b82f6' },
    facts:['Blunt head','Night explorer','Egg case maker'], habitat:'rocky reefs' },
  { key:'bigbelly-seahorse', commonName:'Big-belly Seahorse', scientific:'Hippocampus abdominalis',
    palette:{ from:'#a7f3d0', to:'#34d399', fin:'#99f6e4', tail:'#059669' },
    facts:['Great at hiding','Clings to kelp','Curious eyes'], habitat:'kelp and pylons' },
  { key:'snapper', commonName:'Snapper', scientific:'Chrysophrys auratus',
    palette:{ from:'#fda4af', to:'#fdba74', fin:'#fecaca', tail:'#fb7185' },
    facts:['Schooling fish','Strong swimmer','Shiny scales'], habitat:'bays and inshore reefs' },
  { key:'flathead', commonName:'Flathead', scientific:'Platycephalus spp.',
    palette:{ from:'#fef08a', to:'#86efac', fin:'#fde68a', tail:'#84cc16' },
    facts:['Bottom sitter','Sand camo','Quick bursts'], habitat:'sandy bottoms' },
  { key:'banjo-ray', commonName:'Banjo Ray', scientific:'Trygonorrhina fasciata',
    palette:{ from:'#c7d2fe', to:'#93c5fd', fin:'#bfdbfe', tail:'#6366f1' },
    facts:['Guitar shape','Glides slowly','Likes shallow bays'], habitat:'sandy bays' },
]

function buildProfile(seed: string, energy: EnergyLevel, traits: Trait[]) {
  const rnd = seededRandom(seed + energy + traits.join('-'))
  const idx = Math.floor(rnd() * SPECIES.length)
  const sp = SPECIES[idx]
  const tags = Array.from(new Set([...traits, energy==='Low'?'Observer':energy==='High'?'Lively':'Steady']))
  const badge = ({
    Low: 'Seagrass Saver',
    Medium: 'Bay Buddy',
    High: 'Reef Ranger'
  } as const)[energy]

  const nameLine = `If you were a ${sp.scientific.toLowerCase()}, you'd explore ${sp.habitat} and make new friends.`
  const strengths = [
    traits.includes('Curious') ? 'Curiosity' : 'Detail-focused',
    energy === 'High' ? 'Energetic' : energy === 'Low' ? 'Patient' : 'Balanced',
    ['Imaginative', 'Team-minded', 'Kind'][Math.floor(rnd() * 3)]
  ]
  const growth = energy === 'High'
    ? ['Try a calm observation game', 'Share one fact with a friend']
    : energy === 'Low'
      ? ['Join a small teamwork task', 'Record one new observation daily']
      : ['Try one new skill this week', 'Teach someone your favourite fact']

  const action = 'Do a “Pick 3” mini clean-up with your family to protect local habitats.'

  return {
    ...sp,
    subtitle: nameLine,
    tags,
    badge,
    backstory: `You live around Port Phillip Bay’s ${sp.habitat}. ${sp.facts[0]}. When the water gets murky after rain, you rest and wait. On sunny days you ${sp.facts[1].toLowerCase()}.`,
    strengths,
    growth,
    action
  }
}

const displayName = computed(() => form.name || 'Your')

/** Avatar palette derived from species + energy for subtle variety */
const avatarPalette = computed(() => {
  if (!result.value) return { bodyFrom:'#9bdcfb', bodyTo:'#67e8f9', fin:'#99f6e4', tail:'#34d399' }
  const { palette } = result.value
  const tweak = form.energy === 'High' ? 1 : form.energy === 'Low' ? -1 : 0
  const shift = (hex: string) => {
    // very small lighten/darken
    const n = parseInt(hex.slice(1), 16)
    const r = Math.min(255, Math.max(0, ((n>>16)&255) + tweak*10))
    const g = Math.min(255, Math.max(0, ((n>>8)&255) + tweak*10))
    const b = Math.min(255, Math.max(0, (n&255) + tweak*6))
    return `#${(r<<16|g<<8|b).toString(16).padStart(6,'0')}`
  }
  return {
    bodyFrom: shift(palette.from),
    bodyTo: shift(palette.to),
    fin: shift(palette.fin),
    tail: shift(palette.tail)
  }
})

const bubbles = Array.from({ length: 10 }).map((_,i)=>({ x: 80+i*70, y: 320-(i%5)*40, r: 6+(i%3)*2 }))
const tailPoints = computed(() => {
  // simple triangle attached to body
  const w = 90, h = 90, cx = 210, cy = 260
  return `${cx},${cy} ${cx-w},${cy-h/2} ${cx-w},${cy+h/2}`
})

// Helper functions for better code organization
function showError(title: string, message: string) {
  errorMessage.value = { show: true, title, message }
}

function updateProgress(increment: number = 7) {
  ui.progress = Math.min(90, ui.progress + increment)
}

async function fetchFishInfoWithCache(name: string) {
  const cacheKey = name.toLowerCase().trim()
  
  // Check cache first
  if (fishInfoCache.value.has(cacheKey)) {
    console.log('Using cached fish info for:', name)
    return fishInfoCache.value.get(cacheKey)
  }
  
  // Fetch from API
  const fishInfo = await fetch_fish_info(name)
  if (fishInfo) {
    fishInfoCache.value.set(cacheKey, fishInfo)
  }
  return fishInfo
}

async function fetchCartoonAvatar(wikiImageUrl: string) {
  if (!wikiImageUrl || wikiImageUrl.includes('placeholder') || wikiImageUrl.includes('error')) {
    console.log('Wikipedia image URL is invalid or placeholder, skipping cartoon processing')
    return ''
  }
  
  try {
    const avatarResponse = await fetch_fish_avatar(wikiImageUrl)
    if (avatarResponse?.success && avatarResponse?.cartoon_image) {
      return avatarResponse.cartoon_image
    } else {
      console.warn('Cartoon avatar generation failed:', avatarResponse?.error || 'Unknown error')
      return ''
    }
  } catch (err) {
    console.error('Failed to fetch cartoon avatar:', err)
    return ''
  }
}

function transformFishData(fishInfo: any) {
  const baseInfo = fishInfo.Complete_Base_Marine_Identity
  const personInfo = fishInfo.Personified_Fish_ID_Card
  
  // Process tags: combine user-selected traits with energy level
  const energyTag = form.energy === 'Low' ? 'Observer' : form.energy === 'High' ? 'Lively' : 'Steady'
  const allTags = form.traits.length > 0 
    ? [...form.traits, energyTag]
    : ['Curious', 'Gentle', energyTag]
  
  return {
    commonName: baseInfo.Species_Name_EN,
    scientific: baseInfo.Species_Name_EN,
    subtitle: `Your marine buddy - ${personInfo.Name}`,
    tags: allTags,
    badge: form.energy === 'Low' ? 'Seagrass Saver' : form.energy === 'High' ? 'Reef Ranger' : 'Bay Buddy',
    backstory: baseInfo.Personality_CN || baseInfo.Habitat_CN,
    strengths: [
      `Age: ${personInfo.Age}`,
      personInfo.Personality
    ],
    growth: [
      personInfo.Hobbies,
      baseInfo.Special_Feature || 'Unique marine characteristics'
    ],
    action: 'Do a "Pick 3" mini clean-up with your family to protect local habitats.',
    palette: SPECIES[0].palette,
    
    // Separate the two features
    personInfo: personInfo,
    baseInfo: baseInfo
  }
}

async function onGenerate() {
  if (!validate()) return

  ui.loading = true
  ui.progress = 10

  try {
    const tick = setInterval(() => updateProgress(), 120)

    // Step 1: Fetch fish info (with caching)
    updateProgress(20)
    const fishInfo = await fetchFishInfoWithCache(form.name)
    
    if (!fishInfo) {
      clearInterval(tick)
      showError(
        'Failed to Fetch Fish Info',
        'Unable to retrieve fish information. Please check your connection and try again.'
      )
      ui.loading = false
      return
    }

    // Step 2: Store real image URL
    updateProgress(20)
    const wikiImageUrl = fishInfo.Complete_Base_Marine_Identity?.Wikipedia_Image_URL
    realImageUrl.value = wikiImageUrl || ''
    
    // Step 3: Fetch cartoon avatar (async, non-blocking)
    updateProgress(10)
    const cartoonImage = await fetchCartoonAvatar(wikiImageUrl)

    // Step 4: Transform data and update UI
    updateProgress(10)
    result.value = transformFishData(fishInfo)
    cartoonImageBase64.value = cartoonImage

    // Complete
    clearInterval(tick)
    ui.progress = 100
    ui.loading = false
    await nextTick()
    avatarWrap.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  } catch (error) {
    console.error('Generation failed:', error)
    showError(
      'Generation Failed',
      'Something went wrong while generating your fish buddy. Please try again.'
    )
    ui.loading = false
  }
}

function onSurprise() {
  const names = ['Sunny','Kai','River','Misty','Coral','Skye']
  form.name = names[Math.floor(Math.random()*names.length)]
  form.energy = energyLevels[Math.floor(Math.random()*energyLevels.length)]
  const shuffled = [...allTraits].sort(()=>Math.random()-0.5)
  form.traits = shuffled.slice(0, 1 + Math.floor(Math.random()*3)) as Trait[]
  onGenerate()
}

async function download(kind: 'png'|'svg') {
  if (!avatarSvg.value) return
  if (kind === 'svg') {
    const xml = new XMLSerializer().serializeToString(avatarSvg.value)
    const blob = new Blob([xml], { type: 'image/svg+xml' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${form.name || 'fish-avatar'}.svg`
    a.click()
    URL.revokeObjectURL(url)
  } else {
    // SVG -> PNG
    const svg = avatarSvg.value
    const xml = new XMLSerializer().serializeToString(svg)
    const img = new Image()
    const url = URL.createObjectURL(new Blob([xml], { type: 'image/svg+xml' }))
    img.onload = () => {
      const canvas = document.createElement('canvas')
      canvas.width = svg.viewBox.baseVal.width || svg.clientWidth
      canvas.height = svg.viewBox.baseVal.height || svg.clientHeight
      const ctx = canvas.getContext('2d')!
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height)
      URL.revokeObjectURL(url)
      canvas.toBlob((blob) => {
        if (!blob) return
        const a = document.createElement('a')
        a.href = URL.createObjectURL(blob)
        a.download = `${form.name || 'fish-avatar'}.png`
        a.click()
        URL.revokeObjectURL(a.href)
      })
    }
    img.src = url
  }
}

async function downloadRealImage() {
  if (!realImageUrl.value || realImageUrl.value.includes('placeholder')) return
  
  try {
    const response = await fetch(realImageUrl.value)
    const blob = await response.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${form.name || 'fish'}-real.jpg`
    a.click()
    URL.revokeObjectURL(url)
  } catch (err) {
    console.error('Failed to download real image:', err)
    errorMessage.value = {
      show: true,
      title: 'Download Failed',
      message: 'Unable to download the real fish image. Please try again.'
    }
  }
}

async function downloadCartoon() {
  if (!cartoonImageBase64.value) return
  
  // Convert base64 to blob and download
  const base64Data = cartoonImageBase64.value.split(',')[1]
  const byteCharacters = atob(base64Data)
  const byteNumbers = new Array(byteCharacters.length)
  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i)
  }
  const byteArray = new Uint8Array(byteNumbers)
  const blob = new Blob([byteArray], { type: 'image/png' })
  
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${form.name || 'fish-avatar'}-cartoon.png`
  a.click()
  URL.revokeObjectURL(url)
}

async function shareIt() {
  if (!result.value) return
  try {
    await (navigator as any).share({
      title: `${displayName.value}'s Fish Buddy`,
      text: `I matched with a ${result.value.commonName}!`
    })
  } catch { /* user cancelled */ }
}

onMounted(() => {
  // prefer reduced motion users still get subtle animations
})

// Error message handlers
function closeErrorMessage() {
  errorMessage.value.show = false
}

function retryGeneration() {
  errorMessage.value.show = false
  onGenerate()
}

// Utility function to clear cache
function clearCache() {
  fishInfoCache.value.clear()
  console.log('Fish info cache cleared')
}

// Auto-clear cache periodically to prevent memory issues
setInterval(() => {
  if (fishInfoCache.value.size > 10) {
    clearCache()
  }
}, 300000) // Clear every 5 minutes if cache is large
</script>
