<template>
  <section class="m2" @keyup.left.prevent="prevPage" @keyup.right.prevent="nextPage" tabindex="0">
    <!-- Page 1: Port Phillip Bay -->
    <div v-show="page===1" class="m2__page">
      <h2 class="m2__h2">Port Phillip Bay</h2>
      <p class="m2__p">
        Port Phillip is one of the largest enclosed saltwater spaces in the Southern Hemisphere and one of
        the most biodiverse waters on our planet.
      </p>


      <figure class="be-hero be-hero--under">
        <div class="be-hero__box">
          <img
            class="be-hero__img"
            :src="BASE_URL + '/learning/beaches/hero_bay_aerial.jpg'"
            alt="Port Phillip Bay aerial view from space"
          />
        </div>
      </figure>


      <div class="m2__pager">
        <button class="arrow arrow--left" :disabled="page===1" @click="prevPage"><span>Previous</span></button>
        <button class="arrow arrow--right" @click="nextPage"><span>Next Page</span></button>
      </div>
    </div>

    <!-- Page 2: Famous Beaches（四张卡片） -->
    <div v-show="page===2" class="m2__page">
      <h2 class="m2__h2">Famous Beaches</h2>

      <section class="be-grid" aria-label="Famous beaches around Port Phillip Bay">
        <figure v-for="b in beaches" :key="b.key" class="be-card">
          <img :src="b.img" :alt="b.alt" loading="lazy" />
          <figcaption><b>{{ b.title }}</b> — {{ b.desc }}</figcaption>
        </figure>
      </section>

      <div class="m2__pager">
        <button class="arrow arrow--left" @click="prevPage"><span>Previous</span></button>
        <button class="arrow arrow--right" @click="nextPage"><span>Next Page</span></button>
      </div>
    </div>

    <!-- Page 3: Beach Safety（图标+文案） -->
    <div v-show="page===3" class="m2__page">
      <h2 class="m2__h2">Beach Safety</h2>

      <ul class="be-icons">
        <li v-for="s in safety" :key="s.key" class="be-icon">
          <img :src="s.icon" alt="" role="presentation" />
          <span>{{ s.text }}</span>
        </li>
      </ul>

      <div class="m2__pager">
        <button class="arrow arrow--left" @click="prevPage"><span>Previous</span></button>
      </div>
    </div>

    <!-- 小圆点 -->
    <div class="m2__dots" role="tablist" aria-label="Module 2 pages">
      <button
        v-for="n in total"
        :key="n"
        class="dot"
        :class="{active: page===n}"
        @click="go(n)"
        :aria-selected="page===n"
        :aria-label="'Go to page '+n"
      ></button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const BASE_URL = import.meta.env.BASE_URL

const total = 3
const page = ref(1)

function nextPage(){ if(page.value < total) page.value++ }
function prevPage(){ if(page.value > 1) page.value-- }
function go(n:number){ page.value = n }

/* 图片数据 */
const beaches = [
  {
    key: 'st_kilda',
    title: 'St Kilda Beach',
    desc: 'Penguins live here!',
    img: `${BASE_URL}/learning/beaches/st_kilda_penguin.jpg`,
    alt: 'Penguins at St Kilda pier',
  },
  {
    key: 'brighton',
    title: 'Brighton Beach',
    desc: 'Colorful bathing boxes.',
    img: `${BASE_URL}/learning/beaches/brighton_bathing_boxes.jpg`,
    alt: 'Brighton colorful bathing boxes on the beach',
  },
  {
    key: 'dromana',
    title: 'Dromana Beach',
    desc: 'Famous for paddle boarding.',
    img: `${BASE_URL}/learning/beaches/dromana_paddleboarding.jpg`,
    alt: 'People paddle boarding at Dromana',
  },
  {
    key: 'sorrento',
    title: 'Sorrento Beach',
    desc: 'Great for exploring rock pools.',
    img: `${BASE_URL}/learning/beaches/sorrento_rockpools.jpg`,
    alt: 'Rock pools at Sorrento beach',
  },
]

const safety = [
  { key: 'flags',  icon: `${BASE_URL}/learning/ui/beach_flags.svg`,    text: 'Swim between the red and yellow flags.' },
  { key: 'sun',    icon: `${BASE_URL}/learning/ui/sunscreen_hat.svg`,  text: 'Wear sunscreen and a hat.' },
  { key: 'rip',    icon: `${BASE_URL}/learning/ui/rip_current.svg`,    text: 'Watch out for strong currents.' },
  { key: 'buddy',  icon: `${BASE_URL}/learning/ui/buddy_swim.svg`,     text: 'Never swim alone.' },
]
</script>

