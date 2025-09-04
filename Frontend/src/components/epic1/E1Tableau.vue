<!-- src/components/epic1/E1Tableau.vue -->
<template>
  <div
    class="ocean-frame"
    :style="{ maxWidth: toPx(maxWidth), '--frame-image': oceanFrameDataUrl }"
  >
    <!-- 贴图层（更多海洋元素） -->
    <div v-if="showDecals" class="ocean-decals" aria-hidden="true">
      <template v-for="(d, i) in decals" :key="i">
        <!-- 鱼 -->
        <svg v-if="d.type==='fish'" class="decal" :class="d.anim" :style="decalStyle(d)" viewBox="0 0 60 30">
          <ellipse cx="28" cy="15" rx="16" ry="10" :fill="d.color || '#ffd54f'"/>
          <polygon points="0,15 14,6 14,24" :fill="d.tail || '#ffb300'"/>
          <circle cx="36" cy="13" r="2.2" fill="#263238"/>
          <path d="M18 10 C22 15,22 15,18 20" :stroke="d.gill || '#ff8f00'" stroke-width="2" fill="none"/>
        </svg>

        <!-- 水母 -->
        <svg v-else-if="d.type==='jelly'" class="decal" :class="d.anim" :style="decalStyle(d)" viewBox="0 0 48 60">
          <path d="M24 6c9 0 16 6 16 14v6H8v-6c0-8 7-14 16-14z" :fill="d.color || '#80deea'"/>
          <g :stroke="d.tent || '#26c6da'" stroke-width="2" fill="none" stroke-linecap="round">
            <path d="M12 32 C10 42,18 42,16 52"/>
            <path d="M20 32 C18 44,26 44,24 54"/>
            <path d="M28 32 C26 44,34 44,32 54"/>
            <path d="M36 32 C34 42,40 42,38 52"/>
          </g>
        </svg>

        <!-- 海星 -->
        <svg v-else-if="d.type==='star'" class="decal" :class="d.anim" :style="decalStyle(d)" viewBox="0 0 64 64">
          <path d="M32 4l7 18 19 2-15 12 5 18-16-10-16 10 5-18-15-12 19-2z" :fill="d.color || '#ff8a65'"/>
        </svg>

        <!-- 海草 -->
        <svg v-else-if="d.type==='weed'" class="decal" :class="d.anim" :style="decalStyle(d)" viewBox="0 0 48 80">
          <path d="M10 80 C6 60,18 58,14 40 C10 22,22 20,18 4" :stroke="d.color || '#43a047'" stroke-width="6" fill="none"/>
          <path d="M24 80 C20 62,30 60,28 44 C26 28,34 26,32 10" :stroke="d.color2 || '#66bb6a'" stroke-width="6" fill="none"/>
        </svg>

        <!-- 海龟 -->
        <svg v-else-if="d.type==='turtle'" class="decal" :class="d.anim" :style="decalStyle(d)" viewBox="0 0 70 50">
          <ellipse cx="36" cy="26" rx="18" ry="12" :fill="d.shell || '#8bc34a'"/>
          <circle cx="18" cy="26" r="6" :fill="d.head || '#7cb342'"/>
          <ellipse cx="28" cy="12" rx="6" ry="4" :fill="d.flipper || '#7cb342'"/>
          <ellipse cx="28" cy="40" rx="6" ry="4" :fill="d.flipper || '#7cb342'"/>
          <ellipse cx="52" cy="16" rx="6" ry="4" :fill="d.flipper || '#7cb342'"/>
          <ellipse cx="52" cy="36" rx="6" ry="4" :fill="d.flipper || '#7cb342'"/>
          <circle cx="20" cy="24" r="1.4" fill="#263238"/>
        </svg>

        <!-- 贝壳 -->
        <svg v-else-if="d.type==='shell'" class="decal" :class="d.anim" :style="decalStyle(d)" viewBox="0 0 60 50">
          <path d="M6 34 C8 14, 52 14, 54 34 Q30 50 6 34Z" :fill="d.color || '#ffd180'"/>
          <path d="M14 30 Q30 18 46 30" stroke="#ffb74d" stroke-width="2" fill="none"/>
          <path d="M10 32 Q30 20 50 32" stroke="#ffcc80" stroke-width="2" fill="none"/>
        </svg>

        <!-- 螃蟹 -->
        <svg v-else-if="d.type==='crab'" class="decal" :class="d.anim" :style="decalStyle(d)" viewBox="0 0 60 38">
          <ellipse cx="30" cy="22" rx="16" ry="10" :fill="d.color || '#ef5350'"/>
          <circle cx="22" cy="14" r="3" :fill="d.color || '#ef5350'"/>
          <circle cx="38" cy="14" r="3" :fill="d.color || '#ef5350'"/>
          <circle cx="20" cy="12" r="1.6" fill="#263238"/>
          <circle cx="40" cy="12" r="1.6" fill="#263238"/>
          <path d="M10 20 L2 14 M50 20 L58 14" :stroke="d.claw || '#e53935'" stroke-width="3" fill="none" stroke-linecap="round"/>
          <g :stroke="d.leg || '#e57373'" stroke-width="3" fill="none" stroke-linecap="round">
            <path d="M20 30 l-6 6"/><path d="M24 32 l-4 8"/><path d="M28 33 l-2 9"/>
            <path d="M40 30 l6 6"/><path d="M36 32 l4 8"/><path d="M32 33 l2 9"/>
          </g>
        </svg>

        <!-- 海豚 -->
        <svg v-else-if="d.type==='dolphin'" class="decal" :class="d.anim" :style="decalStyle(d)" viewBox="0 0 100 40">
          <path d="M4 24 C24 6, 66 4, 92 18 C72 18,52 22,38 30 C30 28,18 26,4 24 Z" :fill="d.color || '#64b5f6'"/>
          <path d="M58 14 l10 8 -12 -2 z" :fill="d.color || '#64b5f6'"/>
          <circle cx="74" cy="16" r="1.8" fill="#0d47a1"/>
        </svg>
      </template>

      <!-- 气泡 -->
      <div class="bubbles">
        <span class="b b1"></span>
        <span class="b b2"></span>
        <span class="b b3"></span>
        <span class="b b4"></span>
        <span class="b b5"></span>
      </div>
    </div>

    <!-- 内层：Tableau -->
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
import { computed } from 'vue';

