import { createRouter, createWebHistory } from 'vue-router'

import Home from '@/pages/Home.vue'
import Login from '@/pages/Login.vue'
import Dashboard from '@/pages/Dashboard.vue'
import CampaignManagement from '@/pages/CampaignManagement.vue'
import CampaignStepManagement from '@/pages/CampaignStepManagement.vue'
import TalentSegments from '@/pages/TalentSegmentManagement.vue'
import TalentSegmentDetail from '@/pages/TalentSegmentDetail.vue'
import CandidateManagement from '@/pages/CandidateManagement.vue'
import CandidateSegmentManagement from '@/pages/CandidateSegmentManagement.vue'
import CandidateCampaignManagement from '@/pages/CandidateCampaignManagement.vue'
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
    path: '/candidates',
    component: CandidateManagement,
    meta: { layout: 'private' },
    name: 'CandidateManagement'
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
  const isAuthenticated = true // kiểm tra login ở đây
  if (to.meta.layout === 'private' && !isLoggedIn) {
     next('/login')
    //window.location.href = '/login?redirect-to=/mbw_mira'
  }else{
    next()
  }
})

export default router
