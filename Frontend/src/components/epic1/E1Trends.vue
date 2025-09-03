<template>
  <section class="panel" :class="{ 'trends-fullscreen': full }">
    <!-- 标题 + 全屏按钮 -->
    <div class="panel-title panel-title-row">
      <span>Trends</span>
      <button class="icon-btn" :title="full ? 'Restore' : 'Maximize'" @click="toggleFull" aria-label="Toggle fullscreen">
        <svg v-if="!full" width="16" height="16" viewBox="0 0 24 24">
          <path d="M4 9V4h5M15 4h5v5M20 15v5h-5M9 20H4v-5" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/>
        </svg>
        <svg v-else width="16" height="16" viewBox="0 0 24 24">
          <path d="M9 4H4v5M20 9V4h-5M4 15v5h5M15 20h5v-5" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/>
        </svg>
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
    <div v-show="tab==='hist'" :class="['svg-wrap', { centered: full }]">
      <div class="hint">Distribution of water_quality_score</div>
      <svg :width="hist.w" :height="hist.h" class="hist-svg">
        <!-- 轴线 -->
        <line :x1="hist.pad" :x2="hist.w - hist.pad" :y1="hist.h - hist.pad" :y2="hist.h - hist.pad" stroke="#94a3b8" stroke-width="1"/>
        <line :x1="hist.pad" :x2="hist.pad" :y1="hist.pad" :y2="hist.h - hist.pad" stroke="#94a3b8" stroke-width="1"/>

        <!-- 顶部的 Y 轴标题（不旋转、放在轴顶端） -->
        <text :x="hist.pad" :y="hist.pad - 10" text-anchor="start" font-size="12" fill="#334155">
          Frequency (count)
        </text>

        <!-- x 轴刻度 -->
        <g v-if="histTicks.x.length">
          <g v-for="(t,i) in histTicks.x" :key="'hx'+i">
            <line :x1="t.x" :x2="t.x" :y1="hist.h - hist.pad" :y2="hist.h - hist.pad + 4" stroke="#94a3b8" stroke-width="1"/>
            <text :x="t.x" :y="hist.h - hist.pad + 14" text-anchor="middle" font-size="11" fill="#64748b">{{ t.label }}</text>
          </g>
        </g>
        <!-- y 轴刻度 -->
        <g v-if="histTicks.y.length">
          <g v-for="(t,i) in histTicks.y" :key="'hy'+i">
            <line :x1="hist.pad - 4" :x2="hist.pad" :y1="t.y" :y2="t.y" stroke="#94a3b8" stroke-width="1"/>
            <text :x="hist.pad - 6" :y="t.y + 4" text-anchor="end" font-size="11" fill="#64748b">{{ t.label }}</text>
          </g>
        </g>

        <!-- 柱子 -->
        <g v-for="(b,i) in histogram" :key="i">
          <rect :x="b.x" :y="b.y" :width="b.w" :height="b.h" fill="#60a5fa" opacity="0.9"/>
        </g>

        <!-- X 轴标题 -->
        <text :x="hist.w/2" :y="hist.h - 2" text-anchor="middle" font-size="12" fill="#334155">
          Water Quality Index (WQI)
        </text>
      </svg>
    </div>

    <!-- Class 分布 -->
    <div v-show="tab==='klass'" :class="['svg-wrap', { centered: full }]">
      <div class="hint">Distribution of classes</div>
      <svg :width="klassCfg.w" :height="klassCfg.h" class="klass-svg">
        <!-- 轴线 -->
        <line :x1="klassCfg.pad" :x2="klassCfg.w - klassCfg.pad" :y1="klassCfg.h - klassCfg.pad" :y2="klassCfg.h - klassCfg.pad" stroke="#94a3b8" stroke-width="1"/>
        <line :x1="klassCfg.pad" :x2="klassCfg.pad" :y1="klassCfg.pad" :y2="klassCfg.h - klassCfg.pad" stroke="#94a3b8" stroke-width="1"/>

        <!-- 顶部的 Y 轴标题 -->
        <text :x="klassCfg.pad" :y="klassCfg.pad - 10" text-anchor="start" font-size="12" fill="#334155">
          Water Quality Class
        </text>

        <!-- x 轴刻度 -->
        <g v-if="klassTicks.x.length">
          <g v-for="(t,i) in klassTicks.x" :key="'kx'+i">
            <line :x1="t.x" :x2="t.x" :y1="klassCfg.h - klassCfg.pad" :y2="klassCfg.h - klassCfg.pad + 4" stroke="#94a3b8" stroke-width="1"/>
            <text :x="t.x" :y="klassCfg.h - klassCfg.pad + 14" text-anchor="middle" font-size="11" fill="#64748b">{{ t.label }}</text>
          </g>
        </g>

        <!-- 条形 -->
        <g v-for="(bar,i) in klassBars" :key="i">
          <rect :x="bar.x" :y="bar.y" :width="bar.w" :height="bar.h" :fill="bar.fill"/>
          <text :x="bar.x + bar.w + 6" :y="bar.y + bar.h/2 + 4" font-size="12" fill="#334155">
            {{ bar.label }} ({{ bar.n }})
          </text>
        </g>

        <!-- X 轴标题 -->
        <text :x="klassCfg.w/2" :y="klassCfg.h - 2" text-anchor="middle" font-size="12" fill="#334155">
          Number of Records
        </text>
      </svg>
    </div>

    <!-- 月均 WQI 折线 -->
    <div v-show="tab==='time'" :class="['svg-wrap', { centered: full }]">
      <div class="hint">Monthly average WQI</div>
      <svg :width="tsCfg.w" :height="tsCfg.h" class="ts-svg">
        <!-- 轴线 -->
        <line :x1="tsCfg.pad" :x2="tsCfg.w - tsCfg.pad" :y1="tsCfg.h - tsCfg.pad" :y2="tsCfg.h - tsCfg.pad" stroke="#94a3b8" stroke-width="1"/>
        <line :x1="tsCfg.pad" :x2="tsCfg.pad" :y1="tsCfg.pad" :y2="tsCfg.h - tsCfg.pad" stroke="#94a3b8" stroke-width="1"/>

        <!-- 顶部的 Y 轴标题 -->
        <text :x="tsCfg.pad" :y="tsCfg.pad - 10" text-anchor="start" font-size="12" fill="#334155">
          Average WQI
        </text>

        <!-- x 轴刻度 -->
        <g v-if="tsTicks.x.length">
          <g v-for="(t,i) in tsTicks.x" :key="'tx'+i">
            <line :x1="t.x" :x2="t.x" :y1="tsCfg.h - tsCfg.pad" :y2="tsCfg.h - tsCfg.pad + 4" stroke="#94a3b8" stroke-width="1"/>
            <text :x="t.x" :y="tsCfg.h - tsCfg.pad + 14" text-anchor="middle" font-size="11" fill="#64748b">{{ t.label }}</text>
          </g>
        </g>
        <!-- y 轴刻度 -->
        <g v-if="tsTicks.y.length">
          <g v-for="(t,i) in tsTicks.y" :key="'ty'+i">
            <line :x1="tsCfg.pad - 4" :x2="tsCfg.pad" :y1="t.y" :y2="t.y" stroke="#94a3b8" stroke-width="1"/>
            <text :x="tsCfg.pad - 6" :y="t.y + 4" text-anchor="end" font-size="11" fill="#64748b">{{ t.label }}</text>
          </g>
        </g>

        <!-- 折线与点 -->
        <polyline :points="tsPath" fill="none" stroke="#0ea5e9" stroke-width="2"/>
        <g v-for="(p,i) in tsPoints" :key="i">
          <circle :cx="p.x" :cy="p.y" r="2.5" fill="#0ea5e9"/>
        </g>

        <!-- X 轴标题 -->
        <text :x="tsCfg.w/2" :y="tsCfg.h - 2" text-anchor="middle" font-size="12" fill="#334155">
          Time (Monthly)
        </text>
      </svg>
    </div>
  </section>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from "vue";

