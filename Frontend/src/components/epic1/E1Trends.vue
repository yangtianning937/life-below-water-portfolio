<template>
  <section class="panel" :class="{ 'trends-fullscreen': full }">
    <div class="panel-title panel-title-row">
      <span>Trends</span>
      <button class="icon-btn" :title="full ? 'Restore' : 'Maximize'" @click="toggleFull" aria-label="Toggle fullscreen">
        <svg v-if="!full" width="16" height="16" viewBox="0 0 24 24"><path d="M4 9V4h5M15 4h5v5M20 15v5h-5M9 20H4v-5" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
        <svg v-else width="16" height="16" viewBox="0 0 24 24"><path d="M9 4H4v5M20 9V4h-5M4 15v5h5M15 20h5v-5" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
      </button>
    </div>

    <!-- 日期选择 -->
    <div class="btn-row">
      <label class="checkbox" style="gap:6px;">
        <span>From</span>
        <input type="date"
          :min="iso(range.min)" :max="iso(range.max)"
          :value="iso(range.from)"
          @change="updateFrom($event.target.value)" />
      </label>
      <label class="checkbox" style="gap:6px;">
        <span>To</span>
        <input type="date"
          :min="iso(range.min)" :max="iso(range.max)"
          :value="iso(range.to)"
          @change="updateTo($event.target.value)" />
      </label>
    </div>

    <!-- Tabs -->
    <div class="tab-row">
      <button class="tab" :class="{ active: tab==='hist' }"  @click="$emit('update:tab', 'hist')">WQI Histogram</button>
      <button class="tab" :class="{ active: tab==='klass' }" @click="$emit('update:tab', 'klass')">Class Distribution</button>
      <button class="tab" :class="{ active: tab==='time' }"  @click="$emit('update:tab', 'time')">Monthly Avg WQI</button>
    </div>

    <!-- 直方图 -->
    <div v-show="tab==='hist'">
      <div class="hint">Distribution of water_quality_score</div>
      <svg :width="hist.w" :height="hist.h" class="hist-svg">
        <!-- x 轴 -->
        <line :x1="hist.pad" :x2="hist.w - hist.pad" :y1="hist.h - hist.pad" :y2="hist.h - hist.pad" stroke="#94a3b8" stroke-width="1"/>
        <!-- bars -->
        <g v-for="(b,i) in histogram" :key="i">
          <rect :x="b.x" :y="b.y" :width="b.w" :height="b.h" fill="#60a5fa" opacity="0.9"/>
        </g>
      </svg>
    </div>

    <!-- Class 分布 -->
    <div v-show="tab==='klass'">
      <div class="hint">Distribution of classes</div>
      <svg :width="klassCfg.w" :height="klassCfg.h" class="klass-svg">
        <g v-for="(bar,i) in klassBars" :key="i">
          <rect :x="bar.x" :y="bar.y" :width="bar.w" :height="bar.h" :fill="bar.fill"/>
          <text :x="bar.x + bar.w + 6" :y="bar.y + bar.h/2 + 4" font-size="12" fill="#334155">{{ bar.label }} ({{ bar.n }})</text>
        </g>
      </svg>
    </div>

    <!-- 月均 WQI 折线 -->
    <div v-show="tab==='time'">
      <div class="hint">Monthly average WQI</div>
      <svg :width="tsCfg.w" :height="tsCfg.h" class="ts-svg">
        <polyline :points="tsPath" fill="none" stroke="#0ea5e9" stroke-width="2"/>
        <g v-for="(p,i) in tsPoints" :key="i">
          <circle :cx="p.x" :cy="p.y" r="2.5" fill="#0ea5e9"/>
        </g>
      </svg>
    </div>
  </section>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from "vue";

const props = defineProps({
  rows: { type: Array, required: true },     // 过滤后的记录
  cols: { type: Object, required: true },    // 列名映射，与父保持一致
  range: { type: Object, required: true },   // v-model:range {min,max,from,to}
  tab:   { type: String, required: true },   // v-model:tab  'hist'|'klass'|'time'
  full:  { type: Boolean, required: true },  // v-model:full
});
const emit = defineEmits(["update:range", "update:tab", "update:full"]);

function toDate(x){ const d = new Date(x); return isNaN(+d) ? null : d; }
function iso(d){ return d ? d.toISOString().slice(0,10) : ""; }

/** 画布尺寸（与原逻辑一致） */
const SMALL = { w: 260, h: 140 };
const LARGE = { w: 960, h: 480 };

const hist = ref({ w: SMALL.w, h: SMALL.h, pad: 24, bins: 10, barW: 0 });
const histogram = ref([]);

const klassCfg = ref({ w: SMALL.w, h: SMALL.h, pad: 24, barH: 16, gap: 6 });
const klassBars = ref([]);

const tsCfg = ref({ w: SMALL.w, h: SMALL.h, pad: 24 });
const tsPoints = ref([]);
const tsPath = ref("");

function setTrendsSize(full) {
  const S = full ? LARGE : SMALL;
  hist.value.w = klassCfg.value.w = tsCfg.value.w = S.w;
  hist.value.h = klassCfg.value.h = tsCfg.value.h = S.h;
  buildHistogram(); buildKlassBars(); buildTimeSeries();
}
watch(() => props.full, v => setTrendsSize(v));

