<template>
  <div class="panel" :class="{ 'trends-fullscreen': full }">
    <div class="panel-title-row">
      <div class="panel-title">Trends</div>

      <!-- 右上角图标按钮：切换全屏 -->
      <button class="icon-btn" @click="toggleFull" :title="full ? 'Exit fullscreen' : 'Fullscreen'">
        <svg v-if="!full" width="18" height="18" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M9 3H3v6M21 9V3h-6M3 15v6h6M15 21h6v-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <svg v-else width="18" height="18" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M9 5H5v4M19 9V5h-4M5 15v4h4M15 19h4v-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
    </div>

    <!-- 日期选择 -->
    <div class="date-row">
      <span>From</span>
      <input type="date" v-model="fromStr" @change="onDateChange" />
      <span>To</span>
      <input type="date" v-model="toStr" @change="onDateChange" />
    </div>

    <!-- Tabs -->
    <div class="tab-row">
      <button class="tab" :class="{ active: tab === 'hist' }"    @click="emit('update:tab','hist')">WQI Histogram</button>
      <button class="tab" :class="{ active: tab === 'klass' }"   @click="emit('update:tab','klass')">Class Distribution</button>
      <button class="tab" :class="{ active: tab === 'monthly' }" @click="emit('update:tab','monthly')">Monthly Avg WQI</button>
    </div>

    <!-- 图表说明 -->
    <div class="chart-desc">
      <template v-if="tab === 'hist'">
        <p><b>What this shows:</b> The distribution of the water quality score (WQI) for the selected time range and classes.</p>
        <p><b>How to read:</b> Lower WQI means cleaner water. The score ranges from <b>0 to 3</b> —
          <b>0 = very good & clean</b>, <b>3 = not good</b>. Use the filters above to narrow down by class and date.</p>
      </template>

      <template v-else-if="tab === 'klass'">
        <p><b>What this shows:</b> Number of records in each water quality class.</p>
        <ul class="legend">
          <li><span class="dot dot--green"></span><b>green</b> — healthy water</li>
          <li><span class="dot dot--yellow"></span><b>yellow</b> — be cautious</li>
          <li><span class="dot dot--orange"></span><b>orange</b> — not ideal</li>
          <li><span class="dot dot--darkred"></span><b>dark red</b> — not so good</li>
        </ul>
        <p class="note">After we work out the water quality index, we split it into the four levels above so it’s easy to see how clean the water is.</p>
        <p class="note"><b>Water quality score/index:</b> We check six indicators in the water, then give a score from <b>0–3</b>. <b>0</b> means very good and clean, <b>3</b> means not good.</p>
      </template>

      <template v-else>
        <p><b>What this shows:</b> Monthly average WQI over time.</p>
        <p><b>How to read:</b> Look for overall trend and sudden spikes/drops (they may indicate short-term events or missing data). Closer to <b>0</b> is better (cleaner water).</p>
      </template>
    </div>

    <!-- 图表区域 -->
    <template v-if="tab === 'hist'">
      <div v-if="histBars.length === 0" class="empty">No data for current filters.</div>
      <svg v-else class="hist-svg" :viewBox="`0 0 ${W} ${H}`" preserveAspectRatio="xMidYMid meet">

        <text :x="marginLeft + 2" :y="marginTop - 16" class="axis-title">Frequency (count)</text>

        <g :transform="`translate(${marginLeft},${marginTop})`">
          <!-- Y 轴 -->
          <line :x1="0" :x2="0" :y1="0" :y2="Hc" class="axis"/>
          <template v-for="t in yTicks" :key="'yh-'+t">
            <line :x1="-6" :x2="0" :y1="yScale(t)" :y2="yScale(t)" class="tick"/>
            <text :x="-8" :y="yScale(t)+4" class="tick-label" text-anchor="end">{{ t }}</text>
          </template>

          <!-- bars -->
          <template v-for="(b, i) in histBars" :key="i">
            <rect :x="b.x" :y="b.y" :width="b.w" :height="b.h" class="bar"/>
          </template>

          <!-- X 轴 -->
          <line :x1="0" :x2="Wc" :y1="Hc" :y2="Hc" class="axis" />
          <template v-for="tick in xTicks" :key="`xt-${tick}`">
            <line :x1="xScale(tick)" :x2="xScale(tick)" :y1="Hc" :y2="Hc+6" class="tick"/>
            <text :x="xScale(tick)" :y="Hc+18" class="tick-label" text-anchor="middle">{{ tick.toFixed(1) }}</text>
          </template>
        </g>

        <text :x="marginLeft + Wc/2" :y="H - 8" text-anchor="middle" class="axis-title">Water Quality Index (WQI)</text>
      </svg>
    </template>

    <template v-else-if="tab === 'klass'">
      <div v-if="klassBars.length === 0" class="empty">No data for current filters.</div>
      <svg v-else class="klass-svg" :viewBox="`0 0 ${W} ${H}`" preserveAspectRatio="xMidYMid meet">
        <text :x="marginLeft + 2" :y="marginTop - 16" class="axis-title">Water Quality Class</text>

        <g :transform="`translate(${marginLeft},${marginTop})`">
          <!-- 左侧 Y 轴 -->
          <line :x1="0" :x2="0" :y1="0" :y2="Hc" class="axis"/>

          <!-- bars -->
          <template v-for="(row, i) in klassBars" :key="i">
            <rect :x="0" :y="row.y" :width="row.w" :height="barH" :fill="row.fill" opacity="0.85"/>
            <!-- 左侧类别名（不溢出） -->
            <text :x="-8" :y="row.y + barH/2 + 4" class="tick-label" text-anchor="end">{{ row.left }}</text>
            <!-- 右侧/内部标签：智能放置，避免溢出 -->
            <text
              :x="row.labelX"
              :y="row.y + barH/2 + 4"
              :class="['label', { 'label-in': row.inside }]"
              :text-anchor="row.inside ? 'end' : 'start'"
            >
              {{ row.right }}
            </text>
          </template>

          <!-- x-axis -->
          <line :x1="0" :x2="Wc" :y1="Hc" :y2="Hc" class="axis" />
          <text :x="Wc/2" :y="Hc + 20" class="axis-title" text-anchor="middle">Number of Records</text>
        </g>
      </svg>
    </template>

    <template v-else>
      <div v-if="linePtsSafe.length === 0" class="empty">No data for current filters.</div>
      <svg v-else class="ts-svg" :viewBox="`0 0 ${W} ${H}`" preserveAspectRatio="xMidYMid meet">
        <text :x="marginLeft + Wc/2" :y="marginTop - 16" class="axis-title" text-anchor="middle">Monthly average WQI</text>

        <g :transform="`translate(${marginLeft},${marginTop})`">
          <!-- Y 轴（0~3） -->
          <line :x1="0" :x2="0" :y1="0" :y2="Hc" class="axis"/>
          <template v-for="t in vTicks" :key="'vt-'+t">
            <line :x1="-6" :x2="0" :y1="tyScale(t)" :y2="tyScale(t)" class="tick"/>
            <text :x="-8" :y="tyScale(t)+4" class="tick-label" text-anchor="end">{{ t }}</text>
          </template>

          <!-- 线与点 -->
          <polyline :points="polyPoints" fill="none" stroke-width="2" class="line"/>
          <template v-for="(p, i) in linePtsSafe" :key="i">
            <circle :cx="txScale(p.t)" :cy="tyScale(p.v)" r="2.5" class="dot-line"/>
          </template>

          <!-- X 轴（自适应稀疏年份刻度） -->
          <line :x1="0" :x2="Wc" :y1="Hc" :y2="Hc" class="axis" />
          <template v-for="(t,i) in tTicksAdaptive" :key="`t-${i}`">
            <line :x1="txScale(t.t)" :x2="txScale(t.t)" :y1="Hc" :y2="Hc+6" class="tick"/>
            <text :x="txScale(t.t)" :y="Hc+18" class="tick-label" text-anchor="middle">{{ t.label }}</text>
          </template>
        </g>

        <text :x="marginLeft + Wc/2" :y="H - 8" text-anchor="middle" class="axis-title">Time (Monthly)</text>
        <text :x="marginLeft + 8" :y="marginTop + 16" class="small">Average WQI</text>
      </svg>
    </template>
  </div>
