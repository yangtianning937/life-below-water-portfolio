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

      <!-- ===== MCQ ===== -->
      <div v-if="isMCQ(cur)" class="mcq">
        <img v-if="cur.promptImg" class="mcq__prompt" :src="cur.promptImg" alt="" />
        <div class="mcq__opts">
          <button v-for="opt in cur.options" :key="opt.key"
                  class="mcq__card"
                  :class="btnStateClass(cur, opt.key)"
                  @click="choose(cur, opt.key)"
                  :disabled="cur.locked || cur._state!=='idle' || submitted"
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
                :disabled="cur.locked || cur._state!=='idle' || submitted">True</button>
        <button class="btn btn--outline"
                :class="btnStateClass(cur, 'f')"
                @click="choose(cur, 'f')"
                :disabled="cur.locked || cur._state!=='idle' || submitted">False</button>
      </div>

      <!-- ===== Match（左图右下拉） ===== -->
      <div v-else-if="isMatch(cur)" class="match">
        <div class="match__row" v-for="left in cur.left" :key="left.key">
          <div class="match__left">
            <img class="match__img" :src="left.img" :alt="left.label" />
            <div class="match__label">{{ left.label }}</div>
          </div>
          <select class="match__select"
                  v-model="cur.choices[left.key]"
                  @change="onMatchChange(cur)"
                  :disabled="cur._state!=='idle' || submitted">
            <option disabled value="">Please select the corresponding feature.</option>
            <option v-for="r in cur.right" :key="r.key" :value="r.key">{{ r.label }}</option>
          </select>
        </div>
      </div>

      <!-- ===== Pic（题图 + 名字按钮） ===== -->
      <div v-else-if="isPIC(cur)" class="pic">
        <img class="pic__img" :src="cur.image" alt="" />
        <div class="pic__opts">
          <button v-for="opt in cur.options" :key="opt.key"
                  class="btn btn--outline"
                  :class="btnStateClass(cur, opt.key)"
                  @click="choose(cur, opt.key)"
                  :disabled="cur.locked || cur._state!=='idle' || submitted">
            {{ opt.name }}
          </button>
        </div>
      </div>

      <!-- 反馈 -->
      <p v-if="cur._state==='ok'"    class="quiz__fb quiz__fb--ok">{{ cur.correct   || 'Nice! That’s correct.' }}</p>
      <p v-if="cur._state==='wrong'" class="quiz__fb quiz__fb--warn">{{ cur.incorrect || 'Try again!' }}</p>
    </div>

    <!-- 底部导航（已移除 Check；基于是否“已判题”启用下一步） -->
    <div class="q__footer">
      <button class="arrow arrow--left" :disabled="page===1" @click="prevPage"><span>Previous</span></button>

      <div class="q__dots" role="tablist" aria-label="Quiz pages">
        <button v-for="n in total" :key="n"
                class="dot" :class="{active: page===n}"
                :disabled="n > unlockedPage"
                @click="go(n)"></button>
      </div>

      <button v-if="page<total"
              class="arrow arrow--right"
              :disabled="!cur || cur._state==='idle'"
              @click="nextPage"><span>Next</span></button>

      <button v-else
              class="arrow arrow--right"
              :disabled="!allChecked"
              @click="submitQuiz"><span>Submit</span></button>
    </div>

    <!-- 成绩与重置 -->
    <div v-if="submitted" class="q__summary">
      <p class="quiz__score">Score: {{ score }}/{{ total }}</p>
      <button class="btn btn--ghost" @click="resetQuiz">Reset</button>
    </div>

    <!-- 题库不完整提示 -->
    <FullscreenMessage
      v-model="bankErrorOpen"
      title="Incomplete Question Bank"
      :message="bankErrorText"
      icon="⚠️"
      confirmText="OK"
      :persistent="false"
    />

    <!-- 提交成绩后的祝贺提示（score-based） -->
    <FullscreenMessage
      v-model="submitOpen"
      :title="submitTitle"
      :message="submitText"
      icon="🎉"
      confirmText="OK"
      :persistent="false"
      @confirm="goHome"
    />
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import bank from '@/data/marineQuiz'
import FullscreenMessage from '@/components/FullscreenMessage.vue'
import { useRouter } from 'vue-router'

