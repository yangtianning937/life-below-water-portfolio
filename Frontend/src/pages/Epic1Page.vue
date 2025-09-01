<template>
  <div class="epic1-container">
    <!-- 左侧 Dashboard + Trends -->
    <aside class="sidebar">
      <h2 class="title">Water Quality Dashboard</h2>

      <!-- KPI -->
      <div class="kpi">
        <div class="kpi-card">
          <div class="kpi-label">Records</div>
          <div class="kpi-value">{{ kpis.count }}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Avg WQI</div>
          <div class="kpi-value">{{ kpis.meanWQI }}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Date Range</div>
          <div class="kpi-value kpi-small">{{ kpis.dateSpan }}</div>
        </div>
      </div>

      <!-- 图层开关 -->
      <div class="panel">
        <div class="panel-title">Layers</div>
        <label class="checkbox">
          <input type="checkbox" v-model="showHeat" />
          Heatmap (WQI)
        </label>
        <label class="checkbox">
          <input type="checkbox" v-model="showMarkers" />
          Stations
        </label>
      </div>

      <!-- 分类过滤 -->
      <div class="panel">
        <div class="panel-title">Classes</div>
        <div class="btn-row">
          <button class="btn" @click="selectAllClasses()">Select all</button>
          <button class="btn" @click="clearClasses()">Clear</button>
        </div>
        <div class="class-list">
          <label v-for="k in classOptions" :key="k" class="checkbox">
            <input
              type="checkbox"
              :checked="selectedClasses.has(k)"
              @change="toggleClass(k, $event.target.checked)"
            />
            <span class="color-dot" :style="{ background: colorForClass(k) }"></span>
            <span>{{ k }}</span>
          </label>
        </div>
      </div>

      <!-- 日期过滤 -->
      <div class="panel" v-if="dateRange.min">
        <div class="panel-title">Date</div>
        <label class="date-row">
          <span>From</span>
          <input
            type="date"
            :min="iso(dateRange.min)"
            :max="iso(dateRange.max)"
            :value="iso(dateRange.from)"
            @change="dateRange.from = new Date($event.target.value); applyFilter();"
          />
        </label>
        <label class="date-row">
          <span>To</span>
          <input
            type="date"
            :min="iso(dateRange.min)"
            :max="iso(dateRange.max)"
            :value="iso(dateRange.to)"
            @change="dateRange.to = new Date($event.target.value); applyFilter();"
          />
        </label>
      </div>

      <!-- ===== Trends 面板（3 个可切换图） ===== -->
      <section class="panel">
        <div class="panel-title">Trends</div>
        <div class="tab-row">
          <button class="tab" :class="{ active: trendTab==='hist' }"  @click="trendTab='hist'">WQI Histogram</button>
          <button class="tab" :class="{ active: trendTab==='klass' }" @click="trendTab='klass'">Class Distribution</button>
          <button class="tab" :class="{ active: trendTab==='time' }"  @click="trendTab='time'">Monthly Avg WQI</button>
        </div>

        <!-- WQI Histogram -->
        <div v-show="trendTab==='hist'">
          <div class="hint">Distribution of water_quality_score</div>
          <svg :width="hist.w" :height="hist.h" class="hist-svg">
            <line :x1="hist.pad" :x2="hist.w - hist.pad" :y1="hist.h - hist.pad" :y2="hist.h - hist.pad" stroke="#9CA3AF"/>
            <line :x1="hist.pad" :x2="hist.pad" :y1="hist.pad" :y2="hist.h - hist.pad" stroke="#9CA3AF"/>
            <template v-for="(b,i) in histogram" :key="i">
              <rect :x="hist.pad + i*hist.barW" :y="hist.h - hist.pad - b.h" :width="hist.barW-1" :height="b.h" fill="#60A5FA"/>
            </template>
          </svg>
        </div>

        <!-- Class Distribution -->
        <div v-show="trendTab==='klass'">
          <div class="hint">Count by quality_label</div>
          <svg :width="klassCfg.w" :height="klassCfg.h" class="hist-svg">
            <line :x1="klassCfg.pad" :x2="klassCfg.w - klassCfg.pad" :y1="klassCfg.h - klassCfg.pad" :y2="klassCfg.h - klassCfg.pad" stroke="#9CA3AF"/>
            <line :x1="klassCfg.pad" :x2="klassCfg.pad" :y1="klassCfg.pad" :y2="klassCfg.h - klassCfg.pad" stroke="#9CA3AF"/>
            <template v-for="b in klassBars" :key="b.label">
              <rect :x="b.x" :y="b.y" :width="b.width" :height="b.height" :fill="b.color"/>
              <text :x="b.x + b.width/2" :y="klassCfg.h - 6" text-anchor="middle" font-size="10" fill="#6B7280">{{ b.label }}</text>
            </template>
          </svg>
        </div>

        <!-- Monthly Avg WQI -->
        <div v-show="trendTab==='time'">
          <div class="hint">Average water_quality_score by month</div>
          <svg :width="tsCfg.w" :height="tsCfg.h" class="hist-svg">
            <line :x1="tsCfg.pad" :x2="tsCfg.w - tsCfg.pad" :y1="tsCfg.h - tsCfg.pad" :y2="tsCfg.h - tsCfg.pad" stroke="#9CA3AF"/>
            <line :x1="tsCfg.pad" :x2="tsCfg.pad" :y1="tsCfg.pad" :y2="tsCfg.h - tsCfg.pad" stroke="#9CA3AF"/>
            <path v-if="tsPath" :d="tsPath" fill="none" stroke="#2563EB" stroke-width="2"/>
            <template v-for="p in tsPoints" :key="p.t">
              <circle :cx="p.x" :cy="p.ypx" r="2.5" fill="#2563EB"/>
              <text :x="p.x" :y="tsCfg.h - 6" text-anchor="middle" font-size="10" fill="#6B7280">{{ p.t }}</text>
            </template>
          </svg>
        </div>
      </section>

      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="loading" class="loading">Loading data…</div>
    </aside>

    <!-- 右侧地图 -->
    <section class="map-wrap">
      <div ref="mapDiv" class="map"></div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref, computed, watch } from "vue";
