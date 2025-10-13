<template>
  <div class="page">
    <header class="pagebar">
      <button class="back-arrow" @click="goBack" aria-label="Go back to previous page">
        <span>Previous</span>
      </button>
      <h1 class="pagebar__title">Protect our Bay · Bacteria Patrol</h1>
      <div class="pagebar__spacer"></div>
    </header>

    <section class="content-wrap">
      <div class="desc">
        <h2>Bacteria Patrol at the Beach</h2>
        <p>
          Meet the enterococci—tiny bacteria that tell us if the water has been contaminated
          (human and animals’ poops!). The bar chart below is like a detective tool: it shows
          how much of these bacteria were found at different beaches in Port Phillip Bay over the past 12 years.
        </p>
        <p>
          You can even pick which year you want to spy on using the filter box. If the average number is more
          than 200 in 100 mL of water, that means the water isn’t safe for swimming.
        </p>
        <p>Can you spot which beaches need a clean-up? Let’s protect our bay!</p>
      </div>

      <!-- 这里是 Tableau 容器（按你的 snippet 注入） -->
      <div ref="vizRoot" class="tableau-host"></div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
function goBack() {
  if (history.length > 1) router.back()
  else router.push('/learningModule')
}

const vizRoot = ref<HTMLDivElement | null>(null)
let removeResize: (() => void) | null = null

onMounted(() => {
  const root = vizRoot.value
  if (!root) return

  // 用你的原始嵌入代码（只把 id 改成可控的）
  const embedId = 'viz_bacteria_patrol'
  root.innerHTML = `
    <div class='tableauPlaceholder' id='${embedId}' style='position: relative'>
      <noscript>
        <a href='#'>
          <img alt='Bacteria in Water by Year in Different Sites '
               src='https://public.tableau.com/static/images/Ne/NewWorkbook2_17590370510770/Sheet1/1_rss.png'
               style='border: none' />
        </a>
      </noscript>
      <object class='tableauViz' style='display:none;'>
        <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
        <param name='embed_code_version' value='3' />
        <param name='site_root' value='' />
        <param name='name' value='NewWorkbook2_17590370510770/Sheet1' />
        <param name='tabs' value='no' />
        <param name='toolbar' value='yes' />
        <param name='static_image' value='https://public.tableau.com/static/images/Ne/NewWorkbook2_17590370510770/Sheet1/1.png' />
        <param name='animate_transition' value='yes' />
        <param name='display_static_image' value='yes' />
        <param name='display_spinner' value='yes' />
        <param name='display_overlay' value='yes' />
        <param name='display_count' value='yes' />
        <param name='language' value='en-US' />
      </object>
    </div>
  `

  const divElement = document.getElementById(embedId)!
  const vizObject = divElement.getElementsByTagName('object')[0] as HTMLElement

  // 自适应：宽度 100%，高度按 4:3（=0.75）比
  const setSize = () => {
    vizObject.style.width = '100%'
    vizObject.style.height = (divElement.offsetWidth * 0.75) + 'px'
  }
  setSize()
  window.addEventListener('resize', setSize)
  removeResize = () => window.removeEventListener('resize', setSize)

  // 加载 Tableau 脚本
  const scriptElement = document.createElement('script')
  scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js'
  // 按你的原始做法：插入到 object 前（也可以 append 到 divElement 末尾）
  vizObject.parentNode!.insertBefore(scriptElement, vizObject)
})

onBeforeUnmount(() => {
  removeResize?.()
})
</script>

<style scoped>
.page { display:flex; flex-direction:column; min-height:100vh; }

.pagebar {
  display:flex; align-items:center; gap:12px;
  padding:10px 16px; border-bottom:1px solid #e5e7eb;
}
.pagebar__title { font-weight:700; font-size:18px; }
.pagebar__spacer { flex:1; }
.back-arrow{
  position:relative; border:none; cursor:pointer;
  font-weight:800; color:#0b1220; background:#e8b6ae;
  padding:12px 18px 12px 46px; border-radius:6px;
  box-shadow:0 6px 14px rgba(15,23,42,.08);
}
.back-arrow::before{
  content:''; position:absolute; left:-28px; top:0; width:0; height:0;
  border-top:26px solid transparent; border-bottom:26px solid transparent;
  border-right:28px solid #e8b6ae;
}

.content-wrap { padding:16px; }
.desc { max-width:960px; margin:0 auto 14px; }
.desc h2 { font-size:22px; margin-bottom:6px; }

/* 外层容器，限定最大宽度，居中显示 */
.tableau-host {
  width: 100%;
  max-width: 1600px;
  margin: 8px auto 24px;
}
</style>
