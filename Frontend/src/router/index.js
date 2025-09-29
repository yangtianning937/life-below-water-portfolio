// FRONTEND/src/router/index.js
import {createRouter, createWebHistory} from 'vue-router'

// Pages
import HomePage from '@/pages/HomePage.vue'
import WaterQuality from '@/pages/Epic1Page.vue'
import Epic2List from '@/pages/Epic2List.vue'
import Epic2Register from '@/pages/Epic2Register.vue'
import LearningModule from "@/pages/LearningModule.vue";
import LockPage from "@/pages/LockPage.vue";
import MarineQuiz from "@/pages/MarineQuiz.vue";
import {useAuth} from "@/assets/security/auth";

const routes = [
    {path: '/', name: 'lock', component: LockPage, meta: {public: true, title: 'LifeBelowWater | Unlock'}},
    {
        path: '/home',
        name: 'home',
        component: HomePage,
        meta: {title: 'LifeBelowWater | Home'}
    },
    {
        path: '/learningModule',
        name: 'learningModule',
        component: LearningModule,
        meta: {title: 'LifeBelowWater | LearningModule'}
    },
    {
        path: '/epic1',
        name: 'data_hub', // 与导航栏 AppHeader.vue 的命名一致
        component: WaterQuality,
        meta: {title: 'LifeBelowWater | Marine Environment Data Hub'}
    },
    {
        path: '/epic2',
        name: 'activity', // 与导航栏命名一致
        component: Epic2List,
        meta: {title: 'LifeBelowWater | Volunteer Activity'}
    },
    {
        path: '/epic2/register/:id',
        name: 'activity_register',
        component: Epic2Register,
        props: true,
        meta: {title: 'LifeBelowWater | Register Activity'}
    },
    {
        path: '/marine_quiz',
        name: 'marine_quiz',
        component: MarineQuiz
    },
    {
        path: '/nearby',
        name: 'nearby',
        component: () => import('@/pages/NearbyBeach.vue'),
        meta: {title: 'LifeBelowWater | Nearby Beach'}
    },
    {
        path: '/fish_identity',
        name: 'fish_identity',
        component: () => import('@/pages/FishIdentity.vue'),
        meta: {title: 'LifeBelowWater | Fish Identity'}
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
        meta: {title: 'LifeBelowWater | 404'}
    }
]

const router = createRouter({
    // 如果部署在子路径，改为 createWebHistory('/子路径/')
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) return savedPosition
        if (to.hash) return {el: to.hash, behavior: 'smooth'}
        return {left: 0, top: 0, behavior: 'smooth'}
    }
})

// 访问控制：未登录 → 锁页
router.beforeEach((to) => {
    const {isAuthed} = useAuth()
    if (to.meta?.public) return true
    if (isAuthed()) return true
    sessionStorage.setItem('redirect_after_login', to.fullPath || '/home')
    return {name: 'lock'}
})


// 动态设置页面标题
router.afterEach((to) => {
    document.title = to.meta?.title || 'LifeBelowWater'
})

export default router
