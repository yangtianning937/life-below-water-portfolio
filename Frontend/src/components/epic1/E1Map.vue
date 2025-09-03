<template>
  <div id="map"></div>
</template>

<script setup>
import { onMounted, onUnmounted, ref, watch } from "vue";
import L from "leaflet";
import "leaflet.heat";

const props = defineProps({
  rows: { type: Array, required: true },
  cols: { type: Object, required: true },
  showHeat: { type: Boolean, required: true },
  showMarkers: { type: Boolean, required: true },
  colorForClass: { type: Function, required: true },
});

const mapDiv = ref(null);
let map, heatLayer, markersLayer;

function initMap() {
  if (map) return;
  map = L.map("map", { zoomControl: true, preferCanvas: true }).setView([-37.81, 144.96], 10);
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
  if (!props.rows.length) return;

  const norm = makeNormalizer(props.rows.map(r => r[props.cols.wqi]));
  if (props.showHeat) {
    const heat = props.rows
      .filter(r => isFinite(r[props.cols.lat]) && isFinite(r[props.cols.lon]))
      .map(r => [r[props.cols.lat], r[props.cols.lon], norm(r[props.cols.wqi])]);
    heatLayer.setLatLngs(heat);
  }
  if (props.showMarkers) {
    props.rows.forEach(r => {
      const lat = r[props.cols.lat], lon = r[props.cols.lon];
      if (!isFinite(lat) || !isFinite(lon)) return;
      const m = L.circleMarker([lat, lon], { radius: 5, weight: 1, color: props.colorForClass(r[props.cols.klass]), fillOpacity: 0.75 });
      const popup = `
        <div style="font-size:12px;line-height:1.2">
          <div><b>${String(r[props.cols.name] ?? "-")}</b></div>
          <div>${String(r[props.cols.body] ?? "-")}</div>
          <div>WQI: ${String(r[props.cols.wqi] ?? "-")}</div>
          <div>${String(r[props.cols.date] ?? "-")}</div>
        </div>`;
      m.bindPopup(popup);
      markersLayer.addLayer(m);
    });
  }
}

onMounted(() => { initMap(); renderLayers(); });
onUnmounted(() => { if (map) { map.remove(); map = null; } });

watch(() => [props.rows, props.showHeat, props.showMarkers], renderLayers, { deep: true });
</script>