import L from "leaflet";
import "leaflet.heat";
import Papa from "papaparse";

/** === 列名映射（与你的 CSV 对齐） ===
 * 如果你的 CSV 列名不同，改这里即可
 */
const COLS = {
  lat:   "latitude",
  lon:   "longitude",
  wqi:   "water_quality_score",
  klass: "quality_label",
  date:  "date",
  name:  "site_name_short",
  body:  "water_body",
};

// ====== 状态 ======
const mapDiv = ref(null);
let map, heatLayer, markersLayer;

const rawRows = ref([]);
const filteredRows = ref([]);

const classOptions = ref([]);
const selectedClasses = ref(new Set());

const showHeat = ref(true);
const showMarkers = ref(true);

const loading = ref(true);
const error = ref("");

const dateRange = ref({ min: null, max: null, from: null, to: null });

// 工具函数
const iso = (d) => (d ? d.toISOString().slice(0, 10) : "");
const toDate = (v) => { if (!v) return null; const d = new Date(v); return isNaN(d) ? null : d; };

// ===== 地图初始化 =====
function initMap() {
  if (map) return;
  map = L.map(mapDiv.value, { zoomControl: true, preferCanvas: true })
    .setView([-37.81, 144.96], 10);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap"
  }).addTo(map);

  heatLayer = L.heatLayer([], { radius: 22, blur: 18, maxZoom: 14 }).addTo(map);
  markersLayer = L.layerGroup().addTo(map);
}

// 颜色
function colorForClass(k) {
  const palette = [
    "#2563EB","#16A34A","#9333EA","#0891B2","#EA580C",
    "#DC2626","#6B7280","#059669","#1D4ED8","#7C3AED",
  ];
  if (!k) return "#6B7280";
  let hash = 0;
  const s = String(k);
  for (let i = 0; i < s.length; i++) hash = (hash * 31 + s.charCodeAt(i)) & 0xffffffff;
  return palette[Math.abs(hash) % palette.length];
}

