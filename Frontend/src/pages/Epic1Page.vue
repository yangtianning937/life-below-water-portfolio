<template>
  <div class="epic1-container">
    <!-- 左侧 Sidebar：KPI + 图层 + Class 过滤 + Trends（含日期与全屏） -->
    <aside class="sidebar">
      <h2 class="title">Water Quality Dashboard</h2>

      <E1KPI :kpis="kpis" />

      <E1Layers v-model:show-heat="showHeat" v-model:show-markers="showMarkers" />

      <E1ClassFilter
        :options="classOptions"
        v-model:selected="selectedClassesArr"
        :color-for-class="colorForClass"
      />

      <E1Trends
        :rows="filteredRows"
        :cols="COLS"
        v-model:range="dateRange"
        v-model:tab="trendTab"
        v-model:full="trendsFull"
      />
    </aside>

    <!-- 右侧地图 -->
    <section class="map-wrap">
      <E1Map
        :rows="filteredRows"
        :cols="COLS"
        :show-heat="showHeat"
        :show-markers="showMarkers"
        :color-for-class="colorForClass"
      />
    </section>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref, computed, watch } from "vue";
import Papa from "papaparse";

/** 子组件 */
import E1KPI from "@/components/epic1/E1KPI.vue";
import E1Layers from "@/components/epic1/E1Layers.vue";
import E1ClassFilter from "@/components/epic1/E1ClassFilter.vue";
import E1Trends from "@/components/epic1/E1Trends.vue";
import E1Map from "@/components/epic1/E1Map.vue";

/** 列名映射（保持与原文件一致） */
const COLS = {
  lat:   "latitude",
  lon:   "longitude",
  wqi:   "water_quality_score",
  klass: "quality_label",
  date:  "date",
  name:  "site_name_short",
  body:  "water_body",
};

const loading = ref(false);
const error = ref("");
const rawRows = ref([]);
const filteredRows = ref([]);

/** Layers 开关 */
const showHeat = ref(true);
const showMarkers = ref(true);

/** Class 过滤 */
const classOptions = ref([]);              // 所有可选 class（字符串数组）
const selectedClassesArr = ref([]);        // v-model（数组）内部会转 Set 参与过滤

/** 日期与趋势 */
const dateRange = ref({ min: null, max: null, from: null, to: null });
const trendTab = ref("hist");
const trendsFull = ref(false);

/* 工具函数（保持原有配色逻辑） */
function colorForClass(k) {
  const palette = ["#2563EB","#16A34A","#9333EA","#0891B2","#EA580C","#DC2626","#6B7280","#059669","#1D4ED8","#7C3AED"];
  if (!k) return "#6B7280";
  let hash = 0, s = String(k);
  for (let i = 0; i < s.length; i++) hash = (hash * 31 + s.charCodeAt(i)) & 0xffffffff;
  return palette[Math.abs(hash) % palette.length];
}
function toDate(x){ const d = new Date(x); return isNaN(+d) ? null : d; }
function iso(d){ return d ? d.toISOString().slice(0,10) : ""; }

/** 基于已选 class + 日期进行过滤 */
function applyFilter() {
  const sel = new Set(selectedClassesArr.value.map(String));
  let rows = rawRows.value;

  if (sel.size) rows = rows.filter(r => sel.has(String(r[COLS.klass])));

  if (dateRange.value.from && dateRange.value.to) {
    rows = rows.filter(r => {
      const d = toDate(r[COLS.date]);
      return d && d >= dateRange.value.from && d <= dateRange.value.to;
    });
  }

  filteredRows.value = rows;
}

/** KPI 计算（保持与原逻辑一致） */
const kpis = computed(() => {
  const n = filteredRows.value.length;
  if (!n) return { count: 0, meanWQI: "-", dateSpan: "-" };

  const wqis = filteredRows.value
    .map(r => r[COLS.wqi])
    .filter(v => typeof v === "number" && isFinite(v));

  const meanWQI = wqis.length ? (wqis.reduce((a,b)=>a+b,0)/wqis.length).toFixed(1) : "-";
  const dates = filteredRows.value.map(r => toDate(r[COLS.date])).filter(Boolean).sort((a,b)=>a-b);

  let dateSpan = "-";
  if (dates.length) dateSpan = `${iso(dates[0])} ~ ${iso(dates.at(-1))}`;

  return { count: n, meanWQI, dateSpan };
});

/** 监听 filter 更改 */
watch(selectedClassesArr, applyFilter, { deep: true });
watch(dateRange, applyFilter, { deep: true });