const props = defineProps({
  url: { type: String, default: '' },
  src: { type: String, default: '' },
  height: { type: [Number, String], default: 520 },
  maxWidth: { type: [Number, String], default: 'min(1280px, 96vw)' },
  showDecals: { type: Boolean, default: true },
  decalsDensity: { type: String, default: 'high' } // 'low' | 'medium' | 'high'
});

const toPx = v => (typeof v === 'number' ? `${v}px` : v);

const baseUrl = computed(() => (props.url || props.src || '').trim());
const embedUrl = computed(() => {
  const u = baseUrl.value;
  if (!u) return '';
  try {
    const url = new URL(u);
    if (!url.searchParams.has(':showVizHome')) url.searchParams.set(':showVizHome', 'no');
    if (!url.searchParams.has(':embed'))       url.searchParams.set(':embed', 'y');
    if (!url.searchParams.has(':toolbar'))     url.searchParams.set(':toolbar', 'yes');
    return url.toString();
  } catch {
    return u.includes(':showVizHome') ? u : `${u}${u.includes('?') ? '&' : '?'}:showVizHome=no&:embed=y&:toolbar=yes`;
  }
});

/* 贴图点位 */
const decals = computed(() => {
  const base = [
    // top
    { type:'fish',    top: 10, left: 22,  w: 80,  anim:'anim-swim-slow', r:0 },
    { type:'jelly',   top: 14, right: 26, w: 72,  anim:'anim-float',     r:0 },
    { type:'star',    top: 12, left: 200, w: 56,  anim:'anim-rock',      r:8 },
    { type:'shell',   top: 12, right: 210,w: 52,  anim:'anim-rock',      r:-6 },
    // bottom
    { type:'weed',    bottom: 18, left: 26,  w: 74, anim:'anim-sway' },
    { type:'crab',    bottom: 18, right: 32, w: 74, anim:'anim-rock' },
    { type:'turtle',  bottom: 16, left: 200, w: 86, anim:'anim-swim-slow', r:3 },
    { type:'star',    bottom: 18, left: 420, w: 58, anim:'anim-rock', r:5 },
    // sides
    { type:'fish',    left: 18,  top: 180, w: 70, anim:'anim-swim', r:90  },
    { type:'shell',   left: 18,  bottom: 140, w: 48, anim:'anim-rock', r:12 },
    { type:'jelly',   right: 20, top: 220, w: 66, anim:'anim-float' },
    { type:'fish',    right: 22, bottom: 160, w: 72, anim:'anim-swim', r:-90 },
    // corners
    { type:'star',    right: 24, bottom: 22, w: 64, anim:'anim-rock', r:6 },
    { type:'weed',    left: 24,  bottom: 22, w: 68, anim:'anim-sway' }
  ];
  if (props.decalsDensity === 'low') return base.slice(0, 7);
  if (props.decalsDensity === 'medium') return base.slice(0, 11);
  return base;
});

