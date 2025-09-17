<template>
  <!-- 支持键盘 ←/→ 切换 -->
  <section class="m2" @keyup.left.prevent="prevPage" @keyup.right.prevent="nextPage" tabindex="0">
    <!-- Page 1: Port Phillip Bay -->
    <div v-show="page===1" class="m2__page">
      <h2 class="m2__h2">Port Phillip Bay</h2>
      <p class="m2__p">
        Port Phillip is one of the largest enclosed saltwater spaces in the Southern Hemisphere and one of the most
        biodiverse waters on our planet.
      </p>

      <div class="m2__art m2__art--bay"></div>

      <div class="m2__pager">
        <button class="arrow arrow--left" :disabled="page===1" @click="prevPage"><span>Previous</span></button>
        <button class="arrow arrow--right" @click="nextPage"><span>Next Page</span></button>
      </div>
    </div>

    <!-- Page 2: Famous Beaches -->
    <div v-show="page===2" class="m2__page">
      <h2 class="m2__h2">Famous Beaches</h2>

      <ul class="beach-list">
        <li><b>St Kilda Beach</b>: Penguins live here!</li>
        <li><b>Brighton Beach</b>: Colorful bathing boxes.</li>
        <li><b>Dromana Beach</b>: Famous for paddle boarding.</li>
        <li><b>Sorrento Beach</b>: Great for exploring rock pools.</li>
      </ul>

      <div class="m2__pager">
        <button class="arrow arrow--left" @click="prevPage"><span>Previous</span></button>
        <button class="arrow arrow--right" @click="nextPage"><span>Next Page</span></button>
      </div>
    </div>

    <!-- Page 3: Beach Safety -->
    <div v-show="page===3" class="m2__page">
      <h2 class="m2__h2">Beach Safety</h2>

      <ul class="safety">
        <li>Wear sunscreen and a hat.</li>
        <li>Never swim alone; swim between the red and yellow flags.</li>
        <li>Watch out for sharks and strong currents.</li>
      </ul>

      <div class="m2__pager">
        <button class="arrow arrow--left" @click="prevPage"><span>Previous</span></button>

      </div>
    </div>

    <!-- 小圆点 -->
    <div class="m2__dots" role="tablist" aria-label="Module 2 pages">
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
/* 透明卡片容器，使用父页面的颜色变量 */
.m2{
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

.m2__h2{ margin:0 0 12px; font-weight:800; font-size:1.6rem; line-height:1.25; color: var(--lm-heading); }
.m2__p{ margin:0; line-height:1.7; font-size:1.05rem; }

/* Page 2 带卡片风格列表 */
.beach-list{ margin: 8px 0 0; padding-left: 22px; line-height:1.7; }
.beach-list li{ margin: 6px 0; }

/* Page 3 安全提示，左侧竖线强调 */
.safety{ margin: 8px 0 0; padding-left: 22px; line-height:1.8; }
.safety li{ margin: 6px 0; }

/* 插图占位（按需替换图片路径） */
.m2__art{ position:absolute; background-repeat:no-repeat; background-size:contain; background-position:center; opacity:.9; pointer-events:none; }
.m2__art--bay{ width:260px; height:140px; right:6%; bottom:110px; background-image:url('@/assets/bay.png'); }

/* 翻页箭头（与 Module 1 一致） */
.m2__pager{ position:absolute; left:0; right:0; bottom:18px; display:flex; justify-content:space-between; align-items:center; padding:0 16px; }
.arrow{ position:relative; border:none; cursor:pointer; font-weight:800; padding:14px 22px; color:#0b1220; background:#e8b6ae; }
.arrow:disabled{ opacity:.5; cursor:not-allowed; }
.arrow span{ position:relative; z-index:1; }
.arrow--left{ padding-left:46px; }
.arrow--left::before{ content:''; position:absolute; left:-28px; top:0; width:0; height:0; border-top:28px solid transparent; border-bottom:28px solid transparent; border-right:28px solid #e8b6ae; }
.arrow--right{ background:#0ea5b5; color:#fff; padding-right:46px; }
.arrow--right::after{ content:''; position:absolute; right:-28px; top:0; width:0; height:0; border-top:28px solid transparent; border-bottom:28px solid transparent; border-left:28px solid #0ea5b5; }

/* 页码点 */
.m2__dots{ position:absolute; left:50%; transform:translateX(-50%); bottom:10px; display:flex; gap:8px; }
.dot{ width:10px; height:10px; border-radius:999px; background:#94a3b8; border:0; cursor:pointer; }
.dot.active{ background:#0ea5b5; }

/* 响应式 */
@media (max-width: 720px){
  .m2{ padding-bottom:84px; }
  .m2__art--bay{ right:3%; bottom:92px; opacity:.7; }
}

/* 固定浅色方案（禁用深色背景） */
@media (prefers-color-scheme: dark){
  .m2{ background: transparent; color: var(--lm-text); }
  .m2__h2{ color: var(--lm-heading); }
}
</style>