/** 全屏开关 + ESC 退出（继承原逻辑） */
function toggleFull(){ emit("update:full", !props.full); }
function handleEsc(e){ if(e.key === "Escape") emit("update:full", false); }
watch(() => props.full, (v) => {
  if (v) {
    document.documentElement.style.overflow = "hidden";
    document.body.style.overflow = "hidden";
    document.addEventListener("keydown", handleEsc);
  } else {
    document.documentElement.style.overflow = "";
    document.body.style.overflow = "";
    document.removeEventListener("keydown", handleEsc);
  }
});

/** ===== 三个图的构建函数（从原文件迁移，按 props.rows/cols 取值） ===== */
function buildHistogram() {
  const wqis = props.rows.map(r => r[props.cols.wqi]).filter(v => typeof v === "number" && isFinite(v));
  if (!wqis.length) { histogram.value = []; return; }
  const min = Math.min(...wqis), max = Math.max(...wqis);
  const bins = Array.from({ length: hist.value.bins }, () => 0);
  const step = (max - min) / hist.value.bins || 1;
  for (const v of wqis) {
    let idx = Math.floor((v - min) / step);
    if (idx >= bins.length) idx = bins.length - 1;
    if (idx < 0) idx = 0;
    bins[idx]++;
  }
  const pad = hist.value.pad, W = hist.value.w - pad*2, H = hist.value.h - pad*2;
  const maxN = Math.max(...bins, 1);
  hist.value.barW = W / bins.length;
  histogram.value = bins.map((n, i) => {
    const barH = (n / maxN) * H;
    const x = pad + i * hist.value.barW;
    const y = hist.value.h - pad - barH;
    return { x, y, w: hist.value.barW - 2, h: barH };
  });
}

function buildKlassBars() {
  const counts = new Map();
  for (const r of props.rows) {
    const k = String(r[props.cols.klass] ?? "").trim();
    if (!k) continue;
    counts.set(k, (counts.get(k) || 0) + 1);
  }
  const items = Array.from(counts.entries()).sort((a,b)=>b[1]-a[1]);
  const pad = klassCfg.value.pad, barH = klassCfg.value.barH, gap = klassCfg.value.gap;
  const W = klassCfg.value.w - pad*2;
  const H = klassCfg.value.h - pad*2;
  const maxN = Math.max(...items.map(([,n])=>n), 1);
  let y = klassCfg.value.h - pad - barH;
  klassBars.value = items.map(([label, n]) => {
    const w = (n / maxN) * W;
    const row = { x: pad, y, w, h: barH, n, label, fill: "#60a5fa" };
    y -= (barH + gap);
    return row;
  }).filter(r => r.y >= pad);
}

function buildTimeSeries() {
  // 聚合到 YYYY-MM
  const byMonth = new Map();
  for (const r of props.rows) {
    const d = toDate(r[props.cols.date]); const v = r[props.cols.wqi];
    if (!d || typeof v !== "number" || !isFinite(v)) continue;
    const key = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}`;
    const cur = byMonth.get(key) || { sum:0, n:0, date:new Date(d.getFullYear(), d.getMonth(), 1) };
    cur.sum += v; cur.n += 1;
    byMonth.set(key, cur);
  }
  const rows = Array.from(byMonth.values()).sort((a,b)=>a.date-b.date).map(o => ({ date:o.date, value:o.sum/o.n }));
  if (!rows.length) { tsPoints.value = []; tsPath.value = ""; return; }

  const pad = tsCfg.value.pad, W = tsCfg.value.w - pad*2, H = tsCfg.value.h - pad*2;
  const xs = rows.map(r => +r.date), ys = rows.map(r => r.value);
  const minX = Math.min(...xs), maxX = Math.max(...xs);
  const minY = Math.min(...ys), maxY = Math.max(...ys);
  const xOf = (t) => pad + (W * (t - minX)) / Math.max(1, maxX-minX);
  const yOf = (v) => (tsCfg.value.h - pad) - (H * (v - minY)) / Math.max(1e-6, maxY-minY);

  tsPoints.value = rows.map(r => ({ x: xOf(+r.date), y: yOf(r.value) }));
  tsPath.value = tsPoints.value.map(p => `${p.x},${p.y}`).join(" ");
}

/** 响应变化重建图表 */
watch(() => props.rows, () => { buildHistogram(); buildKlassBars(); buildTimeSeries(); }, { deep: true });
watch(() => [tsCfg.value.w, tsCfg.value.h], buildTimeSeries);
watch(() => [hist.value.w, hist.value.h, hist.value.bins], buildHistogram);
watch(() => [klassCfg.value.w, klassCfg.value.h], buildKlassBars);

function updateFrom(val) {
  if (!val) return;
  const d = new Date(val);
  emit("update:range", { ...props.range, from: d });
}
function updateTo(val) {
  if (!val) return;
  const d = new Date(val);
  emit("update:range", { ...props.range, to: d });
}

onMounted(() => setTrendsSize(false)); // 初始小窗
onUnmounted(() => {
  document.documentElement.style.overflow = "";
  document.body.style.overflow = "";
  document.removeEventListener("keydown", handleEsc);
});
</script>
