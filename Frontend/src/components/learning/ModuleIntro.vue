<template>
  <section
    class="card m1"
    tabindex="0"
    @keyup.left.prevent="prevPage"
    @keyup.right.prevent="tryNextByKey"
  >
    <!-- ===== Page 1：左文右图 ===== -->
    <div v-show="page===1" class="m1__page m1__page--intro">
      <h2 class="m1__title">What is an Ecosystem?</h2>

      <div class="m1__grid">
        <div class="m1__text">
          <p>The ocean is like a big neighborhood where animals, plants, and tiny creatures all live together.</p>
          <p>They depend on each other to survive.</p>
          <p><b>Example:</b> seagrass provides food and shelter for fish.</p>
          <p><b>Fun fact:</b> The ocean makes more than half of the oxygen we breathe!</p>
        </div>

        <aside class="m1__media" aria-label="Seagrass and reef photos">
          <img class="media__img" :src="BASE_URL + '/learning/intro/seagrass.png'" alt="Seagrass under sunlight" />
        </aside>
      </div>

      <div class="m1__pager">
        <button class="arrow arrow--left" disabled><span>Previous</span></button>
        <Dots :total="3" :page="page" />
        <button class="arrow arrow--right" @click="nextPage"><span>Next Page</span></button>
      </div>
    </div>

    <!-- ===== Page 2：营养素 ===== -->
    <div v-show="page===2" class="m1__page">
      <div class="m1__bar">
        <h2 class="m1__title">Nutrients in the Ocean</h2>
        <!-- 右侧 CTA：跳到水质页 -->
        <router-link
          class="m1__cta"
          :to="{ name:'data_hub' }"
          aria-label="Go to Water Quality"
        >
          Explore Water Quality
        </router-link>
      </div>

      <p class="m1__lead">Nutrients are like vitamins for the sea. They help plants grow and fish to survive.</p>

      <div class="pill">
        <div class="pill__title">TSS (Total Suspended Solids)</div>
        <div class="pill__text">
          This is the measure of how much the water is clouded. Too much material floating in the water
          (like dirt or algae) prevents sunlight from passing through, and aquatic plants can't grow well.
        </div>
      </div>

      <div class="pill">
        <div class="pill__title">Total Nitrogen</div>
        <div class="pill__text">
          Nitrogen encourages plant growth — but too much can cause algae to grow too fast.
          That turns the water green and slimy, and it kills fish and other life.
        </div>
      </div>

      <div class="pill">
        <div class="pill__title">Total Phosphorus</div>
        <div class="pill__text">
          This is all of the phosphorus in the water. Scientists analyze this to see if the bay is getting
          too much pollution from farms or cities or not.
        </div>
      </div>

      <div class="m1__pager">
        <button class="arrow arrow--left" @click="prevPage"><span>Previous</span></button>
        <Dots :total="3" :page="page" />
        <button class="arrow arrow--right" @click="nextPage"><span>Next Page</span></button>
      </div>
    </div>

    <!-- ===== Page 3：食物链 ===== -->
    <div v-show="page===3" class="m1__page">
      <h2 class="m1__title">Marine Food Chains</h2>
      <ul class="m1__bullets">
        <li>Marine food chains show “who eats who” in the sea.</li>
        <li>If one part is missing, the whole chain is affected. That is why we need a good water quality for them to survive.</li>
        <li>Fun fact: Sharks are "keystone species" that maintain ocean health.</li>
      </ul>

      <div class="foodchain">
        <div class="fc__item">
          <img :src="BASE_URL + '/learning/intro/plankton.png'" alt="Plankton" />
          <div class="fc__label">Plankton</div>
        </div>
        <img class="fc__arrow" :src="BASE_URL + '/learning/ui/arrow_right.svg'" alt="" />
        <div class="fc__item">
          <img :src="BASE_URL + '/learning/intro/small_fish.png'" alt="Small Fish" />
          <div class="fc__label">Small Fish</div>
        </div>
        <img class="fc__arrow" :src="BASE_URL + '/learning/ui/arrow_right.svg'" alt="" />
        <div class="fc__item">
          <img :src="BASE_URL + '/learning/intro/big_fish.png'" alt="Bigger Fish" />
          <div class="fc__label">Bigger Fish</div>
        </div>
        <img class="fc__arrow" :src="BASE_URL + '/learning/ui/arrow_right.svg'" alt="" />
        <div class="fc__item">
          <img :src="BASE_URL + '/learning/intro/shark.png'" alt="Shark" />
          <div class="fc__label">Shark</div>
        </div>
      </div>



      <div class="m1__pager">
        <button class="arrow arrow--left" @click="prevPage"><span>Previous</span></button>
        <Dots :total="3" :page="page" />
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const BASE_URL = import.meta.env.BASE_URL

const emit = defineEmits(['complete'])

const page = ref(1)
function nextPage(){ if(page.value < 3) page.value++ }
function prevPage(){ if(page.value > 1) page.value-- }
function tryNextByKey(){ if (page.value < 3) nextPage() }

