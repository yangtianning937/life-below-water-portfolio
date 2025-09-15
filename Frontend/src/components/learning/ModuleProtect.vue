<template>
  <!-- 支持键盘 ←/→ 切换 -->
  <section class="m3" @keyup.left.prevent="prevPage" @keyup.right.prevent="nextPage" tabindex="0">
    <!-- Page 1: Why Protect Our Bay? -->
    <div v-show="page===1" class="m3__page">
      <h2 class="m3__h2">Why Protect Our Bay?</h2>
      <p class="m3__p">
        Many animals live here—dolphins, fish, seals, seabirds. People come to swim, sail, and play. The bay matters to animals and to us!
      </p>

      <div class="m3__pager">
        <button class="arrow arrow--left" :disabled="page===1" @click="prevPage"><span>Previous</span></button>
        <button class="arrow arrow--right" @click="nextPage"><span>Next Page</span></button>
      </div>
    </div>

    <!-- Page 2: The Bay Needs Our Help -->
    <div v-show="page===2" class="m3__page">
      <h2 class="m3__h2">The Bay Needs Our Help</h2>
      <ul class="needs">
        <li>Rubbish like plastic bags and bottles can hurt animals if eaten or cause entanglement.</li>
        <li>Chemicals from cars or gardens wash into the bay when it rains.</li>
        <li>If we don’t take care, the bay could become dirty and unsafe for animals and people.</li>
      </ul>

      <div class="m3__pager">
        <button class="arrow arrow--left" @click="prevPage"><span>Previous</span></button>
        <button class="arrow arrow--right" @click="nextPage"><span>Next Page</span></button>
      </div>
    </div>

    <!-- Page 3: How We Can Protect the Bay -->
    <div v-show="page===3" class="m3__page">
      <h2 class="m3__h2">How We Can Protect the Bay</h2>
      <ul class="actions">
        <li>Always put rubbish in the bin.</li>
        <li>Use reusable bottles, bags, and containers.</li>
        <li>Don’t pick up sea creatures or break shells.</li>
        <li>Join beach clean-ups and share knowledge with friends.</li>
      </ul>

      <div class="m3__pager">
        <button class="arrow arrow--left" @click="prevPage"><span>Previous</span></button>
        <button class="arrow arrow--right" :disabled="page===total" @click="nextPage">
          <span>Complete Module</span>
        </button>
      </div>
    </div>

    <!-- 小圆点 -->
    <div class="m3__dots" role="tablist" aria-label="Module 3 pages">
      <button v-for="n in total" :key="n" class="dot" :class="{active: page===n}" @click="go(n)" :aria-selected="page===n" :aria-label="'Go to page '+n"></button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const total = 3
const page = ref(1)
function nextPage(){ if(page.value < total) page.value++ }
function prevPage(){ if(page.value > 1) page.value-- }
function go(n:number){ page.value = n }
</script>

<style scoped>
.m3{
  background: transparent;
  border: 1px solid #1f2937;
  border-radius: 16px;
  padding: 24px 20px 56px;
  position: relative;
  min-height: 520px;
  box-shadow: 0 10px 28px rgba(15,23,42,.08);
  color: var(--lm-text);
  outline: none;
}

.m3__h2{ margin:0 0 12px; font-weight:800; font-size:1.6rem; line-height:1.25; color: var(--lm-heading); }
.m3__p{ margin:0; line-height:1.7; font-size:1.05rem; }

/* Page 2 列表：左侧色条强调“警示” */
.needs{ margin:8px 0 0; padding-left: 22px; line-height:1.8; }
.needs li{ margin: 6px 0; }

/* Page 3 列表：做成“对勾”感觉（文本样式即可） */
.actions{ margin:8px 0 0; padding-left:22px; line-height:1.8; }
.actions li{ margin:6px 0; }

/* 翻页箭头（复用） */
.m3__pager{ position:absolute; left:0; right:0; bottom:18px; display:flex; justify-content:space-between; align-items:center; padding:0 16px; }
.arrow{ position:relative; border:none; cursor:pointer; font-weight:800; padding:14px 22px; color:#0b1220; background:#e8b6ae; }
.arrow:disabled{ opacity:.5; cursor:not-allowed; }
.arrow span{ position:relative; z-index:1; }
.arrow--left{ padding-left:46px; }
.arrow--left::before{ content:''; position:absolute; left:-28px; top:0; width:0; height:0; border-top:28px solid transparent; border-bottom:28px solid transparent; border-right:28px solid #e8b6ae; }
.arrow--right{ background:#0ea5b5; color:#fff; padding-right:46px; }
.arrow--right::after{ content:''; position:absolute; right:-28px; top:0; width:0; height:0; border-top:28px solid transparent; border-bottom:28px solid transparent; border-left:28px solid #0ea5b5; }

/* 页码点 */
.m3__dots{ position:absolute; left:50%; transform:translateX(-50%); bottom:10px; display:flex; gap:8px; }
.dot{ width:10px; height:10px; border-radius:999px; background:#94a3b8; border:0; cursor:pointer; }
.dot.active{ background:#0ea5b5; }

/* 响应式 */
@media (max-width: 720px){ .m3{ padding-bottom:84px; } }

/* 固定浅色方案 */
@media (prefers-color-scheme: dark){
  .m3{ background: transparent; color: var(--lm-text); }
  .m3__h2{ color: var(--lm-heading); }
}
</style>
