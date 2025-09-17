<template>
  <section class="card q" tabindex="0"
           @keyup.left.prevent="prevPage"
           @keyup.right.prevent="tryNextByKey">
    <div class="q__header">
      <h2 class="card__title">Marine Quiz</h2>
      <div class="q__progress" role="progressbar" :aria-valuenow="progressPct" aria-valuemin="0" aria-valuemax="100">
        <div class="q__progress-bar" :style="{ width: progressPct + '%' }"></div>
      </div>
    </div>

    <!-- 当前题 -->
    <div v-if="cur" class="quiz">
      <p class="quiz__q"><span class="quiz__no">Q{{ page }}.</span> {{ cur.text }}</p>

      <!-- ===== MCQ（每个选项有图片+名字） ===== -->
      <div v-if="isMCQ(cur)" class="mcq">
        <img v-if="cur.promptImg" class="mcq__prompt" :src="cur.promptImg" alt="" />
        <div class="mcq__opts">
          <button v-for="opt in cur.options" :key="opt.key"
                  class="mcq__card"
                  :class="btnStateClass(cur, opt.key)"
                  @click="choose(cur, opt.key)"
                  :disabled="cur._state==='ok' || submitted"
                  :aria-pressed="cur.choice === opt.key">
            <img class="mcq__img" :src="opt.img" :alt="opt.name" />
            <span class="mcq__name">{{ opt.name }}</span>
          </button>
        </div>
      </div>

      <!-- ===== True/False ===== -->
      <div v-else-if="isTF(cur)" class="quiz__opts quiz__opts--tf">
        <button class="btn btn--outline"
                :class="btnStateClass(cur, 't')"
                @click="choose(cur, 't')"
                :disabled="cur._state==='ok' || submitted">True</button>
        <button class="btn btn--outline"
                :class="btnStateClass(cur, 'f')"
                @click="choose(cur, 'f')"
                :disabled="cur._state==='ok' || submitted">False</button>
      </div>

      <!-- ===== Click & Match（左侧动物+图，右侧特征下拉选择） ===== -->
      <div v-else-if="isMatch(cur)" class="match">
        <div class="match__row" v-for="left in cur.left" :key="left.key">
          <div class="match__left">
            <img class="match__img" :src="left.img" :alt="left.label" />
            <div class="match__label">{{ left.label }}</div>
          </div>
          <select class="match__select"
                  v-model="cur.choices[left.key]"
                  :disabled="cur._state==='ok' || submitted">
            <option disabled value="">Please select the corresponding feature.</option>
            <option v-for="r in cur.right" :key="r.key" :value="r.key">{{ r.label }}</option>
          </select>
        </div>
      </div>

      <!-- ===== Name the Pic（题干一张图片，选名字） ===== -->
      <div v-else-if="isPIC(cur)" class="pic">
        <img class="pic__img" :src="cur.image" alt="" />
        <div class="pic__opts">
          <button v-for="opt in cur.options" :key="opt.key"
                  class="btn btn--outline"
                  :class="btnStateClass(cur, opt.key)"
                  @click="choose(cur, opt.key)"
                  :disabled="cur._state==='ok' || submitted">
            {{ opt.name }}
          </button>
        </div>
      </div>

      <!-- 反馈 -->
      <p v-if="cur._state==='ok'"    class="quiz__fb quiz__fb--ok">{{ cur.correct   || 'Nice! That’s correct.' }}</p>
      <p v-if="cur._state==='wrong'" class="quiz__fb quiz__fb--warn">{{ cur.incorrect || 'Try again!' }}</p>
    </div>

    <!-- 底部导航（右侧按钮：Check / Next / Submit） -->
    <div class="q__footer">
      <button class="arrow arrow--left" :disabled="page===1" @click="prevPage"><span>Previous</span></button>

      <div class="q__dots" role="tablist" aria-label="Quiz pages">
        <button v-for="n in total" :key="n"
                class="dot" :class="{active: page===n}"
                :disabled="n > unlockedPage"
                @click="go(n)"></button>
      </div>

      <button v-if="cur && cur._state!=='ok'"
              class="arrow arrow--right"
              :disabled="!isAnswered(cur)"
              @click="checkCurrent"><span>Check</span></button>

      <button v-else-if="page<total"
              class="arrow arrow--right"
              @click="nextPage"><span>Next</span></button>

      <button v-else
              class="arrow arrow--right"
              :disabled="!allCorrect"
              @click="submitQuiz"><span>Submit</span></button>
    </div>

    <!-- 成绩与重置 -->
    <div v-if="submitted" class="q__summary">
      <p class="quiz__score">Score: {{ score }}/{{ total }}</p>
      <button class="btn btn--ghost" @click="resetQuiz">Reset</button>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import bank from '@/data/marineQuiz'

