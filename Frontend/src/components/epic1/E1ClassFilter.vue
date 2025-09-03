<template>
  <div class="panel">
    <div class="panel-title">Classes</div>
    <div class="btn-row">
      <button class="btn" @click="$emit('update:selected', [...options])">Select all</button>
      <button class="btn" @click="$emit('update:selected', [])">Clear</button>
    </div>
    <div class="class-list">
      <label v-for="k in options" :key="k" class="checkbox">
        <input
          type="checkbox"
          :checked="modelSet.has(k)"
          @change="toggle(k, $event.target.checked)"
        />
        <span class="color-dot" :style="{ background: colorForClass(k) }"></span>
        <span>{{ k }}</span>
      </label>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  options: { type: Array, required: true },       // 全部 class
  selected: { type: Array, required: true },      // 已选（v-model）
  colorForClass: { type: Function, required: true }
});
const emit = defineEmits(["update:selected"]);

const modelSet = computed(() => new Set(props.selected.map(String)));

function toggle(k, checked) {
  const next = new Set(modelSet.value);
  if (checked) next.add(k); else next.delete(k);
  emit("update:selected", Array.from(next));
}
</script>