const props = defineProps({
  rows:  { type: Array,  required: true },   // 过滤后的记录
  cols:  { type: Object, required: true },   // 列名映射
  range: { type: Object, required: true },   // v-model:range {min,max,from,to}
  tab:   { type: String, required: true },   // v-model:tab
  full:  { type: Boolean, required: true },  // v-model:full
});
const emit = defineEmits(["update:range", "update:tab", "update:full"]);

function toDate(x){ const d = new Date(x); return isNaN(+d) ? null : d; }
function iso(d){ return d ? d.toISOString().slice(0,10) : ""; }

/** 画布尺寸（全屏时更大内边距，让图更居中不拥挤） */
const SMALL = { w: 260, h: 160, pad: 28 };
const LARGE = { w: 960, h: 520, pad: 40 };

/** ------- 直方图 ------- */
const hist = ref({ w: SMALL.w, h: SMALL.h, pad: SMALL.pad, bins: 10, barW: 0 });
const histogram = ref([]);
const histTicks = ref({ x: [], y: [] });

/** ------- Class 分布 ------- */
const klassCfg = ref({ w: SMALL.w, h: SMALL.h, pad: SMALL.pad, barH: 18, gap: 6 });
const klassBars = ref([]);
const klassTicks = ref({ x: [] });

/** ------- 月均折线 ------- */
const tsCfg = ref({ w: SMALL.w, h: SMALL.h, pad: SMALL.pad });
const tsPoints = ref([]);
const tsPath = ref("");
const tsTicks = ref({ x: [], y: [] });

/** 调整大小（含全屏切换时增加 pad） */
function setTrendsSize(full) {
  const S = full ? LARGE : SMALL;
  hist.value.w = klassCfg.value.w = tsCfg.value.w = S.w;
  hist.value.h = klassCfg.value.h = tsCfg.value.h = S.h;
  hist.value.pad = klassCfg.value.pad = tsCfg.value.pad = S.pad;
  buildHistogram(); buildKlassBars(); buildTimeSeries();
}
watch(() => props.full, v => setTrendsSize(v));

/** 全屏与 ESC 退出 */
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

