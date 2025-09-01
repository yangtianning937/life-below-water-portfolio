// FRONTEND/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// Pages
import HomePage from '@/pages/HomePage.vue'
import Epic1Page from '@/pages/Epic1Page.vue'
import Epic2List from '@/pages/Epic2List.vue'
import Epic2Register from '@/pages/Epic2Register.vue'



const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage,
    meta: { title: 'LifeBelowWater | Home' }
  },
  {
    path: '/epic1',
    name: 'data_hub', // 与导航栏 AppHeader.vue 的命名一致
    component: Epic1Page,
    meta: { title: 'LifeBelowWater | Marine Environment Data Hub' }
  },
  {
    path: '/epic2',
    name: 'activity', // 与导航栏命名一致
    component: Epic2List,
    meta: { title: 'LifeBelowWater | Volunteer Activity' }
  },
  {
    path: '/epic2/register',
    name: 'activity_register',
    component: Epic2Register,
    meta: { title: 'LifeBelowWater | Register Activity' }
  },
  
  // 404
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: {
      template: `
        <section style="min-height:60vh;display:grid;place-items:center;text-align:center;padding:40px">
          <div>
            <h1 style="font-size:28px;margin:0 0 8px;">404 - Page Not Found</h1>
            <p style="margin:0 0 16px;color:#6b7280;">The page you are looking for doesn’t exist.</p>
            <router-link to="/" style="color:#2563eb;text-decoration:underline;">Back to Home</router-link>
          </div>
        </section>
      `
    },
    meta: { title: 'LifeBelowWater | 404' }
  }
]

const router = createRouter({
  // 如果部署在子路径，改为 createWebHistory('/子路径/')
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { left: 0, top: 0, behavior: 'smooth' }
  }
})

// 动态设置页面标题
router.afterEach((to) => {
  document.title = to.meta?.title || 'LifeBelowWater'
})

export default router
