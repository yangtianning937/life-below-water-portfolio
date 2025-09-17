<template>
  <!-- 支持键盘 ←/→ 翻页 -->
  <section class="m1" @keyup.left.prevent="prevPage" @keyup.right.prevent="nextPage" tabindex="0">
    <!-- Page 1 -->
    <div v-show="page===1" class="m1__page">
      <h2 class="m1__h2">What is an Ecosystem?</h2>
      <ul class="m1__bullets">
        <li>The ocean is like a big neighborhood where animals, plants, and tiny creatures all live together.</li>
        <li>They depend on each other to survive.</li>
        <li><b>Example:</b> seagrass provides food and shelter for fish.</li>
        <li><b>Fun fact:</b> The ocean makes more than half of the oxygen we breathe!</li>
      </ul>

      <!-- 装饰图（可按需替换资源或删除） -->
      <div class="m1__art m1__art--fish"></div>

      <div class="m1__pager">
        <button class="arrow arrow--left" :disabled="page===1" @click="prevPage"><span>Previous</span></button>
        <button class="arrow arrow--right" @click="nextPage"><span>Next Page</span></button>
      </div>
    </div>

    <!-- Page 2 -->
    <div v-show="page===2" class="m1__page">
      <!-- 标题行 + 右侧按钮（你要的“右后方”） -->
      <div class="m1__bar">
        <h2 class="m1__h2">Nutrients in the Ocean</h2>


        <RouterLink class="m1__cta" to="/epic1">Explore Water Quality</RouterLink>
      </div>

      <ul class="m1__bullets">
        <li>Nutrients are like vitamins for the sea.</li>
        <li>They help plants grow and fish to survive.</li>
      </ul>

      <p class="m1__lead">Some interesting water nutrients are:</p>

      <!-- 胶囊卡片 1 -->
      <div class="pill">
        <div class="pill__title">TSS (Total Suspended Solids)</div>
        <div class="pill__text">
          This is the measure of how much the water is clouded. Too much material floating in the water
          (like dirt or algae) prevents sunlight from passing through, and aquatic plants can't grow well.
        </div>
      </div>

      <!-- 胶囊卡片 2 -->
      <div class="pill">
        <div class="pill__title">Total Nitrogen</div>
        <div class="pill__text">
          Nitrogen encourages plant growth — but too much can cause algae to grow too fast. That turns the water
          green and slimy, and it kills fish and other life.
        </div>
      </div>

      <!-- 胶囊卡片 3 -->
      <div class="pill">
        <div class="pill__title">Total Phosphorus</div>
        <div class="pill__text">
          This is all of the phosphorus in the water. Scientists analyze this to see if the bay is getting too much pollution
          from farms or cities or not.
        </div>
      </div>

      <div class="m1__pager">
        <button class="arrow arrow--left" @click="prevPage"><span>Previous</span></button>
        <button class="arrow arrow--right" @click="nextPage"><span>Next Page</span></button>
      </div>
    </div>

    <!-- Page 3 -->
    <div v-show="page===3" class="m1__page">
      <h2 class="m1__h2">Marine Food Chains</h2>
      <p class="m1__lead">Marine food chains show “who eats who” in the sea.</p>
      <p class="m1__chain">
        Plankton <span class="m1__arrow">→</span> Small Fish <span class="m1__arrow">→</span> Bigger Fish <span class="m1__arrow">→</span> Shark
      </p>
      <ul class="m1__bullets">
        <li>If one part is missing, the whole chain is affected. That is why we need good water quality for them to survive.</li>
        <li>Fun fact: Sharks are "keystone species" that maintain ocean health by controlling populations of other marine animals.</li>
      </ul>

      <div class="m1__pager">
        <button class="arrow arrow--left" @click="prevPage"><span>Previous</span></button>
        <button class="arrow arrow--right" :disabled="page===total" @click="nextPage"><span>Complete Module</span></button>
      </div>
    </div>

    <!-- 底部页码点 -->
    <div class="m1__dots" role="tablist" aria-label="Module 1 pages">
      <button v-for="n in total" :key="n" class="dot" :class="{active: page===n}" @click="go(n)"
              :aria-selected="page===n" :aria-label="'Go to page '+n"></button>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const total = 3
const page = ref(1)

