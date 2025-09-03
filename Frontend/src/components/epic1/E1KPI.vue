<template>
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
</template>

<script setup>
defineProps({ kpis: { type: Object, required: true } });
</script>