</template>

<script setup>
import { computed, ref, watch, onBeforeUnmount } from 'vue'

const props = defineProps({
  rows:  { type: Array,  default: () => [] },
  cols:  { type: Object, required: true },     // { wqi, klass, date }
  range: { type: Object, required: true },     // { from, to, min, max }
  tab:   { type: String, default: 'hist' },
  full:  { type: Boolean, default: false },
  colorForClass: { type: Function, default: null },
})
const emit = defineEmits(['update:range', 'update:tab', 'update:full'])

/* ---------- 切换全屏（用按钮触发），并锁定滚动 ---------- */
const toggleFull = () => emit('update:full', !props.full)
const lockScroll = (on) => { document.body.style.overflow = on ? 'hidden' : '' }
watch(() => props.full, v => lockScroll(v), { immediate: true })
onBeforeUnmount(() => lockScroll(false))

/* ---------- 日期双向绑定（支持换行） ---------- */
const toISO = d => d instanceof Date && !isNaN(+d) ? d.toISOString().slice(0,10) : ''
const fromStr = ref(toISO(props.range?.from))
const toStr   = ref(toISO(props.range?.to))
watch(() => props.range, (r)=>{ fromStr.value = toISO(r?.from); toStr.value = toISO(r?.to) }, { deep:true })
function onDateChange(){
  emit('update:range', {
    ...props.range,
    from: fromStr.value ? new Date(fromStr.value) : null,
    to:   toStr.value   ? new Date(toStr.value)   : null,
  })
}

