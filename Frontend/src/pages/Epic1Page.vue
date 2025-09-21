<template>
  <div class="page">
    <header class="pagebar">
      <button class="back-arrow" @click="goBack" aria-label="Go back to previous page">
        <span>Previous</span>
      </button>
      <h1 class="pagebar__title">Water Quality</h1>
      <div class="pagebar__spacer"></div>
    </header>

    <section class="map-wrap">
      <E1Tableau
        :url="tableauUrl"
        :height="630"
        :maxWidth="1600"
        decalsDensity="high"
      />
    </section>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import E1Tableau from '@/components/epic1/E1Tableau.vue'

const router = useRouter()

/**
 * 只切换到「上一个页面」：
 * - 优先用 history.state.back（Vue Router 会记录上一个地址）
 * - 否则若浏览器有历史则 router.back()
 * - 没有历史时保持当前页（不再强制跳到 learning）
 *   （如需默认去向，可在注释处改成 router.push({ name: 'home' }) 或 'data_hub'）
 */
function goBack() {
  const state = window.history.state
  if (state && state.back) {
    router.push(state.back)
    return
  }
  if (window.history.length > 1) {
    router.back()
    return
  }
}

const tableauUrl =
  'https://public.tableau.com/views/NewWorkbook_17569007097240/Sheet1?:showVizHome=no&:embed=y&:toolbar=yes&:tabs=no'
</script>

<style scoped>
.page { width: 100%; height: 100%; }

/* 顶部返回栏 */
.pagebar{
  position: sticky; top: 0;
  display: flex; align-items: center; gap: 12px;
  padding: 10px 6px 12px;
  background: transparent; /* 让父页淡蓝背景透出 */
  z-index: 5;
}
.pagebar__title{ margin:0; font-size:1.4rem; font-weight:800; }
.pagebar__spacer{ flex:1; }

/* 返回箭头按钮（与学习模块风格一致） */
.back-arrow{
  position: relative;
  border: none; cursor: pointer;
  font-weight: 800; color: #0b1220;
  background: #e8b6ae;
  padding: 12px 18px 12px 46px;  /* 给左侧箭头留空间 */
  border-radius: 6px;
  box-shadow: 0 6px 14px rgba(15,23,42,.08);
}
.back-arrow::before{
  content:''; position:absolute; left:-28px; top:0;
  width:0; height:0;
  border-top:26px solid transparent;
  border-bottom:26px solid transparent;
  border-right:28px solid #e8b6ae;
}
.back-arrow:disabled{ opacity:.5; cursor:not-allowed; }

/* Tableau 容器 */
.map-wrap{
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  overflow: hidden;
  min-height: 520px;
}
</style>