// 组卷：5题；四类至少各1，+1个随机补位
const total = 5
const quiz = ref([]) // 统一附加：choice / _state；match 再附加 choices:{}
const page = ref(1)
const submitted = ref(false)
const score = ref(0)

const cur = computed(() => quiz.value[page.value - 1] || null)
const answeredCount = computed(() => quiz.value.filter(q => isAnswered(q)).length)
const progressPct    = computed(() => Math.round((answeredCount.value / total) * 100))
const allCorrect     = computed(() => quiz.value.every(q => q._state === 'ok'))

// 未解锁之前的最大页：必须按顺序答对
const unlockedPage = computed(() => {
  const i = quiz.value.findIndex(q => q._state !== 'ok')
  return i === -1 ? total : i + 1
})

// 题型判断
const isMCQ  = q => (q?.type || '').toLowerCase() === 'mcq'
const isTF   = q => (q?.type || '').toLowerCase() === 'tf'
const isMatch= q => (q?.type || '').toLowerCase() === 'match'
const isPIC  = q => (q?.type || '').toLowerCase() === 'pic'

// 是否“已答”：用于进度条/Check 按钮是否可点
function isAnswered(q){
  if (isMatch(q)) {
    const leftKeys = (q.left || []).map(l => l.key)
    return leftKeys.length && leftKeys.every(k => q.choices && q.choices[k])
  }
  return q.choice !== null && q.choice !== undefined && q.choice !== ''
}

// 选择（mcq / tf / pic）
function choose(q, key){
  if (q._state === 'ok') return
  q.choice = (q.choice === key) ? null : key
}

// 检查当前题
function checkCurrent(){
  if (!cur.value) return

  if (isMatch(cur.value)) {
    // 全部匹配完才判分
    if (!isAnswered(cur.value)) return
    const ans = cur.value.answer || {}
    const sel = cur.value.choices || {}
    const ok = Object.keys(ans).every(k => ans[k] === sel[k])
    cur.value._state = ok ? 'ok' : 'wrong'
  } else {
    if (!cur.value.choice) return
    cur.value._state = (cur.value.choice === cur.value.answer) ? 'ok' : 'wrong'
  }
}

// 翻页
function nextPage(){ if (page.value < unlockedPage.value) page.value++ }
function tryNextByKey(){ if (!cur.value) return; (cur.value._state === 'ok') ? nextPage() : checkCurrent() }
function prevPage(){ if (page.value > 1) page.value-- }
function go(n){ if (n <= unlockedPage.value) page.value = n }

// 选项状态 class
function btnStateClass(q, key){
  const isSelected = q.choice === key
  const isAnswer   = key === q.answer
  return {
    selected: isSelected,
    correct:  q._state === 'ok'    && isAnswer,
    wrong:    q._state === 'wrong' && isSelected && !isAnswer
  }
}

// ===== 组卷：确保四类都有（mcq / tf / match / pic），总数 = 5 =====

function pick1(arr) {
  return arr[Math.floor(Math.random() * arr.length)]
}

function uniqueClone(q) {
  const cloned = (typeof structuredClone === 'function')
    ? structuredClone(q)
    : JSON.parse(JSON.stringify(q))
  // 避免 v-for key 冲突
  cloned.key = `${q.key}#${Math.random().toString(36).slice(2,7)}`
  return cloned
}