/** 弹窗状态 */
const bankErrorOpen = ref(false)
const bankErrorText = ref('')
const submitOpen = ref(false)
const submitText = ref('')
const submitTitle = ref('Congratulations')

const router = useRouter()

function goHome() {
  submitOpen.value = false
  router.push('/home')
}

/** 组卷：5题；四类至少各1，+1个随机补位 */
const total = 5
const quiz = ref([]) // 附加：choice / _state / locked；match 另有 choices:{}
const page = ref(1)
const submitted = ref(false)
const score = ref(0)

const cur = computed(() => quiz.value[page.value - 1] || null)

/** 进度：按“已判题”计算 */
const checkedCount = computed(() => quiz.value.filter(q => q._state !== 'idle').length)
const progressPct  = computed(() => Math.round((checkedCount.value / total) * 100))
const allChecked   = computed(() => quiz.value.length === total && quiz.value.every(q => q._state !== 'idle'))

/** 未解锁之前的最大页：允许进入“已判题”的下一题 */
const unlockedPage = computed(() => {
  const i = quiz.value.findIndex(q => q._state === 'idle')
  return i === -1 ? total : i + 1
})

/** 题型判断 */
const isMCQ  = q => (q?.type || '').toLowerCase() === 'mcq'
const isTF   = q => (q?.type || '').toLowerCase() === 'tf'
const isMatch= q => (q?.type || '').toLowerCase() === 'match'
const isPIC  = q => (q?.type || '').toLowerCase() === 'pic'

/** 是否“作答” */
function isAnswered(q){
  if (!q) return false
  if (isMatch(q)) {
    const leftKeys = (q.left || []).map(l => l.key)
    return leftKeys.length && leftKeys.every(k => q.choices && q.choices[k])
  }
  return q.choice !== null && q.choice !== undefined && q.choice !== ''
}

/** 判题工具 */
function judge(q){
  if (!q || q._state !== 'idle') return
  if (isMatch(q)) {
    if (!isAnswered(q)) return
    const ans = q.answer || {}
    const sel = q.choices || {}
    const ok = Object.keys(ans).every(k => ans[k] === sel[k])
    q._state = ok ? 'ok' : 'wrong'
  } else {
    if (!q.choice) return
    q._state = (q.choice === q.answer) ? 'ok' : 'wrong'
  }
}

/** 选择（mcq / tf / pic）：单题只允许一次选择 & 立即判题 */
function choose(q, key){
  if (!q || q._state !== 'idle' || q.locked) return
  q.choice = key
  q.locked = true
  judge(q)
}

/** Match：当所有下拉都选完时自动判题 */
function onMatchChange(q){
  if (!q || q._state !== 'idle') return
  if (isAnswered(q)) judge(q)
}

/** 键盘：右键=已判题则下一题，否则尝试判题（仅对 match 有意义） */
function tryNextByKey(){
  if (!cur.value) return
  if (cur.value._state === 'idle') {
    if (isMatch(cur.value)) judge(cur.value)
  } else {
    nextPage()
  }
}

/** 翻页与导航 */
function nextPage(){ if (page.value < unlockedPage.value) page.value++ }
function prevPage(){ if (page.value > 1) page.value-- }
function go(n){ if (n <= unlockedPage.value) page.value = n }

/** 选项状态 class */
function btnStateClass(q, key){
  const isSelected = q.choice === key
  const isAnswer   = key === q.answer
  return {
    selected: isSelected,
    correct:  q._state === 'ok'    && isAnswer,
    wrong:    q._state === 'wrong' && isSelected && !isAnswer
  }
}

/** 组卷：确保四类都有（mcq / tf / match / pic），总数 = 5 */
function pick1(arr) { return arr[Math.floor(Math.random() * arr.length)] }
function uniqueClone(q) {
  const cloned = (typeof structuredClone === 'function')
    ? structuredClone(q)
    : JSON.parse(JSON.stringify(q))
  cloned.key = `${q.key}#${Math.random().toString(36).slice(2,7)}`
  return cloned
}
function hydrate(q) {
  if (isMatch(q)) {
    const obj = {}
    ;(q.left || []).forEach(l => { obj[l.key] = '' })
    q.choices = obj
  }
  q.choice = null
  q._state = 'idle'
  q.locked = false
  return q
}