/* ✅ 关键：模板里调用的样式函数 */
function decalStyle(d) {
  const s = {};
  if (d.top    != null) s.top    = `${d.top}px`;
  if (d.right  != null) s.right  = `${d.right}px`;
  if (d.bottom != null) s.bottom = `${d.bottom}px`;
  if (d.left   != null) s.left   = `${d.left}px`;
  if (d.w      != null) s.width  = `${d.w}px`;
  // 用 CSS 变量传递旋转角度，避免与动画的 transform 冲突
  s['--rot'] = (d.r != null ? `${d.r}deg` : '0deg');
  return s;
}

/* 海洋边框 SVG */
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
`)}")`;
</script>

<style scoped>
.ocean-frame {
  position: relative;
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

/* 贴图层 */
.ocean-decals {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 2;
}

/* 通用贴图：用 CSS 变量 --rot 与动画组合 */
.decal {
  position: absolute;
  opacity: 0.95;
  filter: drop-shadow(0 4px 6px rgba(0,0,0,0.15));
  transform: rotate(var(--rot));
  transform-origin: center;
}

/* 内层白底 */
.ocean-frame__inner {
  position: relative;
  z-index: 1;
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

/* 动画：与 --rot 组合，避免覆盖 */
.anim-swim {
  animation: swim 12s ease-in-out infinite;
}
@keyframes swim {
  0%,100% { transform: rotate(var(--rot)) translateX(0) }
  50%     { transform: rotate(var(--rot)) translateX(18px) }
}
.anim-swim-slow { animation: swim-slow 18s ease-in-out infinite; }
@keyframes swim-slow {
  0%,100% { transform: rotate(var(--rot)) translateX(0) }
  50%     { transform: rotate(var(--rot)) translateX(14px) }
}
.anim-float { animation: float 10s ease-in-out infinite; }
@keyframes float {
  0%,100% { transform: rotate(var(--rot)) translateY(0) }
  50%     { transform: rotate(var(--rot)) translateY(-12px) }
}
.anim-rock { animation: rock 8s ease-in-out infinite; }
@keyframes rock {
  0%,100% { transform: rotate(calc(var(--rot) + 6deg)) }
  50%     { transform: rotate(calc(var(--rot) - 6deg)) }
}
.anim-sway { animation: sway 7s ease-in-out infinite; }
@keyframes sway {
  0%,100% { transform: rotate(var(--rot)) }
  50%     { transform: rotate(calc(var(--rot) + 4deg)) }
}

/* 气泡 */
.bubbles { position: absolute; left: 60px; bottom: 30px; width: 0; height: 0; z-index: 2; }
.bubbles .b {
  position: absolute; bottom: 0; left: 0;
  width: 10px; height: 10px; border-radius: 50%;
  background: rgba(255,255,255,0.7);
  animation: bubble 6s linear infinite;
}
.b1 { animation-delay: 0s;   transform: translateX(0) }
.b2 { animation-delay: 1s;   transform: translateX(18px) scale(0.9) }
.b3 { animation-delay: 2s;   transform: translateX(-14px) scale(0.85) }
.b4 { animation-delay: 3s;   transform: translateX(8px)  scale(0.95) }
.b5 { animation-delay: 4.5s; transform: translateX(-8px) scale(0.8) }

@keyframes bubble {
  0% { opacity: 0; transform: translateY(0) scale(0.8); }
  10%{ opacity: 1; }
  100%{ opacity: 0; transform: translateY(-160px) scale(1.2); }
}
</style>
