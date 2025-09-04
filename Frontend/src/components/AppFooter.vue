<template>
  <footer class="o-footer">
    <svg class="waves" viewBox="0 0 1200 100" preserveAspectRatio="none" aria-hidden="true">
      <path class="wave wave-1" d="M0,40 C200,80 400,0 600,40 C800,80 1000,0 1200,40 L1200,0 L0,0 Z"/>
      <path class="wave wave-2" d="M0,60 C200,100 400,20 600,60 C800,100 1000,20 1200,60 L1200,0 L0,0 Z"/>
    </svg>

    <div class="ocean-ornaments" aria-hidden="true"></div>

    <div class="o-container">
      <RouterLink to="/" class="brand">
        <svg class="fish" viewBox="0 0 60 30" aria-hidden="true">
          <ellipse cx="28" cy="15" rx="16" ry="10" fill="#ffd54f"/>
          <polygon points="0,15 14,6 14,24" fill="#ffb300"/>
          <circle cx="36" cy="13" r="2.2" fill="#0f172a"/>
          <path d="M18 10 C22 15,22 15,18 20" stroke="#ff8f00" stroke-width="2" fill="none"/>
        </svg>
        <span class="title">{{ title }}</span>
      </RouterLink>

      <div class="spacer" />
    </div>

    <div class="sub">
      <slot name="copyright">
        © {{ year }} Team Lakers · All rights reserved.
      </slot>
    </div>
  </footer>
</template>

<script setup>
const props = defineProps({
  title: { type: String, default: 'Port Philip Protectors' }
})
const year = new Date().getFullYear()
</script>

<style scoped>
.o-footer{
  position: relative;
  color:#eaf7ff;
  background: linear-gradient(
    180deg,
    #1f3b82 0%,
    #1e40af 40%,
    #4338ca 75%,
    #4f46e5 100%
  );
  border-top: 1px solid rgba(255,255,255,0.16);
  box-shadow: 0 -6px 18px rgba(0,0,0,0.08);
  overflow: hidden;
}

.waves{
  position:absolute; left:0; right:0; top:-1px;
  width:100%; height:20px; /* thinner */
}
.wave{ fill:rgba(255,255,255,.12); }
.wave-1{ animation: drift 12s linear infinite; }
.wave-2{ animation: drift 9s linear infinite reverse; opacity:.7; }
@keyframes drift{ 0%{transform:translateX(0)} 100%{transform:translateX(-50%)} }

.ocean-ornaments{
  pointer-events:none;
  position:absolute; inset:0;
  background:
    radial-gradient(120px 60px at 12% 100%, rgba(255,255,255,.16), transparent 60%),
    radial-gradient(140px 70px at 44% 110%, rgba(255,255,255,.14), transparent 70%),
    radial-gradient(160px 80px at 82% 100%, rgba(255,255,255,.12), transparent 70%),
    repeating-linear-gradient(125deg, rgba(255,255,255,.06) 0 14px, rgba(255,255,255,.03) 14px 28px);
  mask-image: linear-gradient(to top, rgba(0,0,0,.9), rgba(0,0,0,.25));
  opacity:.8;
}

.o-container{
  display:flex; align-items:center; gap:12px;
  padding:8px 12px 4px; /* thinner */
}
.brand{
  display:flex; align-items:center; gap:10px;
  color:#fff; text-decoration:none; font-weight:700;
}
.brand .fish{ width:24px; height:auto; filter: drop-shadow(0 3px 6px rgba(0,0,0,.18)); } /* smaller */
.title{ font-size:16px; line-height:1; text-shadow: 0 1px 2px rgba(0,0,0,.18); } /* smaller */
.spacer{ flex:1; }

.sub{
  padding:4px 12px 8px; /* thinner */
  font-size:12px; color:#d9f0ff; opacity:.9;
  text-align:center;
}

@media (max-width: 640px){
  .o-container{ padding:6px 10px 4px; }
  .title{ font-size:15px; }
}
</style>
