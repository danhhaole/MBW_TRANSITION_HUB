import { createRouter, createWebHistory } from 'vue-router'

import Home from '@/pages/Home.vue'
import Login from '@/pages/Login.vue'
import Dashboard from '@/pages/Dashboard.vue'
import CampaignManagement from '@/pages/CampaignManagement.vue'
import TalentSegments from '@/pages/TalentSegmentManagement.vue'
import TalentSegmentDetail from '@/pages/TalentSegmentDetail.vue'
import CandidateManagement from '@/pages/CandidateManagement.vue'
import { userResource } from '@/stores/user'
import { sessionStore } from '@/stores/session'

const routes = [
  {
    path: '/',
    component: Home,
    meta: { layout: 'private' }
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
  },
  {
    path: '/campaigns',
    component: CampaignManagement,
    meta: { layout: 'private' },
    name: 'CampaignManagement'
  },
  {
    path: '/talent-segments',
    component: TalentSegments,
    meta: { layout: 'private' },
    name: 'TalentSegments'
  },
  {
    path: '/talent-segments/:id',
    component: TalentSegmentDetail,
    meta: { layout: 'private' },
    name: 'TalentSegmentDetail'
  },
  {
    path: '/candidates',
    component: CandidateManagement,
    meta: { layout: 'private' },
    name: 'CandidateManagement'
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
     next('/login')
    //window.location.href = '/login?redirect-to=/mbw_mira'
  }else{
    next()
  }
})

export default router