<style scoped>
/* 容器卡片 */
.m2{
  background: transparent;
  border: 1px solid #1f2937;
  border-radius: 16px;

  padding: 24px 20px 24px;
  position: relative;
  min-height: 560px;
  box-shadow: 0 10px 28px rgba(15,23,42,.08);
  color: var(--lm-text);
  outline: none;
}


.m2__page{
  position: relative;
  padding-bottom: 120px;
  min-height: 480px;
}

.m2__h2{ margin:0 0 12px; font-weight:800; font-size:1.6rem; line-height:1.25; color: var(--lm-heading); }
.m2__p{ margin:8px 0 10px; line-height:1.7; font-size:1.05rem; }


/* Page 1 图片容器 */
.be-hero{ margin-top: 8px; }
.be-hero__box{
  background:#fff;
  border:1px solid #e5e7eb;
  border-radius:16px;
  padding:8px;
  box-shadow:0 10px 22px rgba(2,6,23,.06);
  display:flex;
  align-items:center;
  justify-content:center;
  --hero-max-h: 360px;

}


.be-hero__img{
  display:block;
  max-width:100%;
  height:auto;
  max-height: var(--hero-max-h);
  object-fit: contain;
  border-radius:12px;
}


/* Page 2 海滩卡片网格 */
.be-grid{
  display:grid; gap:12px;
  grid-template-columns: repeat(2, minmax(0,1fr));
  margin: 6px 0 16px;
}
@media (min-width: 920px){ .be-grid{ grid-template-columns: repeat(4, minmax(0,1fr)); } }

.be-card{
  background:#fff; border:1px solid #e5e7eb; border-radius:14px; overflow:hidden;
  box-shadow:0 10px 22px rgba(2,6,23,.06);
}
.be-card img{ width:100%; aspect-ratio:4/3; object-fit:cover; display:block; }
.be-card figcaption{ padding:10px 12px; line-height:1.5; }

/* Page 3 安全提示（图标 + 文本） */
.be-icons{ display:grid; gap:10px; grid-template-columns: 1fr; margin-top: 6px; }
@media (min-width: 720px){ .be-icons{ grid-template-columns: 1fr 1fr; } }
.be-icon{
  display:flex; align-items:center; gap:10px;
  background:#0b122005; border:1px solid #e5e7eb; border-radius:12px; padding:10px 12px;
}
.be-icon img{ width:36px; height:36px; object-fit:contain; }

/* 翻页按钮： */
.m2__pager{
  position:absolute; left:0; right:0; bottom:46px;
  display:flex; justify-content:space-between; align-items:center; padding:0 16px;
}
.arrow{ position:relative; border:none; cursor:pointer; font-weight:800; padding:14px 22px; color:#0b1220; background:#e8b6ae; }
.arrow:disabled{ opacity:.5; cursor:not-allowed; }
.arrow span{ position:relative; z-index:1; }
.arrow--left{ padding-left:46px; }
.arrow--left::before{
  content:''; position:absolute; left:-28px; top:0; width:0; height:0;
  border-top:28px solid transparent; border-bottom:28px solid transparent; border-right:28px solid #e8b6ae;
}
.arrow--right{ background:#0ea5b5; color:#fff; padding-right:46px; }
.arrow--right::after{
  content:''; position:absolute; right:-28px; top:0; width:0; height:0;
  border-top:28px solid transparent; border-bottom:28px solid transparent; border-left:28px solid #0ea5b5;
}

/* 页码点：永远在最底下中间 */
.m2__dots{ position:absolute; left:50%; transform:translateX(-50%); bottom:10px; display:flex; gap:8px; }
.dot{ width:10px; height:10px; border-radius:999px; background:#94a3b8; border:0; cursor:pointer; }
.dot.active{ background:#0ea5b5; }

/* 响应式 */
@media (max-width: 720px){
  .m2{ min-height: 600px; }
}

/* 固定浅色方案（禁用深色背景） */
@media (prefers-color-scheme: dark){
  .m2{ background: transparent; color: var(--lm-text); }
  .m2__h2{ color: var(--lm-heading); }
}
</style>
