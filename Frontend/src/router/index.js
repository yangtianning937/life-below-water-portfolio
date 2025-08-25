// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

import Epic1Page from '@/pages/Epic1Page.vue'
import Epic2List from '@/pages/Epic2List.vue'
import Epic2Register from '@/pages/Epic2Register.vue'

const routes = [
  { path: '/', redirect: { name: 'data_hub' } },
  { path: '/data_hub', name: 'data_hub', component: Epic1Page },

  // Epic 2
  { path: '/activity', name: 'activity', component: Epic2List },
  { path: '/activity/register/:id', name: 'activity_register', component: Epic2Register, props: true },
]

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})
