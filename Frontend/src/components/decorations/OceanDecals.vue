<template>
  <!-- 动态 teleport 目标：body / 全屏元素 -->
  <teleport :to="mountTo">
    <div
      v-if="enabled"
      class="ocean-decals-global"
      :style="{ '--z': zIndex, '--opacity': opacity }"
      aria-hidden="true"
    >
      <template v-for="(d, i) in decals" :key="i">
        <!-- 鱼 -->
        <svg v-if="d.type==='fish'" class="decal anim-swim-slow" :style="decalStyle(d)" viewBox="0 0 60 30">
          <ellipse cx="28" cy="15" rx="16" ry="10" fill="#ffd54f"/>
          <polygon points="0,15 14,6 14,24" fill="#ffb300"/>
          <circle cx="36" cy="13" r="2.2" fill="#263238"/>
          <path d="M18 10 C22 15,22 15,18 20" stroke="#ff8f00" stroke-width="2" fill="none"/>
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
  </teleport>
</template>

<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  enabled: { type: Boolean, default: true },
  density: { type: String, default: 'high' },       // 'low' | 'medium' | 'high'
  opacity: { type: Number, default: 0.9 },            // 0~1
  zIndex:  { type: [Number, String], default: 5 },

  /** 选择器或元素：用于“伪全屏”容器（可选）。 */
  to: { type: [String, Object], default: 'body' },

  /** 自动跟随“真全屏”。开启后在 fullscreenchange 时把 teleport 目标切到 document.fullscreenElement */
  followFullscreen: { type: Boolean, default: true }
})

/* 计算贴图 */
const decals = computed(() => {
  const base = [
    { type:'fish', top: 16, left: 300,  w: 82, r:0 },
    { type:'jelly', top: 16, right: 32, w: 74, r:0 },
    { type:'weed', bottom: 24, left: 34, w: 74, r:0 },
    { type:'crab', bottom: 24, right: 500, w: 74, r:0 },
    // ……按需继续补……
  ]
  if (props.density === 'low') return base.slice(0, 4)
  if (props.density === 'medium') return base
  return base.concat([
    { type:'star', right: 28, bottom: 26, w: 60, r:8 },
    { type:'turtle', bottom: 22, left: 260, w: 86, r:3 },
  ])
})

function decalStyle(d) {
  const s = {}
  if (d.top    != null) s.top    = `${d.top}px`
  if (d.right  != null) s.right  = `${d.right}px`
  if (d.bottom != null) s.bottom = `${d.bottom}px`
  if (d.left   != null) s.left   = `${d.left}px`
  if (d.w      != null) s.width  = `${d.w}px`
  return s
}

/* 动态 teleport 目标 */
const mountTo = ref(props.to)

function handleFsChange() {
  if (!props.followFullscreen) return
  const fsEl = document.fullscreenElement
  // 全屏中 => 将 teleport 目标切到全屏元素；退出 => 切回 props.to（默认 body）
  mountTo.value = fsEl || props.to
}

onMounted(() => {
  handleFsChange()
  document.addEventListener('fullscreenchange', handleFsChange)
})
onBeforeUnmount(() => {
  document.removeEventListener('fullscreenchange', handleFsChange)
})
</script>

<style scoped>
.ocean-decals-global {
  position: fixed;
  inset: 0;
  z-index: var(--z);
  pointer-events: none;
  opacity: var(--opacity);
}
.decal { position: absolute; opacity: .95; filter: drop-shadow(0 4px 6px rgba(0,0,0,.15)); }
.anim-swim-slow { animation: swim-slow 18s ease-in-out infinite; }
@keyframes swim-slow { 0%,100%{ transform: translateX(0) } 50%{ transform: translateX(14px) } }

.bubbles { position: absolute; left: 60px; bottom: 30px; width: 0; height: 0; }
.bubbles .b{ position:absolute; bottom:0; left:0; width:10px; height:10px; border-radius:50%; background:rgba(255,255,255,.7); animation:bubble 6s linear infinite; }
.b1{animation-delay:0s} .b2{animation-delay:1s} .b3{animation-delay:2s} .b4{animation-delay:3s} .b5{animation-delay:4.5s}
@keyframes bubble{0%{opacity:0;transform:translateY(0) scale(.8)}10%{opacity:1}100%{opacity:0;transform:translateY(-160px) scale(1.2)}}
</style>