function hydrate(q) {
  // 附加响应式字段
  if (isMatch(q)) {
    const obj = {}
    ;(q.left || []).forEach(l => { obj[l.key] = '' })
    q.choices = obj
  }
  q.choice = null
  q._state = 'idle'
  return q
}

function ensureBankReady() {
  const missing = []
  if (!bank.mcq   || !bank.mcq.length)   missing.push('MCQ')
  if (!bank.tf    || !bank.tf.length)    missing.push('True/False')
  if (!bank.match || !bank.match.length) missing.push('Click & Match')
  if (!bank.pic   || !bank.pic.length)   missing.push('Name the Pic')
  if (missing.length) {
    console.error('The question bank lacks question types：' + missing.join('、'))
    alert(`The question bank lacks question types：${missing.join('、')},Please fill in the blanks first before you start answering the questions.`)
    return false
  }
  return true
}

function buildPaper() {
  if (!ensureBankReady()) { quiz.value = []; return }

  const chosen = []
  const pickedKeys = new Set()

  // 四类各取 1 题（确保覆盖）
  const firstBatch = [ pick1(bank.mcq), pick1(bank.tf), pick1(bank.match), pick1(bank.pic) ]
  firstBatch.forEach(q => {
    const c = uniqueClone(q)
    pickedKeys.add(q.key)     // 去重依据原始 key
    chosen.push(hydrate(c))
  })

  // 补到 total：优先从未使用过的题里取
  const poolUnique = [...bank.mcq, ...bank.tf, ...bank.match, ...bank.pic]
    .filter(q => !pickedKeys.has(q.key))
  if (chosen.length < total && poolUnique.length) {
    chosen.push(hydrate(uniqueClone(pick1(poolUnique))))
  }

  // 若题库太少仍不足 total，则允许重复（但换 key）
  const poolAll = [...bank.mcq, ...bank.tf, ...bank.match, ...bank.pic]
  while (chosen.length < total && poolAll.length) {
    chosen.push(hydrate(uniqueClone(pick1(poolAll))))
  }

  // 洗牌
  for (let i = chosen.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    const tmp = chosen[i]; chosen[i] = chosen[j]; chosen[j] = tmp
  }

  quiz.value = chosen.slice(0, total)
}



function submitQuiz(){
  submitted.value = true
  // MATCH 按全部配对正确算 1 分
  score.value = quiz.value.reduce((a, q) => {
    if (isMatch(q)) {
      const ans = q.answer || {}, sel = q.choices || {}
      const ok = Object.keys(ans).every(k => ans[k] === sel[k])
      return a + (ok ? 1 : 0)
    }
    return a + ((q.choice === q.answer) ? 1 : 0)
  }, 0)
}
function resetQuiz(){
  submitted.value = false
  score.value = 0
  page.value = 1
  buildPaper()
}

onMounted(buildPaper)
</script>

<style scoped>
/* 容器 */
.card{
  background: transparent;
  color: var(--lm-text);
  border: 1px solid #1f2937;
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 10px 28px rgba(15,23,42,.08);
}
.card__title{ margin:0 0 10px; font-size:1.25rem; line-height:1.35; font-weight:800; color: var(--lm-heading); }

