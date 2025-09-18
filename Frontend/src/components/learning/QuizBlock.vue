<template>
  <!-- 一页一题；← 返回；→ 为“检查/下一题/提交” -->
  <section class="card q" tabindex="0"
           @keyup.left.prevent="prevPage"
           @keyup.right.prevent="tryNextByKey">
    <div class="q__header">
      <h2 class="card__title">Module 4: Quiz Time!</h2>
      <div class="q__progress"
           role="progressbar"
           :aria-valuenow="progressPct"
           aria-valuemin="0"
           aria-valuemax="100">
        <div class="q__progress-bar" :style="{ width: progressPct + '%' }"></div>
      </div>
    </div>

    <!-- 当前页 -->
    <div v-if="cur" class="quiz">
      <p class="quiz__q"><span class="quiz__no">Q{{ page }}.</span> {{ cur.text }}</p>
      <img v-if="cur.image" class="quiz__img" :src="cur.image" alt="" />

      <div class="quiz__opts">
        <button
          v-for="opt in cur.options"
          :key="opt.key"
          class="btn btn--outline"
          :class="btnStateClass(cur, opt.key)"
          @click="choose(cur, opt.key)"
          :disabled="cur._state==='ok' || submitted"
          :aria-pressed="cur.choice === opt.key"
        >
          {{ opt.label }}
        </button>
      </div>

      <p v-if="cur._state==='ok'"    class="quiz__fb quiz__fb--ok">{{ cur.correct   || 'Nice! That’s correct.' }}</p>
      <p v-if="cur._state==='wrong'" class="quiz__fb quiz__fb--warn">{{ cur.incorrect || 'Try again!' }}</p>
    </div>

    <!-- 底部导航 -->
    <div class="q__footer">
      <button class="arrow arrow--left" :disabled="page===1" @click="prevPage"><span>Previous</span></button>

      <div class="q__dots" role="tablist" aria-label="Quiz pages">
        <button v-for="n in total" :key="n"
                class="dot" :class="{active: page===n}"
                :disabled="n > unlockedPage"
                @click="go(n)"
                :aria-selected="page===n"></button>
      </div>

      <!-- 右键：未答对=Check；已答对且非最后页=Next；最后页=Submit -->
      <button v-if="cur && cur._state!=='ok'"
              class="arrow arrow--right"
              :disabled="!cur.choice"
              @click="checkCurrent"><span>Check</span></button>

      <button v-else-if="page<total"
              class="arrow arrow--right"
              @click="nextPage"><span>Next</span></button>

      <button v-else
              class="arrow arrow--right"
              :disabled="!allCorrect"
              @click="submitQuiz"><span>Submit</span></button>
    </div>

    <div v-if="submitted" class="q__summary">
      <p class="quiz__score">Score: {{ score }}/{{ total }}</p>
      <button class="btn btn--ghost" @click="resetQuiz">Reset</button>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

/** 分模块题库：{ m1:[], m2:[], m3:[] } */
const props = defineProps({ bankByModule: { type: Object, required: true } })

/* ------- 构建 3 题（各模块抽 1） ------- */
const quiz = ref([])
const page = ref(1)
const submitted = ref(false)
const score = ref(0)

const total = computed(() => quiz.value.length || 3)
const cur   = computed(() => quiz.value[page.value - 1] || null)

/* 进度条：已答/总题数 */
const answeredCount = computed(() =>
  quiz.value.filter(q => q._state !== 'idle').length
)
const progressPct = computed(() =>
  Math.round((answeredCount.value / total.value) * 100)
)
const allCorrect = computed(() => quiz.value.every(q => q._state === 'ok'))

/* 只能去到“已解锁”的最大页 */
const unlockedPage = computed(() => {
  const i = quiz.value.findIndex(q => q._state !== 'ok')
  return i === -1 ? total.value : i + 1
})

function pickOne(arr = []) {
  if (!arr.length) return null
  const i = Math.floor(Math.random() * arr.length)
  return { ...arr[i], choice: null, _state: 'idle' }
}
function buildThree(bank) {
  const out = []
  const a = pickOne(bank.m1); if (a) out.push(a)
  const b = pickOne(bank.m2); if (b) out.push(b)
  const c = pickOne(bank.m3); if (c) out.push(c)
  return out
}

/* ------- 交互 ------- */
function choose(q, key){ if (q._state==='ok') return; q.choice = q.choice === key ? null : key }
function checkCurrent(){
  if (!cur.value || !cur.value.choice) return
  cur.value._state = (cur.value.choice === cur.value.answer) ? 'ok' : 'wrong'
}
function nextPage(){ if (page.value < unlockedPage.value) page.value++ }
function tryNextByKey(){
  if (!cur.value) return
  if (cur.value._state === 'ok') nextPage()
  else checkCurrent()
}
function prevPage(){ if (page.value > 1) page.value-- }
function go(n){ if (n <= unlockedPage.value) page.value = n }