// 权重归一化（WQI→0~1）
function makeNormalizer(values) {
  const vs = values.filter(v => typeof v === "number" && isFinite(v));
  const min = Math.min(...vs), max = Math.max(...vs);
  const span = Math.max(1e-6, max - min);
  return v => (typeof v === "number" && isFinite(v)) ? Math.min(1, Math.max(0.05, (v - min) / span)) : 0.2;
}

// 渲染热力 & 点位
function renderLayers() {
  if (!map) return;
  heatLayer.setLatLngs([]);
  markersLayer.clearLayers();

  if (!filteredRows.value.length) return;

  const norm = makeNormalizer(filteredRows.value.map(r => r[COLS.wqi]));

  if (showHeat.value) {
    const heat = filteredRows.value
      .filter(r => isFinite(r[COLS.lat]) && isFinite(r[COLS.lon]))
      .map(r => [r[COLS.lat], r[COLS.lon], norm(r[COLS.wqi])]);
    heatLayer.setLatLngs(heat);
  }

  if (showMarkers.value) {
    filteredRows.value.forEach(r => {
      const lat = r[COLS.lat], lon = r[COLS.lon];
      if (!isFinite(lat) || !isFinite(lon)) return;

      const m = L.circleMarker([lat, lon], {
        radius: 5, weight: 1,
        color: colorForClass(r[COLS.klass]),
        fillOpacity: 0.75
      });

      const popup = `
        <div style="font-size:12px;line-height:1.4">
          <div><b>${r[COLS.name] ?? "N/A"}</b></div>
          <div>${r[COLS.body] ?? ""}</div>
          <div>Class: <b>${r[COLS.klass] ?? "N/A"}</b></div>
          <div>WQI: <b>${r[COLS.wqi] ?? "N/A"}</b></div>
        </div>`;
      m.bindPopup(popup);
      markersLayer.addLayer(m);
    });
  }

  // 自适应视图
  const pts = filteredRows.value
    .filter(r => isFinite(r[COLS.lat]) && isFinite(r[COLS.lon]))
    .map(r => [r[COLS.lat], r[COLS.lon]]);
  if (pts.length) {
    const bounds = L.latLngBounds(pts);
    map.fitBounds(bounds.pad(0.05));
  }
}

// ===== Trends：直方图 =====
const trendTab = ref("hist");
const hist = { w: 260, h: 140, pad: 24, bins: 10, barW: 0 };
const histogram = ref([]);

function buildHistogram() {
  const wqis = filteredRows.value
    .map((r) => r[COLS.wqi])
    .filter((v) => typeof v === "number" && isFinite(v));
  if (!wqis.length) { histogram.value = []; return; }
  const min = Math.min(...wqis), max = Math.max(...wqis);
  const bins = Array.from({ length: hist.bins }, () => 0);
  const step = (max - min) / hist.bins || 1;
  wqis.forEach((v) => {
    let idx = Math.floor((v - min) / step);
    if (idx >= hist.bins) idx = hist.bins - 1;
    if (idx < 0) idx = 0;
    bins[idx]++;
  });
  const maxC = Math.max(...bins);
  const maxH = hist.h - 2 * hist.pad;
  hist.barW = (hist.w - 2 * hist.pad) / hist.bins;
  histogram.value = bins.map((c) => ({ c, h: maxC ? (c / maxC) * maxH : 0 }));
}

// ===== Trends：等级分布 =====
const klassCfg = { w: 260, h: 140, pad: 24, barGap: 6 };
const klassBars = ref([]);

function buildKlassBars() {
  const counts = new Map();
  filteredRows.value.forEach((r) => {
    const k = r[COLS.klass] == null ? "N/A" : String(r[COLS.klass]);
    counts.set(k, (counts.get(k) || 0) + 1);
  });
  const entries = Array.from(counts.entries()).sort((a, b) => b[1] - a[1]);
  const maxC = entries.length ? Math.max(...entries.map(([, v]) => v)) : 0;
  const innerW = klassCfg.w - 2 * klassCfg.pad;
  const barW = entries.length
    ? (innerW - (entries.length - 1) * klassCfg.barGap) / entries.length
    : 0;
  const innerH = klassCfg.h - 2 * klassCfg.pad;
  klassBars.value = entries.map(([label, v], i) => ({
    label,
    v,
    x: klassCfg.pad + i * (barW + klassCfg.barGap),
    y: klassCfg.h - klassCfg.pad - (maxC ? (v / maxC) * innerH : 0),
    width: barW,
    height: maxC ? (v / maxC) * innerH : 0,
    color: colorForClass(label),
  }));
}

