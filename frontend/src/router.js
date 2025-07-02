import { createRouter, createWebHistory } from 'vue-router'

import Home from '@/pages/Home.vue'
import Login from '@/pages/Login.vue'
import Dashboard from '@/pages/Dashboard.vue'
import { userResource } from '@/stores/user'
import { sessionStore } from '@/stores/session'

const routes = [
  {
    path: '/',
    component: Home,
    meta: { layout: 'public' }
  },
  {
    path: '/login',
    component: Login,
    meta: { layout: 'public' }
  },
  {
    path: '/dashboard',
    component: Dashboard,
    meta: { layout: 'private' }
  }
]

let router = createRouter({
  history: createWebHistory('/mbw_mira'),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const { isLoggedIn } = sessionStore()
  isLoggedIn && (await userResource.promise)
  const isAuthenticated = true // kiểm tra login ở đây
  if (to.meta.layout === 'private' && !isLoggedIn) {
    window.location.href = '/login?redirect-to=/mbw_mira'
  }else{
    next()
  }
})

export default router
