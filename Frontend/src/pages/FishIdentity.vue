<!-- src/pages/FishIdentity.vue -->
<template>
  <main class="min-h-screen bg-gradient-to-b from-sky-50 to-blue-50">
    <section class="mx-auto max-w-5xl px-4 py-8">
      <!-- Header -->
      <header class="mb-6">
        <h1 class="text-2xl md:text-3xl font-semibold text-slate-800">
          Tell us about you
        </h1>
        <p class="text-slate-600 mt-1">
          With just a few taps, we'll create your personalised <span class="font-semibold">Fish Buddy</span>.
        </p>
      </header>

      <div class="grid lg:grid-cols-2 gap-6">
        <!-- ===== Left: Form ===== -->
        <section class="bg-white/90 backdrop-blur rounded-2xl shadow p-5 md:p-6">
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
        <section class="bg-white/90 rounded-2xl shadow p-5 md:p-6 relative">
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
            <!-- Progress bar (subtle) -->
            <div class="h-2 w-full bg-slate-100 rounded-full mb-4 overflow-hidden">
              <div class="h-full bg-emerald-400" style="width: 65%"></div>
            </div>

            <!-- Avatar canvas -->
            <div class="rounded-2xl bg-gradient-to-b from-sky-50 to-blue-50 p-4 md:p-6">
              <div class="relative aspect-[16/9] w-full rounded-xl overflow-hidden" ref="avatarWrap">
                <svg
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
              </div>

              <div class="mt-3 flex flex-wrap gap-2">
                <button class="px-3 py-2 rounded-xl bg-slate-800 text-white hover:opacity-95"
                        @click="download('png')">
                  Download PNG
                </button>
                <button class="px-3 py-2 rounded-xl border border-slate-300 hover:border-sky-300"
                        @click="download('svg')">
                  Download SVG
                </button>
                <button v-if="canShare" class="px-3 py-2 rounded-xl border border-slate-300 hover:border-sky-300"
                        @click="shareIt">
                  Share
                </button>
              </div>
            </div>

            <!-- Profile panel -->
            <div class="mt-5">
              <div class="flex items-center gap-2">
                <span class="inline-block h-3 w-3 rounded-full bg-sky-400"></span>
                <h2 class="text-lg md:text-xl font-semibold text-slate-800">
                  {{ displayName }}’s {{ result.commonName }}
                  <span class="text-slate-500">· {{ result.scientific }}</span>
                </h2>
              </div>
              <p class="mt-1 text-slate-600">{{ result.subtitle }}</p>

              <div class="mt-5 grid md:grid-cols-2 gap-4">
                <div class="rounded-xl border border-slate-200 p-4">
                  <h3 class="font-semibold text-slate-800">Personality tags</h3>
                  <p class="mt-1 text-slate-700">{{ result.tags.join(' · ') }}</p>
                </div>
                <div class="rounded-xl border border-slate-200 p-4">
                  <h3 class="font-semibold text-slate-800">Badge suggestion</h3>
                  <p class="mt-1 text-slate-700">{{ result.badge }}</p>
                </div>
                <div class="rounded-xl border border-slate-200 p-4 md:col-span-2">
                  <h3 class="font-semibold text-slate-800">Backstory</h3>
                  <p class="mt-1 text-slate-700">{{ result.backstory }}</p>
                </div>
                <div class="rounded-xl border border-slate-200 p-4">
                  <h3 class="font-semibold text-slate-800">Strengths</h3>
                  <p class="mt-1 text-slate-700">{{ result.strengths.join('; ') }}</p>
                </div>
                <div class="rounded-xl border border-slate-200 p-4">
                  <h3 class="font-semibold text-slate-800">Growth tips</h3>
                  <p class="mt-1 text-slate-700">{{ result.growth.join('; ') }}</p>
                </div>
                <div class="rounded-xl border border-slate-200 p-4 md:col-span-2">
                  <h3 class="font-semibold text-slate-800">Real-world action</h3>
                  <p class="mt-1 text-slate-700">{{ result.action }}</p>
                </div>
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
  </main>
</template>

<script setup lang="ts">
import { nextTick, onMounted, reactive, ref, computed } from 'vue'

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
const result = ref<ReturnType<typeof buildProfile> | null>(null)
const avatarSvg = ref<SVGSVGElement | null>(null)
const avatarWrap = ref<HTMLDivElement | null>(null)

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

async function onGenerate() {
  if (!validate()) return

  ui.loading = true
  ui.progress = 10

  // Simulated quick generation (< 3s); replace with API call when ready.
  const seed = `${form.name}|${form.energy}|${form.traits.join(',')}`
  const tick = setInterval(()=>{ ui.progress = Math.min(95, ui.progress + 7) }, 120)

  // If you have backend, await fetch('/api/identity/generate', { ... })
  await new Promise(r => setTimeout(r, 1200)) // kid-friendly quick load
  result.value = buildProfile(seed, form.energy, form.traits)

  clearInterval(tick)
  ui.progress = 100
  ui.loading = false
  await nextTick()
  avatarWrap.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
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

async function shareIt() {
  if (!result.value) return
  try {
    await (navigator as any).share({
      title: `${displayName.value}’s Fish Buddy`,
      text: `I matched with a ${result.value.commonName}!`
    })
  } catch { /* user cancelled */ }
}

onMounted(() => {
  // prefer reduced motion users still get subtle animations
})
</script>
