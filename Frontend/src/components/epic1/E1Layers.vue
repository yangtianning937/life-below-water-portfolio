<template>
  <div class="panel">
    <div class="panel-title">Layers</div>
    <label class="checkbox">
      <input type="checkbox" :checked="showHeat" @change="$emit('update:show-heat', $event.target.checked)" />
      Heatmap (WQI)
    </label>
    <label class="checkbox">
      <input type="checkbox" :checked="showMarkers" @change="$emit('update:show-markers', $event.target.checked)" />
      Stations
    </label>
  </div>
</template>

<script setup>
defineProps({
  showHeat: { type: Boolean, required: true },
  showMarkers: { type: Boolean, required: true }
});
defineEmits(["update:show-heat", "update:show-markers"]);
</script>
