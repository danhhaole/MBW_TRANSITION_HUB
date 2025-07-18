import { createRouter, createWebHistory } from 'vue-router'

import { userResource } from '@/stores/user'
import { sessionStore } from '@/stores/session'

// Talent Segment
import TalentSegments from './pages/TalentSegmentManagement.vue'
import TalentSegmentDetail from './pages/TalentSegmentDetail.vue'
import TalentSegmentDetailView from './pages/TalentSegmentDetailView.vue'

// Campaign Management
import CampaignManagement from './pages/CampaignManagement.vue'
import CampaignDetailView from './pages/CampaignDetailView.vue'

// Candidate Management
import CandidateManagement from './pages/CandidateManagement.vue'
import CandidateDetailView from './pages/CandidateDetailView.vue'

// Interaction Management
import InteractionManagement from './pages/InteractionManagement.vue'

// Action Management
import ActionManagement from './pages/ActionManagement.vue'

// Email Log Management
import EmailLogManagement from './pages/EmailLogManagement.vue'

// Candidate Data Source Management
import CandidateDataSourceManagement from './pages/CandidateDataSourceManagement.vue'

// Candidate Data Source Management Direct
import CandidateDataSourceManagementDirect from './pages/CandidateDataSourceManagementDirect.vue'

// Candidate Pool Management
import CandidatePoolManagement from './pages/CandidatePoolManagement.vue'

const routes = [
	{
		path: '/',
		name: 'Dashboard',
		component: () => import('@/pages/Dashboard.vue'),
	},
	{
		alias: '/talentsegment',
		path: '/talentsegment',
		name: 'TalentSegment',
		component: () => import('@/pages/TalentSegment.vue'),
	},
	{
		alias: '/candidate',
		path: '/candidate',
		name: 'Candidate',
		component: () => import('@/pages/Candidate.vue'),
	},
	{
		alias: '/campaigns',
		path: '/campaigns',
		name: 'CampaignManagement',
		component: CampaignManagement,
	},
	{
		path: '/campaigns/:id',
		component: CampaignDetailView,

		name: 'CampaignDetailView',
	},
	{
		alias: '/report',
		path: '/report',
		name: 'Report',
		component: () => import('@/pages/Report.vue'),
	},
	{
		alias: '/settings',
		path: '/settings',
		name: 'Settings',
		component: () => import('@/pages/Settings.vue'),
	},
	{
		path: '/:invalidpath',
		name: 'Invalid Page',
		component: () => import('@/pages/InvalidPage.vue'),
	},
	{
		path: '/talent-segments',
		component: TalentSegments,
		name: 'TalentSegments',
	},
	{
		path: '/talent-segments/:id',
		component: TalentSegmentDetailView,
		name: 'TalentSegmentDetail',
	},
	{
		path: '/talent-segments/:id/detail',
		component: TalentSegmentDetailView,
		name: 'TalentSegmentDetailView',
	},

	{
		path: '/candidates',
		component: CandidateManagement,
		name: 'CandidateManagement',
	},
	{
		path: '/candidates/:id',
		component: CandidateDetailView,
		name: 'CandidateDetailView',
	},
	{
		path: '/interactions',
		component: InteractionManagement,
		name: 'InteractionManagement',
	},
	{
		path: '/actions',
		component: ActionManagement,
		name: 'ActionManagement',
	},
	{
		path: '/email-logs',
		component: EmailLogManagement,
		name: 'EmailLogManagement',
	},
	{
		path: '/data-sources',
		component: CandidateDataSourceManagement,
		name: 'CandidateDataSourceManagement',
	},
	{
		path: '/data-sources-direct',
		component: CandidateDataSourceManagementDirect,
		name: 'CandidateDataSourceManagementDirect',
	},
	{
		path: '/candidate-pools',
		component: CandidatePoolManagement,
		name: 'CandidatePoolManagement',
	},
]

const scrollBehavior = (to, from, savedPosition) => {
	if (to.name === from.name) {
		to.meta?.scrollPos && (to.meta.scrollPos.top = 0);
		return { left: 0, top: 0 };
	}
	const scrollpos = to.meta?.scrollPos || { left: 0, top: 0 };

	if (scrollpos.top > 0) {
		setTimeout(() => {
			let el = document.querySelector("#list-rows");
			el.scrollTo({
				top: scrollpos.top,
				left: scrollpos.left,
				behavior: "smooth",
			});
		}, 300);
	}
};

let router = createRouter({
	history: createWebHistory('/mbw_mira'),
	routes,
	scrollBehavior
})

router.beforeEach(async (to, from, next) => {
	const { isLoggedIn } = sessionStore()
	isLoggedIn && (await userResource.promise)

	// Nếu user đã login và đang truy cập trang login, redirect về dashboard
	if (!isLoggedIn) {
		window.location.href = "/login?redirect-to=/mbw_mira/";
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