/** ======= 三个图构建 ======= */
function buildHistogram() {
  const wqis = props.rows.map(r => r[props.cols.wqi]).filter(v => typeof v === "number" && isFinite(v));
  histogram.value = [];
  histTicks.value = { x: [], y: [] };
  if (!wqis.length) return;

  const min = Math.min(...wqis), max = Math.max(...wqis);
  const bins = Math.max(3, Math.min(60, hist.value.bins));
  const counts = Array.from({ length: bins }, () => 0);
  const step = (max - min) / bins || 1;

  for (const v of wqis) {
    let idx = Math.floor((v - min) / step);
    if (idx >= counts.length) idx = counts.length - 1;
    if (idx < 0) idx = 0;
    counts[idx]++;
  }

  const pad = hist.value.pad, W = hist.value.w - pad*2, H = hist.value.h - pad*2;
  const maxN = Math.max(...counts, 1);
  hist.value.barW = W / bins;

  histogram.value = counts.map((n, i) => {
    const barH = (n / maxN) * H;
    const x = pad + i * hist.value.barW;
    const y = hist.value.h - pad - barH;
    return { x, y, w: Math.max(1, hist.value.barW - 2), h: barH };
  });

  // 轴刻度
  const midV = (min + max) / 2;
  histTicks.value.x = [
    { x: pad,          label: min.toFixed(1) },
    { x: pad + W/2,    label: midV.toFixed(1) },
    { x: pad + W,      label: max.toFixed(1) },
  ];
  histTicks.value.y = [
    { y: hist.value.h - pad,     label: "0" },
    { y: hist.value.h - pad - H/2, label: Math.round(maxN/2).toString() },
    { y: hist.value.h - pad - H,   label: String(maxN) },
  ];
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

  // x 轴刻度
  klassTicks.value.x = [
    { x: pad,       label: "0" },
    { x: pad + W/2, label: Math.round(maxN/2).toString() },
    { x: pad + W,   label: String(maxN) },
  ];
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
  tsPoints.value = []; tsPath.value = ""; tsTicks.value = { x: [], y: [] };
  if (!rows.length) return;

  const pad = tsCfg.value.pad, W = tsCfg.value.w - pad*2, H = tsCfg.value.h - pad*2;
  const xs = rows.map(r => +r.date), ys = rows.map(r => r.value);
  const minX = Math.min(...xs), maxX = Math.max(...xs);
  const minY = Math.min(...ys), maxY = Math.max(...ys);
  const xOf = (t) => pad + (W * (t - minX)) / Math.max(1, maxX-minX);
  const yOf = (v) => (tsCfg.value.h - pad) - (H * (v - minY)) / Math.max(1e-6, maxY-minY);

  tsPoints.value = rows.map(r => ({ x: xOf(+r.date), y: yOf(r.value) }));
  tsPath.value = tsPoints.value.map(p => `${p.x},${p.y}`).join(" ");

  // 轴刻度：x 起/中/止 YYYY-MM，y min/中/max
  const fmt = (d) => `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}`;
  const midT = new Date((minX + maxX) / 2);
  const midY = (minY + maxY) / 2;
  tsTicks.value.x = [
    { x: xOf(minX),  label: fmt(new Date(minX)) },
    { x: xOf(+midT), label: fmt(midT) },
    { x: xOf(maxX),  label: fmt(new Date(maxX)) },
  ];
  tsTicks.value.y = [
    { y: yOf(minY),  label: minY.toFixed(1) },
    { y: yOf(midY),  label: midY.toFixed(1) },
    { y: yOf(maxY),  label: maxY.toFixed(1) },
  ];
}

/** 监听 */
watch(() => props.rows, () => { buildHistogram(); buildKlassBars(); buildTimeSeries(); }, { deep: true });
watch(() => [tsCfg.value.w, tsCfg.value.h, tsCfg.value.pad], buildTimeSeries);
watch(() => [hist.value.w, hist.value.h, hist.value.pad, hist.value.bins], buildHistogram);
watch(() => [klassCfg.value.w, klassCfg.value.h, klassCfg.value.pad], buildKlassBars);

function updateFrom(val) {
  if (!val) return;
  emit("update:range", { ...props.range, from: new Date(val) });
}
function updateTo(val) {
  if (!val) return;
  emit("update:range", { ...props.range, to: new Date(val) });
}

onMounted(() => setTrendsSize(false));
onUnmounted(() => {
  document.documentElement.style.overflow = "";
  document.body.style.overflow = "";
  document.removeEventListener("keydown", handleEsc);
});
</script>

<style scoped>
/* 全屏时让图更靠中间，并给左右留白 */
.trends-fullscreen {
  position: fixed; inset: 0; background: #fff; padding: 24px 36px;
  z-index: 1000; overflow: auto; display: grid; grid-template-columns: 1fr; gap: 12px;
}

/* 包一层容器，普通模式按原样显示；全屏时水平居中 */
.svg-wrap { width: 100%; }
.svg-wrap.centered { display: flex; justify-content: center; }

.hint { font-size: 12px; color: #64748b; margin: 6px 0; }
</style>
