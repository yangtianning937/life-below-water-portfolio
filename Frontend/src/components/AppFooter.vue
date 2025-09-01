<!-- src/components/AppFooter.vue -->
<script setup>
const year = new Date().getFullYear()
// 可在 .env 设置覆盖：VITE_ORG_NAME / VITE_UNIT_NAME
const org = import.meta.env.VITE_ORG_NAME  || 'Team Lakers'
//const unit = import.meta.env.VITE_UNIT_NAME || 'Monash FIT5120'
</script>

<template>
  <footer class="bg-slate-50 border-t border-blue-100">
    <div class="max-w-6xl mx-auto px-4 py-6 text-sm text-slate-600
                flex flex-col md:flex-row items-center justify-between gap-3">
      <div class="flex items-center gap-2">
        <span aria-hidden="true">©</span>
        <span>{{ year }} {{ org }} — {{ unit }}. All rights reserved.</span>
      </div>
    </div>
  </footer>
</template>

<style scoped>
/* 调颜色或字号 */
</style>
