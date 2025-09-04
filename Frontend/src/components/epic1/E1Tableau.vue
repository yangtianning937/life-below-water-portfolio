<!-- src/components/epic1/E1Tableau.vue
     使用全局插件 OceanDecals.vue（teleport 到 body），本组件只负责“海洋边框 + Tableau iframe”。
     通过 props 开关与配置贴图密度/透明度/层级。 -->
<template>
  <!-- 全局海洋贴图（可关闭），会被 Teleport 到 <body>，对所有页面可见 -->
  <OceanDecals
    v-if="showDecals"
    :density="decalsDensity"
    :opacity="decalsOpacity"
    :zIndex="decalsZIndex"
  />

  <!-- 本组件的海洋边框与地图 -->
  <div
    class="ocean-frame"
    :style="{ maxWidth: toPx(maxWidth), '--frame-image': oceanFrameDataUrl }"
  >
    <div class="ocean-frame__inner">
      <iframe
        class="tableau-iframe"
        :src="embedUrl"
        title="Tableau Map"
        frameborder="0"
        allowfullscreen
        :style="{ height: toPx(height) }"
      ></iframe>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import OceanDecals from '@/components/decorations/OceanDecals.vue'

const props = defineProps({
  /* Tableau 可视化地址（支持 :url 或 :src） */
  url: { type: String, default: '' },
  src: { type: String, default: '' },

  /* 尺寸控制 */
  height:   { type: [Number, String], default: 520 },
  maxWidth: { type: [Number, String], default: 'min(1280px, 96vw)' },

  /* 全局贴图开关与参数（传给 OceanDecals） */
  showDecals:     { type: Boolean, default: true },
  decalsDensity:  { type: String,  default: 'high' },   // 'low' | 'medium' | 'high'
  decalsOpacity:  { type: Number,  default: 0.9 },      // 0~1
  decalsZIndex:   { type: [Number, String], default: 5 }
})

const toPx = v => (typeof v === 'number' ? `${v}px` : v)

const baseUrl = computed(() => (props.url || props.src || '').trim())
const embedUrl = computed(() => {
  const u = baseUrl.value
  if (!u) return ''
  try {
    const url = new URL(u)
    if (!url.searchParams.has(':showVizHome')) url.searchParams.set(':showVizHome', 'no')
    if (!url.searchParams.has(':embed'))       url.searchParams.set(':embed', 'y')
    if (!url.searchParams.has(':toolbar'))     url.searchParams.set(':toolbar', 'yes')
    return url.toString()
  } catch {
    return u.includes(':showVizHome') ? u : `${u}${u.includes('?') ? '&' : '?'}:showVizHome=no&:embed=y&:toolbar=yes`
  }
})

/* 海洋边框（内联 SVG） */
const oceanFrameDataUrl = `url("data:image/svg+xml;utf8,${encodeURIComponent(`
  <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' preserveAspectRatio='none'>
    <rect x='0' y='0' width='100' height='100' fill='#006994'/>
    <defs>
      <pattern id='w' patternUnits='userSpaceOnUse' width='20' height='20'>
        <path d='M0 15 Q5 10 10 15 T20 15 V20 H0Z' fill='#29b6f6' opacity='0.35'/>
      </pattern>
    </defs>
    <rect x='0' y='0' width='100' height='100' fill='url(#w)' opacity='0.5'/>
    <g fill='#ffd54f' opacity='0.9'>
      <path d='M10 50 l5 4 -5 4 -5 -4z'/>
      <path d='M90 50 l5 4 -5 4 -5 -4z'/>
      <path d='M50 10 l5 4 -5 4 -5 -4z'/>
      <path d='M50 90 l5 4 -5 4 -5 -4z'/>
    </g>
    <g fill='#ffffff' opacity='0.65'>
      <circle cx='14' cy='14' r='2'/>
      <circle cx='86' cy='86' r='2'/>
      <circle cx='16' cy='84' r='1.6'/>
      <circle cx='84' cy='16' r='1.6'/>
    </g>
  </svg>
`)}")`
</script>

<style scoped>
.ocean-frame {
  margin: 0 auto;
  padding: 12px;
  border-width: 18px;
  border-style: solid;
  border-radius: 18px;
  border-image-source: var(--frame-image);
  border-image-slice: 32 fill;
  border-image-width: 18;
  border-image-repeat: round;
  background: rgba(0, 105, 148, 0.08);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}
.ocean-frame__inner {
  border-radius: 12px;
  overflow: hidden;
  background: #fff;
}
.tableau-iframe {
  display: block;
  width: 100%;
  min-height: 360px;
  border: 0;
}
</style>