/* ---------- 画布尺寸与工具 ---------- */
const W=960, H=420
const marginLeft=110, marginRight=120, marginTop=52, marginBottom=40
const Wc = W - marginLeft - marginRight
const Hc = H - marginTop - marginBottom

const finite = v => Number.isFinite(v)
const clamp  = (v,a,b)=>Math.max(a,Math.min(b,v))

/* ================= Histogram ================= */
const xMin=0, xMax=3, bins=12
const xScale = x => ((x - xMin) / (xMax - xMin)) * Wc
const wqiVals = computed(() => props.rows.map(r => +r[props.cols.wqi]).filter(finite))
const histBinsRaw = computed(() => {
  if (!wqiVals.value.length) return []
  const step=(xMax-xMin)/bins, edges=Array.from({length:bins+1},(_,i)=>xMin+i*step)
  const counts=Array(bins).fill(0)
  for(const v of wqiVals.value){
    const idx = v>=xMax ? bins-1 : Math.floor((v-xMin)/step)
    if(idx>=0&&idx<bins) counts[idx]++
  }
  return counts.map((c,i)=>({x0:edges[i], x1:edges[i+1], count:c}))
})
const yMax = computed(()=>Math.max(1, ...histBinsRaw.value.map(b=>b.count).filter(finite)))
const yScale = y => Hc - (clamp(y,0,yMax.value) / yMax.value) * Hc
const histBars = computed(()=> histBinsRaw.value.map(b=>{
  const x0p=xScale(b.x0), x1p=xScale(b.x1), y=yScale(b.count)
  return { x:x0p, y, w:Math.max(0,x1p-x0p-1), h:Math.max(0,Hc-y) }
}).filter(b=>finite(b.x)&&finite(b.y)&&finite(b.w)&&finite(b.h)&&b.w>0))
const xTicks = Array.from({length:7},(_,i)=> xMin + i*(xMax-xMin)/6)
const yTicks = computed(()=>{
  const steps = 5
  const m = yMax.value
  if (!finite(m) || m<=1) return [0,1]
  const out=[]; for(let i=0;i<=steps;i++) out.push(Math.round((m/steps)*i))
  return out
})

/* ================= Class Distribution ================= */
const order=['yellow','green','orange','darkred']
const classRows = computed(()=>{
  const m=new Map()
  for(const r of props.rows){ const k=String(r?.[props.cols.klass]??'').trim(); m.set(k,(m.get(k)||0)+1) }
  const arr = Array.from(m.entries()).map(([name,count])=>({name,count}))
  return [...order.filter(o=>arr.some(a=>a.name===o)).map(o=>arr.find(a=>a.name===o)), ...arr.filter(a=>!order.includes(a.name))].filter(Boolean)
})
const kMax = computed(()=>Math.max(1,...classRows.value.map(d=>d.count).filter(finite)))
const kxScale = x => (clamp(x,0,kMax.value) / kMax.value) * Wc
const barBand=36, barH=18
const classColor = name => props.colorForClass ? props.colorForClass(name) : ({darkred:'#b91c1c',orange:'#f97316',green:'#22c55e',yellow:'#facc15'}[String(name||'').toLowerCase()] || '#6b7280')
const klassBars = computed(()=> classRows.value.map((row,i)=>{
  const w = Math.max(0,kxScale(row.count))
  const inside = w > Wc * 0.72 || (w > Wc - 88)
  const labelX = inside ? (w - 8) : Math.min(w + 8, Wc - 2)
  return {
    y: i*barBand,
    w,
    left: row.name || '(unknown)',
    right:`${row.name || '(unknown)'} (${row.count})`,
    fill: classColor(row.name),
    inside,
    labelX,
  }
}).filter(b=>finite(b.w)))

