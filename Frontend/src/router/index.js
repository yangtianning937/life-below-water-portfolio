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
import BacteriaPatrol from '@/pages/BacteriaPatrol.vue'
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
        path: '/learningModule/bacteria-patrol',
        name: 'BacteriaPatrol',
        component: BacteriaPatrol,
        meta: { title: 'LifeBelowWater | Bacteria Patrol' },
    },

    {
        path: '/epic1',
        name: 'data_hub', // Consistent with AppHeader.vue navigation naming
        component: WaterQuality,
        meta: {title: 'LifeBelowWater | Marine Environment Data Hub'}
    },
    {
        path: '/epic2',
        name: 'activity', // Consistent with navigation naming
        component: Epic2List,
        meta: {title: 'LifeBelowWater | Volunteer Activity', forceRefresh: true}
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
    // 404 Not Found
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
    // If deployed in subpath, change to createWebHistory('/subpath/')
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) return savedPosition
        if (to.hash) return {el: to.hash, behavior: 'smooth'}
        return {left: 0, top: 0, behavior: 'smooth'}
    }
})

// Access control: unauthenticated users → lock page
router.beforeEach((to) => {
    const {isAuthed} = useAuth()
    // If accessing lock page, allow directly
    if (to.meta?.public || to.name === 'lock') return true
    // If authenticated, allow
    if (isAuthed()) return true
    // Unauthenticated, save target path and redirect to lock page
    if (to.path !== '/') {
        sessionStorage.setItem('redirect_after_login', to.fullPath)
    }
    return {name: 'lock'}
})


// Dynamically set page title
router.afterEach((to) => {
    document.title = to.meta?.title || 'LifeBelowWater'
})

export default router