function btnStateClass(q, key){
  const isSelected = q.choice === key
  const isAnswer   = key === q.answer
  return {
    selected: isSelected,
    correct:  q._state === 'ok'    && isAnswer,
    wrong:    q._state === 'wrong' && isSelected && !isAnswer
  }
}

function submitQuiz(){
  submitted.value = true
  score.value = quiz.value.reduce((a, q) => a + (q.choice === q.answer ? 1 : 0), 0)
}
function resetQuiz(){
  submitted.value = false
  score.value = 0
  page.value = 1
  quiz.value.forEach(q => { q.choice = null; q._state = 'idle' })
}

onMounted(() => { quiz.value = buildThree(props.bankByModule) })
</script>

<style scoped>
/* 卡片容器 */
.card{
  background: transparent;
  color: var(--lm-text);
  border: 1px solid #1f2937;
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 10px 28px rgba(15,23,42,.08);
}
.card__title{ margin:0 0 10px; font-size:1.25rem; line-height:1.35; font-weight:800; color: var(--lm-heading); }

/* 进度条（按答对数增长） */
/* 进度条（按已答数量增长） */
.q__progress{
  width:100%;
  height:10px;
  background:#dbeafe;
  border-radius:999px;
  overflow:hidden;
  border:1px solid #93c5fd;
  margin-top:6px;
}
.q__progress-bar{
  height:100%;
  width:0;
  background:#2563eb;
  transition: width .25s ease;
}


/* 一题布局 */
.quiz{ margin-top: 12px; }
.quiz__q{ margin:0 0 8px; font-weight:800; color: var(--lm-heading); }
.quiz__no{ margin-right:6px; }
.quiz__img{ width: 280px; max-width: 100%; display:block; margin: 8px 0 8px; border-radius: 10px; }
.quiz__opts{ display:grid; gap:8px; grid-template-columns:1fr; }
@media (min-width:560px){ .quiz__opts{ grid-template-columns:1fr 1fr; } }
.quiz__fb{ margin:8px 0 0; font-weight:800; }
.quiz__fb--warn{ color:#b45309; }
.quiz__fb--ok{ color:#15803d; }

/* 底部导航（箭头） */
.q__footer{ margin-top: 16px; position: relative; display:flex; align-items:center; justify-content:space-between; }
.arrow{ position:relative; border:none; cursor:pointer; font-weight:800; padding:12px 20px; color:#0b1220; background:#e8b6ae; }
.arrow:disabled{ opacity:.5; cursor:not-allowed; }
.arrow span{ position:relative; z-index:1; }
.arrow--left{ padding-left:46px; }
.arrow--left::before{ content:''; position:absolute; left:-28px; top:0; width:0; height:0; border-top:26px solid transparent; border-bottom:26px solid transparent; border-right:28px solid #e8b6ae; }
.arrow--right{ background:#0ea5b5; color:#fff; padding-right:46px; }
.arrow--right::after{ content:''; position:absolute; right:-28px; top:0; width:0; height:0; border-top:26px solid transparent; border-bottom:26px solid transparent; border-left:28px solid #0ea5b5; }

/* 圆点 */
.q__dots{ display:flex; gap:8px; align-items:center; justify-content:center; position:absolute; left:50%; transform:translateX(-50%); }
.dot{ width:10px; height:10px; border-radius:999px; background:#94a3b8; border:0; cursor:pointer; }
.dot.active{ background:#0ea5b5; }
.dot:disabled{ opacity:.5; cursor:not-allowed; }

/* 成绩与重置 */
.q__summary{ margin-top: 10px; display:flex; gap:12px; align-items:center; }
.quiz__score{ margin:0; font-weight:900; }

/* 通用按钮 */
.btn{
  padding:10px 16px; border-radius:12px; border:1px solid #1f2937;
  background:#1f2937; color:var(--lm-on-solid); font-weight:800; cursor:pointer;
  transition:transform .08s ease, box-shadow .08s ease, opacity .15s; box-shadow:0 6px 14px rgba(2,6,23,.15);
}
.btn:hover{ transform:translateY(-1px); }
.btn:disabled{ opacity:.55; cursor:not-allowed; }

/* 选项按钮（锁定时视觉更灰一点） */
.btn--ghost{ background:transparent; color:var(--lm-text); }
.btn--outline{ background:transparent; color:var(--lm-text); border:1px solid #94a3b8; }
.btn--outline:disabled{ color:#94a3b8; background:#f5f7fb; }
.selected{ outline:2px solid #60a5fa; }
.correct.selected{ outline-color:#16a34a; }
.wrong.selected{   outline-color:#e11d48; }

/* 固定浅色方案 */
@media (prefers-color-scheme: dark){
  .card{ background: transparent; color: var(--lm-text); border-color:#1f2937; }
}
</style>
