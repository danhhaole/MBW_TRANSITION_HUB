import { createRouter, createWebHistory } from 'vue-router'


import Login from '@/pages/Login.vue'
import Dashboard from '@/pages/Dashboard.vue'
import CampaignManagement from '@/pages/CampaignManagement.vue'
import CampaignStepManagement from '@/pages/CampaignStepManagement.vue'
import TalentSegments from '@/pages/TalentSegmentManagement.vue'
import TalentSegmentDetail from '@/pages/TalentSegmentDetail.vue'
import TalentSegmentDetailView from '@/pages/TalentSegmentDetailView.vue'
import CandidateManagement from '@/pages/CandidateManagement.vue'
import CandidateDetailView from '@/pages/CandidateDetailView.vue'
import CandidateSegmentManagement from '@/pages/CandidateSegmentManagement.vue'
import CandidateCampaignManagement from '@/pages/CandidateCampaignManagement.vue'
import CampaignDetailView from '@/pages/CampaignDetailView.vue'
import ActionManagement from '@/pages/ActionManagement.vue'
import InteractionManagement from '@/pages/InteractionManagement.vue'
import EmailLogManagement from '@/pages/EmailLogManagement.vue'
import ProductIntroduction from '@/pages/ProductIntroduction.vue'
import TestLinkField from '@/components/TestLinkField.vue'
import { userResource } from '@/stores/user'
import { sessionStore } from '@/stores/session'
import LinkFieldDemo from './components/LinkFieldDemo.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard', // Redirect trực tiếp đến dashboard
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
    path: '/campaigns/:id',
    component: CampaignDetailView,
    meta: { layout: 'private' },
    name: 'CampaignDetailView'
  },
  {
    path: '/campaign-steps',
    component: CampaignStepManagement,
    meta: { layout: 'private' },
    name: 'CampaignStepManagement'
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
    path: '/talent-segments/:id/detail',
    component: TalentSegmentDetailView,
    meta: { layout: 'private' },
    name: 'TalentSegmentDetailView'
  },
  {
    path: '/candidates',
    component: CandidateManagement,
    meta: { layout: 'private' },
    name: 'CandidateManagement'
  },
  {
    path: '/candidates/:id',
    component: CandidateDetailView,
    meta: { layout: 'private' },
    name: 'CandidateDetailView'
  },
  {
    path: '/candidate-segments',
    component: CandidateSegmentManagement,
    meta: { layout: 'private' },
    name: 'CandidateSegmentManagement'
  },
  {
    path: '/candidate-campaigns',
    component: CandidateCampaignManagement,
    meta: { layout: 'private' },
    name: 'CandidateCampaignManagement'
  },
  {
    path: '/actions',
    component: ActionManagement,
    meta: { layout: 'private' },
    name: 'ActionManagement'
  },
  {
    path: '/interactions',
    component: InteractionManagement,
    meta: { layout: 'private' },
    name: 'InteractionManagement'
  },
  {
    path: '/email-logs',
    component: EmailLogManagement,
    meta: { layout: 'private' },
    name: 'EmailLogManagement'
  },
  {
    path: '/product-introduction',
    component: ProductIntroduction,
    meta: { layout: 'public' },
    name: 'ProductIntroduction'
  },
  {
    path: '/test-link-field',
    component: TestLinkField,
    meta: { layout: 'private' },
    name: 'TestLinkField'
  },
  {
    path: '/link-field-demo',
    component: LinkFieldDemo,
    meta: { layout: 'private' },
    name: 'LinkFieldDemo'
  }
]

let router = createRouter({
  history: createWebHistory('/mbw_mira'),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const { isLoggedIn } = sessionStore()
  isLoggedIn && (await userResource.promise)
  
  // Nếu user đã login và đang truy cập trang login, redirect về dashboard
  if (isLoggedIn && to.path === '/login') {
    next('/dashboard')
    return
  }
  
  // Nếu user chưa login và truy cập private route, redirect về login
  if (to.meta.layout === 'private' && !isLoggedIn) {
    next('/login')
    return
  }
  
  next()
})

export default router
