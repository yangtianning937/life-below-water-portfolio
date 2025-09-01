<template>
  <div class="epic1-container">
    <!-- 左侧 Dashboard + Controls -->
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

      <!-- Layers -->
      <div class="panel">
        <div class="panel-title">Layers</div>
        <label class="checkbox"><input type="checkbox" v-model="showHeat" /> Heatmap (WQI)</label>
        <label class="checkbox"><input type="checkbox" v-model="showMarkers" /> Stations</label>
      </div>

      <!-- ✅ Classes -->
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

      <!-- ===== Trends（内含 Date + 全屏按钮） ===== -->
      <section class="panel">
        <div class="panel-title panel-title-row">
          <span>Trends</span>
          <button
            class="icon-btn"
            :title="trendsFull ? 'Restore' : 'Maximize'"
            @click="trendsFull = !trendsFull"
            aria-label="Toggle fullscreen">
            <svg v-if="!trendsFull" width="16" height="16" viewBox="0 0 24 24"><path d="M4 9V4h5M20 15v5h-5M20 9V4h-5M4 15v5" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
            <svg v-else            width="16" height="16" viewBox="0 0 24 24"><path d="M9 4H4v5M15 20h5v-5M15 4h5v5M9 20H4v-5" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
          </button>
        </div>

        <!-- Date -->
        <div class="panel soft panel-date" v-if="dateRange.min">
          <div class="panel-title">Date</div>
          <label class="date-row">
            <span>From</span>
            <input type="date" :min="iso(dateRange.min)" :max="iso(dateRange.max)" :value="iso(dateRange.from)"
                   @change="dateRange.from = new Date($event.target.value); applyFilter();" />
          </label>
          <label class="date-row">
            <span>To</span>
            <input type="date" :min="iso(dateRange.min)" :max="iso(dateRange.max)" :value="iso(dateRange.to)"
                   @change="dateRange.to = new Date($event.target.value); applyFilter();" />
          </label>
        </div>

        <!-- Tabs -->
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

        <div v-if="error" class="error">{{ error }}</div>
        <div v-if="loading" class="loading">Loading data…</div>
      </section>
    </aside>

    <!-- 右侧地图 -->
    <section class="map-wrap">
      <div ref="mapDiv" class="map"></div>
    </section>
  </div>

  <!-- ===== 全屏覆盖层（包含 Date + Tabs + 图表） ===== -->
  <teleport to="body">
    <div v-if="trendsFull" class="fullscreen-overlay" role="dialog" aria-modal="true">
      <div class="fullscreen-header">
        <h3>Trends (Fullscreen)</h3>
        <button class="icon-btn close-btn" @click="trendsFull = false" aria-label="Close">✖</button>
      </div>

      <div class="fullscreen-body">
        <!-- Date -->
        <div class="panel soft panel-date" v-if="dateRange.min">
          <div class="panel-title">Date</div>
          <label class="date-row">
            <span>From</span>
            <input type="date" :min="iso(dateRange.min)" :max="iso(dateRange.max)" :value="iso(dateRange.from)"
                   @change="dateRange.from = new Date($event.target.value); applyFilter();" />
          </label>
          <label class="date-row">
            <span>To</span>
            <input type="date" :min="iso(dateRange.min)" :max="iso(dateRange.max)" :value="iso(dateRange.to)"
                   @change="dateRange.to = new Date($event.target.value); applyFilter();" />
          </label>
        </div>

        <div class="tab-row" style="margin-bottom:10px">
          <button class="tab" :class="{ active: trendTab==='hist' }"  @click="trendTab='hist'">WQI Histogram</button>
          <button class="tab" :class="{ active: trendTab==='klass' }" @click="trendTab='klass'">Class Distribution</button>
          <button class="tab" :class="{ active: trendTab==='time' }"  @click="trendTab='time'">Monthly Avg WQI</button>
        </div>

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
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { onMounted, onUnmounted, ref, computed, watch } from "vue";
import L from "leaflet";
import "leaflet.heat";
import Papa from "papaparse";

/** 列名映射 */
const COLS = {
  lat:   "latitude",
  lon:   "longitude",
  wqi:   "water_quality_score",
  klass: "quality_label",
  date:  "date",
  name:  "site_name_short",
  body:  "water_body",
};

/* 状态 */
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

/* 工具 */
const iso = (d) => (d ? d.toISOString().slice(0, 10) : "");
const toDate = (v) => { if (!v) return null; const d = new Date(v); return isNaN(d) ? null : d; };