// ===== Trends：月均折线 =====
const tsCfg = { w: 260, h: 140, pad: 24 };
const tsPoints = ref([]);  // [{t:'YYYY-MM', y, x, ypx}]
const tsPath = ref("");

function buildTimeSeries() {
  const rows = filteredRows.value
    .map((r) => ({ d: toDate(r[COLS.date]), y: Number(r[COLS.wqi]) }))
    .filter((o) => o.d && isFinite(o.y));
  if (!rows.length) { tsPoints.value = []; tsPath.value = ""; return; }

  const m = new Map();
  rows.forEach((o) => {
    const key = `${o.d.getFullYear()}-${String(o.d.getMonth() + 1).padStart(2, "0")}`;
    const agg = m.get(key) || { sum: 0, n: 0 };
    agg.sum += o.y; agg.n += 1; m.set(key, agg);
  });
  const list = Array.from(m.entries())
    .map(([t, a]) => ({ t, y: a.sum / a.n }))
    .sort((a, b) => a.t.localeCompare(b.t));

  const left = tsCfg.pad, right = tsCfg.w - tsCfg.pad;
  const top = tsCfg.pad, bottom = tsCfg.h - tsCfg.pad;
  const minY = Math.min(...list.map((p) => p.y));
  const maxY = Math.max(...list.map((p) => p.y));
  const spanY = Math.max(1e-6, maxY - minY);
  const xStep = (right - left) / Math.max(1, list.length - 1);

  tsPoints.value = list.map((p, i) => ({
    ...p,
    x: left + i * xStep,
    ypx: bottom - ((p.y - minY) / spanY) * (bottom - top),
  }));
  tsPath.value = tsPoints.value.reduce(
    (d, p, i) => d + (i ? ` L ${p.x} ${p.ypx}` : `M ${p.x} ${p.ypx}`),
    ""
  );
}

// ===== 加载 & 过滤 =====
async function loadCSV() {
  const url = new URL("../data/water_quality_classified.csv", import.meta.url).href;
  return new Promise((resolve, reject) => {
    Papa.parse(url, {
      download: true,
      header: true,
      dynamicTyping: true,
      skipEmptyLines: true,
      complete: (res) => resolve(res.data),
      error: (err) => reject(err),
    });
  });
}

function applyFilter() {
  let rows = rawRows.value;

  // 分类过滤
  if (selectedClasses.value.size) {
    rows = rows.filter((r) => selectedClasses.value.has(String(r[COLS.klass])));
  }

  // 日期过滤
  if (dateRange.value.from && dateRange.value.to) {
    rows = rows.filter((r) => {
      const d = toDate(r[COLS.date]);
      return d && d >= dateRange.value.from && d <= dateRange.value.to;
    });
  }

  filteredRows.value = rows;

  // 重建图表 & 地图图层
  buildHistogram();
  buildKlassBars();
  buildTimeSeries();
  renderLayers();
}

// KPI
const kpis = computed(() => {
  const n = filteredRows.value.length;
  if (!n) return { count: 0, meanWQI: "-", dateSpan: "-" };

  const wqis = filteredRows.value
    .map((r) => r[COLS.wqi])
    .filter((v) => typeof v === "number" && isFinite(v));
  const meanWQI = wqis.length
    ? (wqis.reduce((a, b) => a + b, 0) / wqis.length).toFixed(1)
    : "-";

  const dates = filteredRows.value
    .map((r) => toDate(r[COLS.date]))
    .filter(Boolean)
    .sort((a, b) => a - b);
  let dateSpan = "-";
  if (dates.length) {
    dateSpan = `${iso(dates[0])} ~ ${iso(dates.at(-1))}`;
  }
  return { count: n, meanWQI, dateSpan };
});

// 交互辅助
function selectAllClasses() { selectedClasses.value = new Set(classOptions.value); applyFilter(); }
function clearClasses()      { selectedClasses.value = new Set();               applyFilter(); }
function toggleClass(k, checked) {
  const next = new Set(selectedClasses.value);
  if (checked) next.add(k); else next.delete(k);
  selectedClasses.value = next;
  applyFilter();
}