function nextPage(){ if(page.value < total) page.value++ }
function prevPage(){ if(page.value > 1) page.value-- }
function go(n){ page.value = Math.min(Math.max(1, n), total) }
</script>

<style scoped>
/* 容器：透明，继承父页淡蓝背景与颜色变量 */
.m1{
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

/* 标题与右侧按钮在同一行 */
.m1__bar{
  display:flex;
  align-items:flex-end;          /* 让按钮与标题基线更贴近 */
  justify-content:space-between; /* 标题靠左，按钮靠右 */
  gap:12px;
  margin-bottom:6px;
}

.m1__h2{ margin:0 0 12px; font-weight:800; font-size:1.8rem; line-height:1.25; color: var(--lm-heading); }
.m1__lead{ margin:10px 0 12px; font-size:1.1rem; font-weight:700; color: var(--lm-text); }
.m1__bullets{ margin:0 0 12px; padding-left:22px; line-height:1.7; font-size:1.05rem; color: var(--lm-text); }
.m1__chain{ font-size:1.3rem; font-weight:800; margin:8px 0 10px; color: var(--lm-heading); }
.m1__arrow{ display:inline-block; padding:0 6px; font-size:1.35rem; color:#0a5d7d; }

/* 右侧跳转按钮（与右下“Next Page”同色系） */
.m1__cta{
  display:inline-block;
  padding:10px 16px;
  border-radius:999px;
  font-weight:800;
  background:#0ea5b5;
  color:#fff;
  border:1px solid #0b7285;
  box-shadow:0 6px 14px rgba(14,165,181,.25);
  transition:transform .08s ease, box-shadow .08s ease;
  white-space:nowrap;
  text-decoration:none;
}
.m1__cta:hover{ transform:translateY(-1px); }

@media (max-width: 720px){
  .m1__bar{ flex-direction:column; align-items:flex-start; gap:8px; }
}

/* 胶囊提示卡（贴近 PDF 手绘风） */
.pill{
  background:#fff; color:#0f172a;
  border: 3px solid #222;
  border-radius: 22px;
  padding: 12px 16px;
  margin: 14px 0;
  box-shadow: 10px 10px 0 #000;
}
.pill__title{ font-weight:800; text-align:center; margin-bottom:4px; color:#0f172a; }
.pill__text { text-align:center; }

/* 装饰图（按需替换资源路径） */
.m1__art{ position:absolute; background-repeat:no-repeat; background-size:contain; background-position:center; opacity:.9; pointer-events:none; }
.m1__art--fish{ width:260px; height:120px; right:8%; bottom:108px; background-image:url('@/assets/images/fish-line.png'); }

/* 翻页箭头 */
.m1__pager{ position:absolute; left:0; right:0; bottom:18px; display:flex; justify-content:space-between; align-items:center; padding:0 16px; }
.arrow{ position:relative; border:none; cursor:pointer; font-weight:800; padding:14px 22px; color:#0b1220; background:#e8b6ae; }
.arrow:disabled{ opacity:.5; cursor:not-allowed; }
.arrow span{ position:relative; z-index:1; }
.arrow--left{ padding-left:46px; }
.arrow--left::before{ content:''; position:absolute; left:-28px; top:0; width:0; height:0; border-top:28px solid transparent; border-bottom:28px solid transparent; border-right:28px solid #e8b6ae; }
.arrow--right{ background:#0ea5b5; color:#fff; padding-right:46px; }
.arrow--right::after{ content:''; position:absolute; right:-28px; top:0; width:0; height:0; border-top:28px solid transparent; border-bottom:28px solid transparent; border-left:28px solid #0ea5b5; }

/* 页码点 */
.m1__dots{ position:absolute; left:50%; transform:translateX(-50%); bottom:10px; display:flex; gap:8px; }
.dot{ width:10px; height:10px; border-radius:999px; background:#94a3b8; border:0; cursor:pointer; }
.dot.active{ background:#0ea5b5; }

/* 固定浅色方案 */
@media (prefers-color-scheme: dark){
  .m1{ background: transparent; color: var(--lm-text); }
  .m1__h2{ color: var(--lm-heading); }
  .pill{ border-color:#222; box-shadow:10px 10px 0 #000; }
}
</style>
