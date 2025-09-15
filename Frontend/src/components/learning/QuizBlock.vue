<template>
  <section class="card">
    <h2 class="card__title">Module 4: Quiz Time!</h2>

    <div class="quiz" v-for="(q, i) in visibleQuiz" :key="i">
      <p class="quiz__q"><span class="quiz__no">Q{{ i+1 }}.</span> {{ q.text }}</p>
      <div class="quiz__opts">
        <button
          v-for="opt in q.options"
          :key="opt.key"
          class="btn btn--outline"
          :class="btnStateClass(q, opt.key)"
          @click="choose(q, opt.key)"
          :aria-pressed="q.choice === opt.key"
        >
          {{ opt.label }}
        </button>
      </div>
      <p v-if="q.choice && !isCorrect(q)" class="quiz__fb quiz__fb--warn">Try again!</p>
      <p v-if="q.choice && isCorrect(q)" class="quiz__fb quiz__fb--ok">Nice! That's correct.</p>
    </div>

    <div class="quiz__actions">
      <button class="btn" @click="submitQuiz" :disabled="!allAnswered">Submit</button>
      <button class="btn btn--ghost" @click="resetQuiz">Reset</button>
      <p v-if="submitted" class="quiz__score" aria-live="polite">Score: {{ score }}/{{ visibleQuiz.length }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

type QuizItem = { text: string; options: { key: string; label: string }[]; answer: string; choice?: string | null }
type QuizData = QuizItem[]

const props = defineProps<{ bank: QuizData; pick?: number }>()
const PICK = props.pick ?? 5

const quiz = ref<QuizData>([])
const visibleQuiz = quiz
const submitted = ref(false)
const score = ref(0)
const allAnswered = computed(() => visibleQuiz.value.every(q => q.choice))

function choose(q: QuizItem, key: string){ q.choice = q.choice === key ? null : key }
function isCorrect(q: QuizItem){ return q.choice === q.answer }
function btnStateClass(q: QuizItem, key: string){
  return { selected: q.choice === key, correct: submitted.value && key === q.answer, wrong: submitted.value && q.choice === key && key !== q.answer }
}
function submitQuiz(){ submitted.value = true; score.value = visibleQuiz.value.reduce((a,q)=>a+(q.choice===q.answer?1:0),0) }
function resetQuiz(){ submitted.value = false; score.value = 0; visibleQuiz.value.forEach(q => (q.choice = null)) }

function pickRandom(bank: QuizData, k: number): QuizData{
  const arr = [...bank]
  for(let i = arr.length - 1; i > 0; i--){ const j = Math.floor(Math.random()*(i+1)); [arr[i], arr[j]] = [arr[j], arr[i]] }
  return arr.slice(0, k).map(q => ({ ...q, choice: null }))
}

onMounted(()=>{ quiz.value = pickRandom(props.bank, PICK) })
</script>

<style scoped>
/* 透明卡片 + 变量控色 */
.card{
  background: transparent;
  color: var(--lm-text);
  border: 1px solid #1f2937;
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 10px 28px rgba(15,23,42,.08);
}
.card__title{ margin:0 0 8px; font-size:1.25rem; line-height:1.35; font-weight:800; color: var(--lm-heading); }

/* quiz */
.quiz{ margin-bottom:16px; }
.quiz__q{ margin:0 0 8px; font-weight:800; color: var(--lm-heading); }
.quiz__no{ margin-right:6px; }
.quiz__opts{ display:grid; gap:8px; grid-template-columns:1fr; }
@media (min-width:560px){ .quiz__opts{ grid-template-columns:1fr 1fr; } }
.quiz__fb{ margin:8px 0 0; font-weight:800; }
.quiz__fb--warn{ color:#b45309; }  /* 深琥珀色 */
.quiz__fb--ok{ color:#15803d; }    /* 深绿色 */
.quiz__actions{ display:flex; align-items:center; gap:12px; }
.quiz__score{ margin:0; font-weight:900; }

/* buttons（与父页一致） */
.btn{
  padding:10px 16px; border-radius:12px; border:1px solid #1f2937;
  background:#1f2937; color:var(--lm-on-solid); font-weight:800; cursor:pointer;
  transition:transform .08s ease, box-shadow .08s ease, opacity .15s; box-shadow:0 6px 14px rgba(2,6,23,.15);
}
.btn:hover{ transform:translateY(-1px); }
.btn:disabled{ opacity:.5; cursor:not-allowed; }
.btn--ghost{ background:transparent; color:var(--lm-text); }
.btn--outline{ background:transparent; color:var(--lm-text); border:1px solid #94a3b8; }
.selected{ outline:2px solid #60a5fa; }
.correct.selected{ outline-color:#16a34a; }
.wrong.selected{ outline-color:#e11d48; }

/* 固定浅色方案 */
@media (prefers-color-scheme: dark){
  .card{ background: transparent; color: var(--lm-text); border-color:#1f2937; }
}
</style>