function colorForClass(k) {
  const palette = ["#2563EB","#16A34A","#9333EA","#0891B2","#EA580C","#DC2626","#6B7280","#059669","#1D4ED8","#7C3AED"];
  if (!k) return "#6B7280";
  let hash = 0, s = String(k);
  for (let i = 0; i < s.length; i++) hash = (hash * 31 + s.charCodeAt(i)) & 0xffffffff;
  return palette[Math.abs(hash) % palette.length];
}

/* 地图 */
function initMap() {
  if (map) return;
  map = L.map(mapDiv.value, { zoomControl: true, preferCanvas: true }).setView([-37.81, 144.96], 10);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { attribution: "© OpenStreetMap" }).addTo(map);
  heatLayer = L.heatLayer([], { radius: 22, blur: 18, maxZoom: 14 }).addTo(map);
  markersLayer = L.layerGroup().addTo(map);
}
function makeNormalizer(values) {
  const vs = values.filter(v => typeof v === "number" && isFinite(v));
  const min = Math.min(...vs), max = Math.max(...vs);
  const span = Math.max(1e-6, max - min);
  return v => (typeof v === "number" && isFinite(v)) ? Math.min(1, Math.max(0.05, (v - min) / span)) : 0.2;
}
function renderLayers() {
  if (!map) return;
  heatLayer.setLatLngs([]); markersLayer.clearLayers();
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
      const m = L.circleMarker([lat, lon], { radius: 5, weight: 1, color: colorForClass(r[COLS.klass]), fillOpacity: 0.75 });
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
  const pts = filteredRows.value.filter(r => isFinite(r[COLS.lat]) && isFinite(r[COLS.lon])).map(r => [r[COLS.lat], r[COLS.lon]]);
  if (pts.length) map.fitBounds(L.latLngBounds(pts).pad(0.05));
}

/* Trends（大小切换 + 全屏） */
const trendTab = ref("hist");
const trendsFull = ref(false);
const SMALL = { w: 260, h: 140 };
const LARGE = { w: 960, h: 480 };

const hist = { w: SMALL.w, h: SMALL.h, pad: 24, bins: 10, barW: 0 };
const histogram = ref([]);

const klassCfg = { w: SMALL.w, h: SMALL.h, pad: 24, barGap: 6 };
const klassBars = ref([]);

const tsCfg = { w: SMALL.w, h: SMALL.h, pad: 24 };
const tsPoints = ref([]);
const tsPath = ref("");

function setTrendsSize(full) {
  const S = full ? LARGE : SMALL;
  hist.w = klassCfg.w = tsCfg.w = S.w;
  hist.h = klassCfg.h = tsCfg.h = S.h;
  buildHistogram(); buildKlassBars(); buildTimeSeries();
}
watch(trendsFull, (v) => setTrendsSize(v));