// 同步图层开关
watch([showHeat, showMarkers], renderLayers);

// 生命周期
onMounted(async () => {
  try {
    const rows = await loadCSV();

    rawRows.value = rows
      .map((r) => {
        const lat = Number(r[COLS.lat]);
        const lon = Number(r[COLS.lon]);
        const wqi = Number(r[COLS.wqi]);
        return {
          ...r,
          [COLS.lat]: isFinite(lat) ? lat : null,
          [COLS.lon]: isFinite(lon) ? lon : null,
          [COLS.wqi]: isFinite(wqi) ? wqi : null,
        };
      })
      .filter((r) => r[COLS.lat] != null && r[COLS.lon] != null); // 只有有坐标的记录

    // 分类（默认全选）
    classOptions.value = Array.from(
      new Set(rawRows.value.map((r) => r[COLS.klass]).filter((v) => v != null))
    ).map(String).sort();
    selectedClasses.value = new Set(classOptions.value);

    // 日期范围（如有）
    const dates = rawRows.value.map((r) => toDate(r[COLS.date])).filter(Boolean).sort((a,b)=>a-b);
    if (dates.length) {
      dateRange.value.min  = dates[0];
      dateRange.value.max  = dates.at(-1);
      dateRange.value.from = dates[0];
      dateRange.value.to   = dates.at(-1);
    }

    // 初始化地图并首次渲染
    initMap();
    applyFilter();
  } catch (e) {
    console.error(e);
    error.value = "CSV 读取或解析失败，请检查数据路径与列名映射。";
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.epic1-container {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 12px;
  height: calc(100vh - 80px);
  padding: 12px;
}
@media (max-width: 900px) {
  .epic1-container { grid-template-columns: 1fr; grid-auto-rows: auto; height: auto; }
  .map-wrap { height: 70vh; }
}
.sidebar {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 14px;
  overflow: auto;
}
.title { font-size: 18px; font-weight: 700; margin: 0 0 10px; }
.kpi { display: grid; grid-template-columns: repeat(3,1fr); gap: 8px; margin-bottom: 10px; }
.kpi-card { border:1px solid #e5e7eb; border-radius:10px; padding:10px; text-align:center; }
.kpi-label { font-size: 12px; color:#6b7280; }
.kpi-value { font-size: 18px; font-weight: 700; }
.kpi-small { font-size: 11px; white-space: nowrap; }

.panel { border-top:1px dashed #e5e7eb; padding-top:10px; margin-top:10px; }
.panel-title { font-weight: 600; margin-bottom: 6px; }
.checkbox { display:flex; align-items:center; gap:8px; margin:4px 0; font-size:14px; }
.btn-row { display:flex; gap:6px; margin-bottom:6px; }
.btn { border:1px solid #e5e7eb; background:#f9fafb; border-radius:8px; padding:4px 8px; font-size:12px; cursor:pointer; }
.class-list { max-height: 140px; overflow:auto; padding-right:6px; }
.color-dot { display:inline-block; width:10px; height:10px; border-radius:999px; border:1px solid #e5e7eb; }

.date-row { display:flex; align-items:center; gap:8px; margin:6px 0; }
.date-row span { width: 40px; color:#6b7280; font-size: 13px; }

.tab-row{display:flex;gap:6px;margin-bottom:8px}
.tab{border:1px solid #e5e7eb;background:#f9fafb;border-radius:8px;padding:4px 8px;font-size:12px;cursor:pointer}
.tab.active{background:#e0ecff;border-color:#93c5fd;color:#1d4ed8}

.hint { font-size: 12px; color:#6b7280; margin-bottom: 6px; }
.hist-svg { width: 100%; border:1px solid #e5e7eb; border-radius:8px; background:#fff; }

.error { color:#dc2626; margin-top:8px; font-size: 13px; }
.loading { color:#6b7280; margin-top:8px; font-size: 13px; }

.map-wrap { position: relative; }
.map { width: 100%; height: 100%; border:1px solid #e5e7eb; border-radius: 14px; overflow: hidden; }
</style>