function ensureBankReady() {
  const missing = []
  if (!bank.mcq   || !bank.mcq.length)   missing.push('MCQ')
  if (!bank.tf    || !bank.tf.length)    missing.push('True/False')
  if (!bank.match || !bank.match.length) missing.push('Click & Match')
  if (!bank.pic   || !bank.pic.length)   missing.push('Name the Pic')
  if (missing.length) {
    console.error('The question bank lacks question types: ' + missing.join(', '))
    bankErrorText.value =
      `The question bank lacks question types: ${missing.join(', ')}. ` +
      `Please complete the blanks before starting the quiz.`
    bankErrorOpen.value = true
    return false
  }
  return true
}

function buildPaper() {
  if (!ensureBankReady()) { quiz.value = []; return }

  const chosen = []
  const pickedKeys = new Set()

  const firstBatch = [ pick1(bank.mcq), pick1(bank.tf), pick1(bank.match), pick1(bank.pic) ]
  firstBatch.forEach(q => {
    const c = uniqueClone(q)
    pickedKeys.add(q.key)
    chosen.push(hydrate(c))
  })

  const poolUnique = [...bank.mcq, ...bank.tf, ...bank.match, ...bank.pic]
    .filter(q => !pickedKeys.has(q.key))
  if (chosen.length < total && poolUnique.length) {
    chosen.push(hydrate(uniqueClone(pick1(poolUnique))))
  }

  const poolAll = [...bank.mcq, ...bank.tf, ...bank.match, ...bank.pic]
  while (chosen.length < total && poolAll.length) {
    chosen.push(hydrate(uniqueClone(pick1(poolAll))))
  }

  for (let i = chosen.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    const tmp = chosen[i]; chosen[i] = chosen[j]; chosen[j] = tmp
  }

  quiz.value = chosen.slice(0, total)
}

/** 分数对应消息（8–12 岁友好） */
function messageForScore(s, t) {
  if (s === t) return "Perfect score! You’recommend an Ocean Expert! 🐳"
  if (s === t - 1) return "Great work! Almost perfect—try again for 5/5! 💪"
  if (s >= Math.ceil(t * 0.6)) return "Nice try! Review a bit and play again! 📚"
  return "Don’t give up! Every try helps you learn! 🌈"
}

/** 分数对应标题（8–12 岁友好） */
function titleForScore(s, t) {
  if (s === t)       return "Ocean Expert!"
  if (s === t - 1)   return "So Close!"
  if (s >= Math.ceil(t * 0.6)) return "Great Effort!"
  return "Keep Going!"
}

function submitQuiz(){
  submitted.value = true
  score.value = quiz.value.reduce((a, q) => {
    if (isMatch(q)) {
      const ans = q.answer || {}, sel = q.choices || {}
      const ok = Object.keys(ans).every(k => ans[k] === sel[k])
      return a + (ok ? 1 : 0)
    }
    return a + ((q.choice === q.answer) ? 1 : 0)
  }, 0)

  submitText.value = messageForScore(score.value, total)
  submitTitle.value = titleForScore(score.value, total)
  submitOpen.value = true
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

/* 进度条（已判题/总数） */
.q__progress{
  width:100%; height:10px; margin-top:6px;
  background:#dbeafe; border:1px solid #93c5fd; border-radius:999px; overflow:hidden;
}
.q__progress-bar{ height:100%; width:0; background:#2563eb; transition: width .25s ease; }

/* 题干 */
.quiz{ margin-top: 12px; }
.quiz__q{ margin:0 0 8px; font-weight:800; color: var(--lm-heading); }
.quiz__no{ margin-right:6px; }

/* ===== MCQ ===== */
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

/* ===== TF/PIC ===== */
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

/* ===== Match ===== */
.match__row{ display:grid; grid-template-columns: 1fr 1.1fr; gap:10px; align-items:center; margin:10px 0; }
.match__left{ display:flex; align-items:center; gap:10px; }
.match__img{ width:80px; height:60px; object-fit:cover; border-radius:10px; border:1px solid #e5e7eb; }
.match__label{ font-weight:800; }
.match__select{ padding:10px 12px; border-radius:10px; border:1px solid #94a3b8; background:#fff; }

/* ===== Pic ===== */
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