function handleEsc(e){ if(e.key === "Escape") trendsFull.value = false; }
watch(trendsFull, (v) => {
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

function buildHistogram() {
  const wqis = filteredRows.value.map(r => r[COLS.wqi]).filter(v => typeof v === "number" && isFinite(v));
  if (!wqis.length) { histogram.value = []; return; }
  const min = Math.min(...wqis), max = Math.max(...wqis);
  const bins = Array.from({ length: hist.bins }, () => 0);
  const step = (max - min) / hist.bins || 1;
  wqis.forEach(v => { let idx = Math.floor((v - min) / step); if (idx >= hist.bins) idx = hist.bins - 1; if (idx < 0) idx = 0; bins[idx]++; });
  const maxC = Math.max(...bins), maxH = hist.h - 2 * hist.pad;
  hist.barW = (hist.w - 2 * hist.pad) / hist.bins;
  histogram.value = bins.map(c => ({ c, h: maxC ? (c / maxC) * maxH : 0 }));
}
function buildKlassBars() {
  const counts = new Map();
  filteredRows.value.forEach(r => { const k = r[COLS.klass] == null ? "N/A" : String(r[COLS.klass]); counts.set(k, (counts.get(k) || 0) + 1); });
  const entries = Array.from(counts.entries()).sort((a, b) => b[1] - a[1]);
  const maxC = entries.length ? Math.max(...entries.map(([, v]) => v)) : 0;
  const innerW = klassCfg.w - 2 * klassCfg.pad, innerH = klassCfg.h - 2 * klassCfg.pad;
  const barW = entries.length ? (innerW - (entries.length - 1) * klassCfg.barGap) / entries.length : 0;
  klassBars.value = entries.map(([label, v], i) => ({
    label, v,
    x: klassCfg.pad + i * (barW + klassCfg.barGap),
    y: klassCfg.h - klassCfg.pad - (maxC ? (v / maxC) * innerH : 0),
    width: barW, height: maxC ? (v / maxC) * innerH : 0,
    color: colorForClass(label),
  }));
}
function buildTimeSeries() {
  const rows = filteredRows.value.map(r => ({ d: toDate(r[COLS.date]), y: Number(r[COLS.wqi]) })).filter(o => o.d && isFinite(o.y));
  if (!rows.length) { tsPoints.value = []; tsPath.value = ""; return; }
  const m = new Map();
  rows.forEach(o => { const key = `${o.d.getFullYear()}-${String(o.d.getMonth() + 1).padStart(2, "0")}`; const agg = m.get(key) || { sum: 0, n: 0 }; agg.sum += o.y; agg.n += 1; m.set(key, agg); });
  const list = Array.from(m.entries()).map(([t, a]) => ({ t, y: a.sum / a.n })).sort((a, b) => a.t.localeCompare(b.t));
  const left = tsCfg.pad, right = tsCfg.w - tsCfg.pad, top = tsCfg.pad, bottom = tsCfg.h - tsCfg.pad;
  const minY = Math.min(...list.map(p => p.y)), maxY = Math.max(...list.map(p => p.y)), spanY = Math.max(1e-6, maxY - minY);
  const xStep = (right - left) / Math.max(1, list.length - 1);
  tsPoints.value = list.map((p, i) => ({ ...p, x: left + i * xStep, ypx: bottom - ((p.y - minY) / spanY) * (bottom - top) }));
  tsPath.value = tsPoints.value.reduce((d, p, i) => d + (i ? ` L ${p.x} ${p.ypx}` : `M ${p.x} ${p.ypx}`), "");
}

/* 数据 & 过滤 */
async function loadCSV() {
  const url = new URL("../data/water_quality_classified.csv", import.meta.url).href
  return new Promise((resolve, reject) => {
    Papa.parse(url, { download: true, header: true, dynamicTyping: true, skipEmptyLines: true,
      complete: (res) => resolve(res.data), error: (err) => reject(err) })
  })
}
function applyFilter() {
  let rows = rawRows.value;
  if (selectedClasses.value.size) rows = rows.filter(r => selectedClasses.value.has(String(r[COLS.klass])));
  if (dateRange.value.from && dateRange.value.to) {
    rows = rows.filter(r => { const d = toDate(r[COLS.date]); return d && d >= dateRange.value.from && d <= dateRange.value.to; });
  }
  filteredRows.value = rows;
  buildHistogram(); buildKlassBars(); buildTimeSeries(); renderLayers();
}
const kpis = computed(() => {
  const n = filteredRows.value.length;
  if (!n) return { count: 0, meanWQI: "-", dateSpan: "-" };
  const wqis = filteredRows.value.map(r => r[COLS.wqi]).filter(v => typeof v === "number" && isFinite(v));
  const meanWQI = wqis.length ? (wqis.reduce((a, b) => a + b, 0) / wqis.length).toFixed(1) : "-";
  const dates = filteredRows.value.map(r => toDate(r[COLS.date])).filter(Boolean).sort((a, b) => a - b);
  let dateSpan = "-"; if (dates.length) dateSpan = `${iso(dates[0])} ~ ${iso(dates.at(-1))}`;
  return { count: n, meanWQI, dateSpan };
});

/* 交互 */
function selectAllClasses() { selectedClasses.value = new Set(classOptions.value); applyFilter(); }
function clearClasses()      { selectedClasses.value = new Set();               applyFilter(); }
function toggleClass(k, checked) { const next = new Set(selectedClasses.value); checked ? next.add(k) : next.delete(k); selectedClasses.value = next; applyFilter(); }
watch([showHeat, showMarkers], renderLayers);

/* 生命周期 */
function onResize(){ setTrendsSize(trendsFull.value); }

onMounted(async () => {
  try {
    const rows = await loadCSV();
    rawRows.value = rows
      .map(r => {
        const lat = Number(r[COLS.lat]), lon = Number(r[COLS.lon]), wqi = Number(r[COLS.wqi]);
        return { ...r, [COLS.lat]: isFinite(lat) ? lat : null, [COLS.lon]: isFinite(lon) ? lon : null, [COLS.wqi]: isFinite(wqi) ? wqi : null };
      })
      .filter(r => r[COLS.lat] != null && r[COLS.lon] != null);

    classOptions.value = Array.from(new Set(rawRows.value.map(r => r[COLS.klass]).filter(v => v != null))).map(String).sort();
    selectedClasses.value = new Set(classOptions.value);

    const dates = rawRows.value.map(r => toDate(r[COLS.date])).filter(Boolean).sort((a, b) => a - b);
    if (dates.length) { dateRange.value.min = dates[0]; dateRange.value.max = dates.at(-1); dateRange.value.from = dates[0]; dateRange.value.to = dates.at(-1); }

    initMap();
    applyFilter();
    setTrendsSize(false); // 初始小窗
  } catch (e) {
    console.error(e); error.value = "Failed to read or parse the CSV. Please check the data path and column name mapping.";
  } finally { loading.value = false; }

  window.addEventListener('resize', onResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', onResize);
  document.documentElement.style.overflow = "";
  document.body.style.overflow = "";
  document.removeEventListener("keydown", handleEsc);
});
</script>

<style scoped>
.epic1-container { display: grid; grid-template-columns: 320px 1fr; gap: 12px; height: calc(100vh - 80px); padding: 12px; }
@media (max-width: 900px) { .epic1-container { grid-template-columns: 1fr; grid-auto-rows: auto; height: auto; } .map-wrap { height: 70vh; } }
.sidebar { background: #fff; border: 1px solid #e5e7eb; border-radius: 14px; padding: 14px; overflow: auto; }
.title { font-size: 18px; font-weight: 700; margin: 0 0 10px; }

.kpi { display: grid; grid-template-columns: repeat(3,1fr); gap: 8px; margin-bottom: 10px; }
.kpi-card { border:1px solid #e5e7eb; border-radius:10px; padding:10px; text-align:center; }
.kpi-label { font-size: 12px; color:#6b7280; }
.kpi-value { font-size: 18px; font-weight: 700; }
.kpi-small { font-size: 11px; white-space: nowrap; }

.panel { border-top:1px dashed #e5e7eb; padding-top:10px; margin-top:10px; }
.panel.soft { border-top-style: solid; border-top-color: #f1f5f9; }
.panel-title { font-weight: 600; margin-bottom: 6px; }
.panel-title-row{ display:flex; align-items:center; justify-content:space-between; }

.checkbox { display:flex; align-items:center; gap:8px; margin:4px 0; font-size:14px; }
.btn-row { display:flex; gap:6px; margin-bottom:6px; }
.btn { border:1px solid #e5e7eb; background:#f9fafb; border-radius:8px; padding:4px 8px; font-size:12px; cursor:pointer; }
.class-list { max-height: 140px; overflow:auto; padding-right:6px; }
.color-dot { display:inline-block; width:10px; height:10px; border-radius:999px; border:1px solid #e5e7eb; }

.panel-date { margin-bottom: 8px; }
.date-row { display:flex; align-items:center; gap:8px; margin:6px 0; }
.date-row span { width: 40px; color:#6b7280; font-size: 13px; }

.tab-row{display:flex;gap:6px;margin-bottom:8px}
.tab{border:1px solid #e5e7eb;background:#f9fafb;border-radius:8px;padding:4px 8px;font-size:12px;cursor:pointer}
.tab.active{background:#e0ecff;border-color:#93c5fd;color:#1d4ed8}

.icon-btn{ display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border:1px solid #e5e7eb; border-radius:8px; background:#f9fafb; cursor:pointer; padding:0; }
.icon-btn:hover{ background:#eef2ff; border-color:#c7d2fe; }

.hint { font-size: 12px; color:#6b7280; margin-bottom: 6px; }
.hist-svg { width: 100%; border:1px solid #e5e7eb; border-radius:8px; background:#fff; }

.error { color:#dc2626; margin-top:8px; font-size: 13px; }
.loading { color:#6b7280; margin-top:8px; font-size: 13px; }

.map-wrap { position: relative; }
.map { width: 100%; height: 100%; border:1px solid #e5e7eb; border-radius: 14px; overflow: hidden; }

/* 全屏覆盖层 */
.fullscreen-overlay{
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: #fff;
  display: flex;
  flex-direction: column;
}
.fullscreen-header{
  display:flex;align-items:center;justify-content:space-between;
  padding: 12px 14px;
  border-bottom: 1px solid #e5e7eb;
  background: #f8fafc;
}
.fullscreen-body{
  flex:1; min-height:0; overflow:auto; padding: 12px 14px;
}
.close-btn{ font-size: 18px; }
</style>