/* 小圆点（内联子组件） */
const Dots = {
  name: 'Dots',
  props: { total: {type:Number, required:true}, page: {type:Number, required:true} },
  template: `
    <div class="dots" role="tablist" aria-label="Pages">
      <button v-for="n in total" :key="n" class="dot" :class="{active: page===n}" disabled></button>
    </div>
  `
}
</script>

<style scoped>
/* 基础卡片 */
.card{
  background: transparent;
  color: var(--lm-text);
  border: 1px solid #1f2937;
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 10px 28px rgba(15,23,42,.08);
}
.m1__page{ position: relative; min-height: 100%; width: 100%; }
.m1__title{ margin:0 0 10px; font-size:1.6rem; font-weight:900; color: var(--lm-heading); }
.m1__lead{ margin: 0 0 10px; }
.m1__bullets{ margin: 6px 0 16px; padding-left: 22px; line-height: 1.7; }

/* Page 1：左文右图布局 */
.m1__page--intro { display: block; }
.m1__grid{
  display: grid;
  grid-template-columns: 1.25fr .9fr; /* 左宽右窄，视觉更舒服 */
  gap: 24px;
  align-items: start;
  margin-top: 6px;
}
.m1__text p{ margin: 0 0 10px; line-height: 1.7; }
.m1__media{
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 14px;
}
.media__img{
  width: min(340px, 100%);
  aspect-ratio: 4 / 3;
  object-fit: cover;
  border-radius: 14px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 10px 24px rgba(2,6,23,.12);
}

/* Page 2 顶部条+CTA */
.m1__bar{ display:flex; align-items:flex-end; justify-content:space-between; gap:10px; }
.m1__cta{
  display:inline-block; padding:10px 16px; border-radius:999px; font-weight:800;
  background:#0ea5b5; color:#fff; border:1px solid #0b7285;
  box-shadow:0 6px 14px rgba(14,165,181,.25); white-space:nowrap; text-decoration:none;
  transition: transform .08s ease, box-shadow .08s ease;
}
.m1__cta:hover{ transform: translateY(-1px); }

/* pill 文本块（PDF 的卡片风格） */
.pill{
  background:#fff; border:1px solid #111; border-radius:16px;
  padding:14px; margin:10px 0 14px; box-shadow: 6px 8px 0 #111;
}
.pill__title{ font-weight:900; margin-bottom:6px; }

/* Page 3 食物链 */
.foodchain{
  display:grid; grid-template-columns: repeat(7, minmax(0,1fr));
  gap: 10px; align-items:center; margin-top: 8px;
}
.fc__item{ text-align:center; }
.fc__item img{ width: 100%; max-width: 180px; aspect-ratio: 4/3; object-fit: contain; }
.fc__label{ font-weight:800; margin-top: 6px; }
.fc__arrow{ width: 26px; justify-self:center; opacity:.9; }

/* 装饰图（可选） */
.m1__art{ position:absolute; inset:auto 10px 12px auto; pointer-events:none; }
.m1__art--bottom{ right: 18px; bottom: 8px; }
.art--fish{ width: 240px; transform: translateY(10px); opacity:.9; }

/* 分页箭头 + 圆点 */
.m1__pager{ margin-top: 16px; display:flex; align-items:center; justify-content:space-between; position:relative; }
.arrow{ position:relative; border:none; cursor:pointer; font-weight:800; padding:12px 20px; color:#0b1220; background:#e8b6ae; }
.arrow:disabled{ opacity:.5; cursor:not-allowed; }
.arrow span{ position:relative; z-index:1; }
.arrow--left{ padding-left:46px; }
.arrow--left::before{
  content:''; position:absolute; left:-28px; top:0; width:0; height:0;
  border-top:26px solid transparent; border-bottom:26px solid transparent; border-right:28px solid #e8b6ae;
}
.arrow--right{ background:#0ea5b5; color:#fff; padding-right:46px; }
.arrow--right::after{
  content:''; position:absolute; right:-28px; top:0; width:0; height:0;
  border-top:26px solid transparent; border-bottom:26px solid transparent; border-left:28px solid #0ea5b5;
}
.dots{ position:absolute; left:50%; transform:translateX(-50%); display:flex; gap:8px; align-items:center; }
.dot{ width:10px; height:10px; border-radius:999px; background:#94a3b8; border:0; }
.dot.active{ background:#0ea5b5; }

/* 响应式：小屏上下排 */
@media (max-width: 900px){
  .m1__grid{ grid-template-columns: 1fr; }
  .m1__media{ align-items: center; }
}

/* 深色模式微调（兼容你的全局卡片样式） */
@media (prefers-color-scheme: dark){
  .card{ background: transparent; border-color:#1f2937; }
  .pill{ background:#0b1220; color:#e5e7eb; border-color:#0b1220; box-shadow: 6px 8px 0 #0b1220; }
}
</style>
