<template>
  <div class="w-full h-full">
    <!--    &lt;!&ndash; 左侧：KPI + Class 过滤 + Trends &ndash;&gt;-->
    <!--    <aside class="sidebar">-->
    <!--      <h2 class="title">Water Quality Dashboard</h2>-->

    <!--      <E1KPI :kpis="kpis" />-->

    <!--      <E1ClassFilter-->
    <!--        :options="classOptions"-->
    <!--        v-model:selected="selectedClassesArr"-->
    <!--        :color-for-class="colorForClass"-->
    <!--      />-->

    <!--      <E1Trends-->
    <!--        :rows="filteredRows"-->
    <!--        :cols="COLS"-->
    <!--        v-model:range="dateRange"-->
    <!--        v-model:tab="trendTab"-->
    <!--        v-model:full="trendsFull"-->
    <!--      />-->
    <!--    </aside>-->

    <!-- 右侧：Tableau -->
    <section class="map-wrap">
      <E1Tableau
          :url="tableauUrl"
          :height="630"
          :maxWidth="1600"
          decalsDensity="high"
      />
    </section>
  </div>
</template>

<script setup>
import {onMounted, ref, computed, watch} from "vue";
import Papa from "papaparse";

/** 子组件 */
import E1KPI from "@/components/epic1/E1KPI.vue";
import E1ClassFilter from "@/components/epic1/E1ClassFilter.vue";
import E1Trends from "@/components/epic1/E1Trends.vue";
import E1Tableau from "@/components/epic1/E1Tableau.vue";


const tableauUrl =
    "https://public.tableau.com/views/NewWorkbook_17569007097240/Sheet1?:showVizHome=no&:embed=y&:toolbar=yes&:tabs=no";

/** 列名映射 */
const COLS = {
  lat: "latitude",
  lon: "longitude",
  wqi: "water_quality_score",
  klass: "quality_label",
  date: "date",
  name: "site_name_short",
  body: "water_body",
};

const loading = ref(false);
const error = ref("");
const rawRows = ref([]);
const filteredRows = ref([]);

/** Class 过滤 */
const classOptions = ref([]);
const selectedClassesArr = ref([]);

/** 日期与趋势 */
const dateRange = ref({min: null, max: null, from: null, to: null});
const trendTab = ref("hist");
const trendsFull = ref(false);

/** 颜色映射 */
function colorForClass(k) {
  const KEY = String(k || "").trim().toLowerCase();
  const MAP = {
    darkred: "#b91c1c",
    orange: "#f97316",
    green: "#22c55e",
    yellow: "#facc15",
  };
  return MAP[KEY] || "#6b7280";
}

const toDate = (x) => {
  const d = new Date(x);
  return isNaN(+d) ? null : d;
};
const iso = (d) => (d ? d.toISOString().slice(0, 10) : "");

/** 应用过滤：按 Class + 日期 */
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

/** KPI */
const kpis = computed(() => {
  const n = filteredRows.value.length;
  if (!n) return {count: 0, meanWQI: "-", dateSpan: "-"};

  const wqis = filteredRows.value
      .map(r => r[COLS.wqi])
      .filter(v => typeof v === "number" && isFinite(v));

  const meanWQI = wqis.length ? (wqis.reduce((a, b) => a + b, 0) / wqis.length).toFixed(1) : "-";
  const dates = filteredRows.value.map(r => toDate(r[COLS.date])).filter(Boolean).sort((a, b) => a - b);
  const dateSpan = dates.length ? `${iso(dates[0])} ~ ${iso(dates.at(-1))}` : "-";
  return {count: n, meanWQI, dateSpan};
});

watch(selectedClassesArr, applyFilter, {deep: true});
watch(dateRange, applyFilter, {deep: true});

/** 加载 CSV */
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

    // 基础清洗（WQI 转数字；经纬度即使清洗，也只用于统计，不再渲染地图）
    rawRows.value = data.map(r => ({
      ...r,
      [COLS.lat]: +r[COLS.lat],
      [COLS.lon]: +r[COLS.lon],
      [COLS.wqi]: +r[COLS.wqi],
      [COLS.date]: r[COLS.date],
    }));

    // Class 选项
    const uniq = Array.from(new Set(rawRows.value.map(r => String(r[COLS.klass]).trim())))
        .filter(Boolean).sort();
    classOptions.value = uniq;
    selectedClassesArr.value = []; // 默认不过滤

    // 日期范围
    const ds = rawRows.value.map(r => toDate(r[COLS.date])).filter(Boolean).sort((a, b) => a - b);
    if (ds.length) {
      dateRange.value.min = ds[0];
      dateRange.value.max = ds.at(-1);
      dateRange.value.from = ds[0];
      dateRange.value.to = ds.at(-1);
    }

    applyFilter();
  } catch (e) {
    console.error(e);
    error.value = "Failed to read or parse the CSV. Please check the data path and column name mapping.";
  } finally {
    loading.value = false;
  }
});
</script>

<style>
.epic1-container {
  height: 100%;
  width: 100%;
}

.sidebar {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 14px;
  overflow: auto;
}

.title {
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 10px;
}

.kpi {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-bottom: 12px;
}

.kpi-card {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 10px;
}

.kpi-label {
  font-size: 12px;
  color: #64748b;
}

.kpi-value {
  font-size: 18px;
  font-weight: 700;
}

.kpi-small {
  font-size: 12px;
  font-weight: 600;
  color: #334155;
}

.panel {
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 10px;
  margin-bottom: 12px;
}

.panel-title {
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 8px;
}

.panel-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.class-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 4px;
  max-height: 240px;
  overflow: auto;
}

.map-wrap {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  overflow: hidden;
  position: relative;
  min-height: 520px;
}
</style>
