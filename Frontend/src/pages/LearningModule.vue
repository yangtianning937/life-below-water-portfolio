<template>
  <div class="lm" @keyup="onKey" tabindex="0" aria-label="Learning Module">
    <!-- Header -->
    <header class="lm__header">
      <h1 class="lm__title">Port Phillip Bay Learning Module</h1>

      <!-- Progress -->
      <div class="lm__progress" role="progressbar" :aria-valuenow="progressPct" aria-valuemin="0" aria-valuemax="100">
        <div class="lm__progress-bar" :style="{ width: progressPct + '%' }"></div>
      </div>

      <!-- Tabs -->
      <nav class="lm__tabs" aria-label="Modules">
        <button
          v-for="(m, i) in modules"
          :key="m.key"
          class="lm__tab"
          :class="{ 'is-active': i === idx.module }"
          @click="goModule(i)"
          :aria-current="i===idx.module ? 'page' : false"
        >
          {{ m.title }}
        </button>
      </nav>
    </header>

    <!-- Body -->
    <main class="lm__body">
      <ModuleIntro    v-if="cur.key==='m1'" />
      <ModuleBeaches  v-else-if="cur.key==='m2'" />
      <ModuleProtect  v-else-if="cur.key==='m3'" />
      <QuizBlock v-else-if="cur.key==='m4'" :bank-by-module="learningQuiz" />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, onMounted, onUnmounted } from 'vue'
import ModuleIntro from '../components/learning/ModuleIntro.vue';
import ModuleBeaches from '../components/learning/ModuleBeaches.vue'
import ModuleProtect from '../components/learning/ModuleProtect.vue'
import QuizBlock     from '../components/learning/QuizBlock.vue'
import learningQuiz from '../data/learningQuiz.randomized.js'



type ModuleKey = 'm1'|'m2'|'m3'|'m4'
const modules = [
  { key: 'm1' as ModuleKey, title: 'Intro to Marine Ecosystem' },
  { key: 'm2' as ModuleKey, title: 'Beaches Near Port Phillip Bay' },
  { key: 'm3' as ModuleKey, title: 'Protect Our Bay' },
  { key: 'm4' as ModuleKey, title: 'Quiz Time!' },
]

const idx = reactive({ module: 0 })
const cur = computed(() => modules[idx.module])
const progressPct = computed(() => Math.round(((idx.module + 1) / modules.length) * 100))

function goModule(i: number) { idx.module = i }
function next() { if (idx.module < modules.length - 1) idx.module++ }
function prev() { if (idx.module > 0) idx.module-- }
function complete() { alert('🎉 Great job! You completed all modules.') }
function onKey(e: KeyboardEvent) {
  if (e.key === 'ArrowRight') next()
  if (e.key === 'ArrowLeft') prev()
  if (e.key === 'Enter' && cur.value.key !== 'm4') next()
}


onMounted(() => document.body.classList.add('bg-learning'))
onUnmounted(() => document.body.classList.remove('bg-learning'))
</script>

<style scoped>
/* 让视口高度撑满，保证背景可见 */
:global(html, body, #app) { height: 100%; }


:global(body.bg-learning) {
  background-color: #DFF3F7;
  color-scheme: light;

  /* === 统一的颜色变量 === */
  --lm-text:        #0f172a;        /* 默认文字 */
  --lm-heading:     #0b1220;        /* 标题文字 */
  --lm-muted:       #475569;        /* 次级说明 */
  --lm-on-solid:    #ffffff;        /* 实心按钮上的文字 */
  --lm-tab:         #111827;        /* 顶部 Tab 文字 */
  --lm-tab-active:  #1e3a8a;        /* 选中 Tab 背景/边框 */
  --lm-progress-bg: #e6eefb;
  --lm-progress-fg: #1e40af;
}

/* 容器透明，让 body 的淡蓝透出来；并设置全页默认文字色 */
.lm {
  background: transparent;
  min-height: 100vh;
  padding: 16px 20px 40px;
  max-width: 980px;
  margin: 0 auto;
  outline: none;
  color: var(--lm-text);
  font-family: ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial;
}

/* Header */
.lm__header { position: sticky; top: 0; background: transparent; backdrop-filter: none; padding: 12px 0 14px; z-index: 2; }
.lm__title  { font-size: 1.7rem; font-weight: 800; margin: 0 0 12px; line-height: 1.2; color: var(--lm-heading); }

/* Progress */
.lm__progress { height: 8px; background: var(--lm-progress-bg); border-radius: 999px; overflow: hidden; margin-bottom: 12px; border: 1px solid #d7e3ff; }
.lm__progress-bar { height: 100%; background: var(--lm-progress-fg); transition: width .25s ease; }

/* Tabs */
.lm__tabs { display: flex; flex-wrap: wrap; gap: 8px; }
.lm__tab  { border: 1px solid #c7d2fe; background: #fff; color: var(--lm-tab); padding: 8px 14px; border-radius: 999px; font-size: .95rem; font-weight: 700; cursor: pointer; transition: transform .08s ease; }
.lm__tab:hover { transform: translateY(-1px); }
.lm__tab.is-active { background: var(--lm-tab-active); color: var(--lm-on-solid); border-color: var(--lm-tab-active); box-shadow: 0 6px 14px rgba(30,58,138,.25); }

/* Body, Footer & buttons */
.lm__body   { margin-top: 16px; }
.lm__footer { display: flex; justify-content: space-between; gap: 12px; margin-top: 18px; }

.btn { padding: 10px 16px; border-radius: 12px; border: 1px solid #1f2937; background: #1f2937; color: var(--lm-on-solid); font-weight: 800; cursor: pointer; transition: transform .08s ease, box-shadow .08s ease, opacity .15s; box-shadow: 0 6px 14px rgba(2,6,23,.15); }
.btn:hover { transform: translateY(-1px); }
.btn:disabled { opacity: .5; cursor: not-allowed; }
.btn--ghost { background: transparent; color: var(--lm-text); }
</style>