/* 进度条（已答/总数） */
.q__progress{
  width:100%; height:10px; margin-top:6px;
  background:#dbeafe; border:1px solid #93c5fd; border-radius:999px; overflow:hidden;
}
.q__progress-bar{ height:100%; width:0; background:#2563eb; transition: width .25s ease; }

/* 题干 */
.quiz{ margin-top: 12px; }
.quiz__q{ margin:0 0 8px; font-weight:800; color: var(--lm-heading); }
.quiz__no{ margin-right:6px; }

/* ===== MCQ（卡片网格） ===== */
.mcq__prompt{ width: 280px; max-width: 100%; border-radius: 12px; margin: 6px 0 10px; }
.mcq__opts{ display:grid; gap:10px; grid-template-columns: repeat(3, minmax(0,1fr)); }
@media (max-width: 720px){ .mcq__opts{ grid-template-columns: 1fr 1fr; } }
.mcq__card{
  display:flex; flex-direction:column; align-items:center; gap:8px;
  border:1px solid #94a3b8; border-radius:12px; padding:10px;
  background:transparent; cursor:pointer;
}
.mcq__card:disabled{ cursor:not-allowed; opacity:.7; }
.mcq__img{ width:100%; aspect-ratio: 4/3; object-fit: cover; border-radius:10px; }
.mcq__name{ font-weight:800; }
.selected{ outline:2px solid #60a5fa; }
.correct.selected{ outline-color:#16a34a; }
.wrong.selected{   outline-color:#e11d48; }

/* ===== TF ===== */
.quiz__opts{ display:grid; gap:8px; grid-template-columns:1fr; }
.quiz__opts--tf{ grid-template-columns:1fr 1fr; }
.btn{
  padding:10px 16px; border-radius:12px; border:1px solid #1f2937;
  background:#1f2937; color:#fff; font-weight:800; cursor:pointer;
  transition:transform .08s ease, box-shadow .08s ease, opacity .15s;
  box-shadow:0 6px 14px rgba(2,6,23,.15);
}
.btn--outline{ background:transparent; color:var(--lm-text); border:1px solid #94a3b8; }
.btn:hover{ transform:translateY(-1px); }
.btn:disabled{ opacity:.55; cursor:not-allowed; }

/* ===== Match（左图右下拉） ===== */
.match__row{ display:grid; grid-template-columns: 1fr 1.1fr; gap:10px; align-items:center; margin:10px 0; }
.match__left{ display:flex; align-items:center; gap:10px; }
.match__img{ width:80px; height:60px; object-fit:cover; border-radius:10px; border:1px solid #e5e7eb; }
.match__label{ font-weight:800; }
.match__select{ padding:10px 12px; border-radius:10px; border:1px solid #94a3b8; background:#fff; }

/* ===== Pic（题图 + 名字按钮） ===== */
.pic__img{ width: 280px; max-width: 100%; display:block; margin: 8px 0 10px; border-radius: 12px; }
.pic__opts{ display:grid; gap:8px; grid-template-columns: 1fr 1fr 1fr; }
@media (max-width: 720px){ .pic__opts{ grid-template-columns: 1fr 1fr; } }

/* 反馈 */
.quiz__fb{ margin:8px 0 0; font-weight:800; }
.quiz__fb--warn{ color:#b45309; }
.quiz__fb--ok{ color:#15803d; }

/* 页脚导航 */
.q__footer{ margin-top: 16px; position: relative; display:flex; align-items:center; justify-content:space-between; }
.arrow{ position:relative; border:none; cursor:pointer; font-weight:800; padding:12px 20px; color:#0b1220; background:#e8b6ae; }
.arrow:disabled{ opacity:.5; cursor:not-allowed; }
.arrow span{ position:relative; z-index:1; }
.arrow--left{ padding-left:46px; }
.arrow--left::before{ content:''; position:absolute; left:-28px; top:0; width:0; height:0; border-top:26px solid transparent; border-bottom:26px solid transparent; border-right:28px solid #e8b6ae; }
.arrow--right{ background:#0ea5b5; color:#fff; padding-right:46px; }
.arrow--right::after{ content:''; position:absolute; right:-28px; top:0; width:0; height:0; border-top:26px solid transparent; border-bottom:26px solid transparent; border-left:28px solid #0ea5b5; }

/* 圆点（未解锁禁用） */
.q__dots{ display:flex; gap:8px; align-items:center; justify-content:center; position:absolute; left:50%; transform:translateX(-50%); }
.dot{ width:10px; height:10px; border-radius:999px; background:#94a3b8; border:0; cursor:pointer; }
.dot.active{ background:#0ea5b5; }
.dot:disabled{ opacity:.5; cursor:not-allowed; }

/* 成绩与重置 */
.q__summary{ margin-top: 10px; display:flex; gap:12px; align-items:center; }
.quiz__score{ margin:0; font-weight:900; }

/* 固定浅色方案 */
@media (prefers-color-scheme: dark){
  .card{ background: transparent; color: var(--lm-text); border-color:#1f2937; }
}
</style>