/* ================= Monthly Avg ================= */
const ym = d => `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}`
const monthly = computed(()=>{
  const g=new Map()
  for(const r of props.rows){
    const d=new Date(r?.[props.cols.date]); const v=+r?.[props.cols.wqi]
    if(!isNaN(+d)&&finite(v)){ const key=ym(d); const arr=g.get(key)||[]; arr.push(v); g.set(key,arr) }
  }
  return Array.from(g.entries()).map(([k,arr])=>({t:new Date(k+'-01'), v:arr.reduce((a,b)=>a+b,0)/arr.length}))
    .filter(p=>!isNaN(+p.t)&&finite(p.v)).sort((a,b)=>a.t-b.t)
})
const linePtsSafe = computed(()=> monthly.value)
const tMin = computed(()=> linePtsSafe.value.length ? linePtsSafe.value[0].t : new Date('2000-01-01'))
const tMax = computed(()=> linePtsSafe.value.length ? linePtsSafe.value.at(-1).t : new Date('2000-12-01'))
const txScale = t => { const a=tMin.value.getTime(), b=tMax.value.getTime(); const x=(t.getTime()-a)/Math.max(1,b-a); return clamp(x,0,1)*Wc }
const vMin=0, vMax=3
const tyScale = v => Hc - ((clamp(v,vMin,vMax)-vMin)/(vMax-vMin))*Hc
const vTicks = [0,0.5,1,1.5,2,2.5,3]

// 自适应年份刻度：保证相邻 label ≥ 60px
const tTicksAdaptive = computed(()=>{
  if(!linePtsSafe.value.length) return []
  const fy=linePtsSafe.value[0].t.getFullYear()
  const ly=linePtsSafe.value.at(-1).t.getFullYear()
  const years= ly - fy + 1
  const pxPerYear = Wc / Math.max(1, years-1)
  const step = Math.max(1, Math.ceil(60 / pxPerYear))
  const out=[]
  for(let y=fy; y<=ly; y+=step) out.push({ t:new Date(`${y}-01-01`), label:String(y) })
  return out
})
const polyPoints = computed(()=> linePtsSafe.value.map(p=>`${txScale(p.t)},${tyScale(p.v)}`).join(' '))
</script>

<style scoped>
/* 日期行：可换行，输入宽度受控 */
.date-row{
  display:flex; align-items:center; gap:8px; margin-bottom:10px;
  flex-wrap: wrap; font-size:12px; color:#334155;
}
.date-row input[type="date"]{
  border:1px solid #e5e7eb; border-radius:8px; padding:4px 8px; font-size:12px;
  width: 150px; max-width: 46%;
}

.axis{ stroke:#cbd5e1; stroke-width:1 }
.tick{ stroke:#94a3b8; stroke-width:1 }
.tick-label{ fill:#64748b; font-size:11px }
.axis-title{ fill:#64748b; font-size:12px; }
.small{ fill:#64748b; font-size:11px; }

.bar{ fill:#60a5fa; }
.line{ stroke:#1d9bf0; }
.dot-line{ fill:#1d9bf0; }
.label{ fill:#334155; font-size:12px }
.label-in{ fill:#ffffff; font-weight:600; }

.chart-desc{
  font-size:12px; color:#475569; background:#f8fafc;
  border:1px solid #e5e7eb; border-radius:8px;
  padding:10px 12px; margin:10px 0 12px;
}
.chart-desc b{ color:#334155 }
.chart-desc .legend{ list-style:none; margin:6px 0; padding:0; display:grid; gap:4px; }
.chart-desc .dot{ display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; vertical-align:-1px; }
.chart-desc .dot--green{  background:#22c55e; }
.chart-desc .dot--yellow{ background:#facc15; }
.chart-desc .dot--orange{ background:#f97316; }
.chart-desc .dot--darkred{ background:#b91c1c; }
.chart-desc .note{ margin:6px 0 0 0; }

.empty{
  border:1px dashed #e5e7eb; background:#fafafa; color:#64748b;
  padding:12px; border-radius:8px; margin-top:8px; font-size:12px;
}

.tab-row{ display:flex; gap:8px; margin-bottom:6px; flex-wrap:wrap; }
.tab{ padding:4px 8px; border:1px solid #e5e7eb; background:#fff; border-radius:8px; cursor:pointer; font-size:12px; }
.tab.active, .tab:hover{ background:#f3f4f6; }

/* 全屏按钮样式 */
.icon-btn{
  border:1px solid #e5e7eb; background:#fff; border-radius:8px;
  padding:6px; cursor:pointer; line-height:0; color:#334155;
}
.icon-btn:hover{ background:#f3f4f6; }

/* 全屏容器 */
.trends-fullscreen{
  position: fixed; inset: 12px; z-index: 1000;
  background: #fff; overflow: auto;
  display: grid; grid-template-columns: 1fr; gap: 10px;
  border-radius: 12px; padding: 16px; box-shadow: 0 10px 40px rgba(0,0,0,.15);
}
</style>
