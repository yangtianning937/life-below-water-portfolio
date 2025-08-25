// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

import Epic1Page from '@/pages/Epic1Page.vue'
import Epic2List from '@/pages/Epic2List.vue'
import Epic2Register from '@/pages/Epic2Register.vue'

const routes = [
  { path: '/', redirect: { name: 'epic1' } },
  { path: '/epic1', name: 'epic1', component: Epic1Page },

  // Epic 2
  { path: '/epic2', name: 'epic2', component: Epic2List },
  { path: '/epic2/register/:id', name: 'epic2-register', component: Epic2Register, props: true },
]

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})