/** 初始数据加载（与原文件一致：从本地 CSV 读） */
onMounted(async () => {
  try {
    loading.value = true;
    const url = new URL("../data/water_quality_classified.csv", import.meta.url).href;
    const data = await new Promise((resolve, reject) => {
      Papa.parse(url, {
        download: true, header: true, dynamicTyping: true, skipEmptyLines: true,
        complete: (res) => resolve(res.data), error: (err) => reject(err)
      });
    });

    // 清洗、映射
    rawRows.value = data.map(r => ({
      ...r,
      [COLS.lat]:  +r[COLS.lat],
      [COLS.lon]:  +r[COLS.lon],
      [COLS.wqi]:  +r[COLS.wqi],
      [COLS.date]: r[COLS.date],
    }));

    // Class 选项
    const uniq = Array.from(new Set(rawRows.value.map(r => String(r[COLS.klass]).trim()))).filter(Boolean).sort();
    classOptions.value = uniq;
    selectedClassesArr.value = []; // 默认不过滤

    // 日期范围
    const ds = rawRows.value.map(r => toDate(r[COLS.date])).filter(Boolean).sort((a,b)=>a-b);
    if (ds.length) {
      dateRange.value.min = ds[0];
      dateRange.value.max = ds.at(-1);
      dateRange.value.from = ds[0];
      dateRange.value.to   = ds.at(-1);
    }

    applyFilter();
  } catch (e) {
    console.error(e);
    error.value = "Failed to read or parse the CSV. Please check the data path and column name mapping.";
  } finally {
    loading.value = false;
  }
});

onUnmounted(() => {
  // 无全屏滚动锁定逻辑放在 Trends 子组件里处理
});
</script>

<style>
/* 保留你原文件中的样式（不改 class 名，确保子组件继续生效） */
.epic1-container { display: grid; grid-template-columns: 320px 1fr; gap: 12px; height: calc(100vh - 80px); padding: 12px; }
@media (max-width: 900px) { .epic1-container { grid-template-columns: 1fr; grid-auto-rows: auto; height: auto; } .map-wrap { height: 70vh; } }
.sidebar { background: #fff; border: 1px solid #e5e7eb; border-radius: 14px; padding: 14px; overflow: auto; }
.title { font-size: 18px; font-weight: 700; margin: 0 0 10px; }

.kpi { display: grid; grid-template-columns: repeat(3,1fr); gap: 8px; margin-bottom: 12px; }
.kpi-card { background: #f8fafc; border: 1px solid #e5e7eb; border-radius: 10px; padding: 10px; }
.kpi-label { font-size: 12px; color: #64748b; }
.kpi-value { font-size: 18px; font-weight: 700; }
.kpi-small { font-size: 12px; font-weight: 600; color: #334155; }

.panel { border: 1px solid #e5e7eb; border-radius: 10px; padding: 10px; margin-bottom: 12px; }
.panel-title { font-size: 14px; font-weight: 700; margin-bottom: 8px; }
.panel-title-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; }

.checkbox { display: flex; align-items: center; gap: 8px; margin: 6px 0; font-size: 14px; }
.btn-row { display: flex; gap: 8px; margin: 6px 0 8px; }
.btn { border: 1px solid #e5e7eb; background: #fff; padding: 4px 8px; border-radius: 8px; font-size: 12px; cursor: pointer; }
.btn:hover { background: #f3f4f6; }

.class-list { display: grid; grid-template-columns: 1fr; gap: 4px; max-height: 240px; overflow: auto; }
.color-dot { width: 10px; height: 10px; border-radius: 999px; display: inline-block; }

.tab-row { display: flex; gap: 8px; margin-bottom: 6px; }
.tab { padding: 4px 8px; border: 1px solid #e5e7eb; background: #fff; border-radius: 8px; cursor: pointer; font-size: 12px; }
.tab.active, .tab:hover { background: #f3f4f6; }

.icon-btn { border: 1px solid #e5e7eb; background: #fff; border-radius: 8px; padding: 4px; cursor: pointer; }
.icon-btn:hover { background: #f3f4f6; }

.hint { font-size: 12px; color: #64748b; margin: 6px 0; }

.map-wrap { background: #fff; border: 1px solid #e5e7eb; border-radius: 14px; overflow: hidden; position: relative; }
#map { width: 100%; height: 100%; min-height: 420px; }

.hist-svg, .klass-svg, .ts-svg { width: 100%; height: auto; display: block; }

.trends-fullscreen {
  position: fixed; inset: 0; background: #fff; padding: 16px;
  z-index: 1000; overflow: auto; display: grid; grid-template-columns: 1fr; gap: 10px;
}
.trends-fullscreen .panel { margin: 0; }
</style>
