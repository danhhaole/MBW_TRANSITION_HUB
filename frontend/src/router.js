import { createRouter, createWebHistory } from 'vue-router'


import { userResource } from '@/stores/user'
import { sessionStore } from '@/stores/session'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/pages/Dashboard.vue'),
  }, {
    alias: '/talentsegment',
    path: '/talentsegment',
    name: 'TalentSegment',
    component: () => import('@/pages/TalentSegment.vue'),
  }, {
    alias: '/candidate',
    path: '/candidate',
    name: 'Candidate',
    component: () => import('@/pages/Candidate.vue'),
  },{
    alias: '/campaigns',
    path: '/campaigns',
    name: 'Campaigns',
    component: () => import('@/pages/Campaigns.vue'),
  },{
    alias: '/report',
    path: '/report',
    name: 'Report',
    component: () => import('@/pages/Report.vue'),
  },{
    alias: '/settings',
    path: '/settings',
    name: 'Settings',
    component: () => import('@/pages/Settings.vue'),
  },{
    path: '/:invalidpath',
    name: 'Invalid Page',
    component: () => import('@/pages/InvalidPage.vue'),
  },
]

let router = createRouter({
  history: createWebHistory('/mbw_mira'),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const { isLoggedIn } = sessionStore()
  isLoggedIn && (await userResource.promise)

  // Nếu user đã login và đang truy cập trang login, redirect về dashboard
  if (!isLoggedIn) {
    next('/login')
    return
  } else if (['Test'].includes(to.name) && !to.hash) {
    let storageKey = to.name === 'Test' ? 'lastTestTab' : 'lastTestTab'
    const activeTab = localStorage.getItem(storageKey) || 'activity'
    const hash = '#' + activeTab
    next({ ...to, hash })
  } else {

    next()
  }
})

export default router
