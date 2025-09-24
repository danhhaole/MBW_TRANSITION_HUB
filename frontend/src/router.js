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
import CandidateDataSourceManagementDirect from './pages/CandidateDataSourceManagementDirect.vue'

// Candidate Pool Management
import CandidatePoolManagement from './pages/CandidatePoolManagement.vue'


// Email Editor
import EmailEditor from './pages/EmailEditor.vue'
import LadiPageEditor from './pages/LadiPageEditor.vue'
import LadiPageView from './pages/LadiPageView.vue'
import ApplicantPoolManagement from './pages/ApplicantPoolManagement.vue'


// Public Profile
import LadiPage from './pages/Public/LadiPage.vue'
import RegisterPage from './pages/Public/RegisterPage.vue'
import UnSubscribePage from './pages/Public/UnSubscribePage.vue'
import ApplicationPage from './pages/Public/ApplicationPage.vue'

const routes = [
	{ path: '/', name: 'Dashboard', component: () => import('@/pages/Dashboard.vue') },
	{ alias: '/talentsegment', path: '/talentsegment', name: 'TalentSegment', component: () => import('@/pages/TalentSegment.vue') },
	{ alias: '/candidate', path: '/candidate', name: 'Candidate', component: () => import('@/pages/Candidate.vue') },
	{ alias: '/campaigns', path: '/campaigns', name: 'CampaignManagement', component: CampaignManagement },
	{ path: '/campaigns/:id', name: 'CampaignDetailView', component: CampaignDetailView },
	{ path: '/job-openings', name: 'JobOpeningManagement', component: () => import('@/pages/JobOpeningManagement.vue') },
	{ path: '/job-openings/:id', name: 'JobOpeningDetailView', component: () => import('@/pages/JobOpeningDetailView.vue') },
	{ alias: '/report', path: '/report', name: 'Report', component: () => import('@/pages/Report.vue') },
	{ alias: '/settings', path: '/settings', name: 'Settings', component: () => import('@/pages/Settings.vue') },
	{ path: '/:invalidpath', name: 'Invalid Page', component: () => import('@/pages/InvalidPage.vue') },
	{ path: '/my-actions', name: 'MyActions', component: () => import('@/pages/MyActions.vue') },

	// Talent Segment
	{ path: '/talent-segments', name: 'TalentSegments', component: TalentSegments },
	{ path: '/talent-segments/:id', name: 'TalentSegmentDetail', component: TalentSegmentDetailView },
	{ path: '/talent-segments/:id/detail', name: 'TalentSegmentDetailView', component: TalentSegmentDetailView },

	// Candidate
	{ path: '/candidates', name: 'CandidateManagement', component: CandidateManagement },
	{ path: '/candidates/:id', name: 'CandidateDetailView', component: CandidateDetailView },

	// Interaction & Action
	{ path: '/interactions', name: 'InteractionManagement', component: InteractionManagement },
	{ path: '/actions', name: 'ActionManagement', component: ActionManagement },

	// Email Log
	{ path: '/email-logs', name: 'EmailLogManagement', component: EmailLogManagement },

	// Data Sources
	{ path: '/data-sources', name: 'CandidateDataSourceManagement', component: CandidateDataSourceManagement },
	{ path: '/data-sources-direct', name: 'CandidateDataSourceManagementDirect', component: CandidateDataSourceManagementDirect },

	// Campaign Templates
	{ path: '/campaign-templates', name: 'CampaignTemplateManagement', component: () => import('@/pages/CampaignTemplateManagement.vue') },
	{ path: '/campaign-template/:id', name: 'CampaignTemplateDetail', component: () => import('@/pages/CampaignTemplateDetail.vue') },

	// Candidate Pool
	{ path: '/candidate-pools', name: 'CandidatePoolManagement', component: CandidatePoolManagement },

	

	// Email Editor
	{ path: '/email-editor', name: 'EmailEditor', component: EmailEditor },
	{ path: '/ladi-editor', name: 'LadiPageEditor', component: LadiPageEditor },
	{ path: '/ladi-view', name: 'LadiPageView', component: LadiPageView },
	{ path: '/applicant-pool', name: 'ApplicantPoolManagement', component: ApplicantPoolManagement },

	// LadiPage Management
	{ 
		path: '/ladi-pages', 
		name: 'ladi-pages',
		component: () => import('./pages/Ladi/LadiPageManagement.vue'),
		meta: {
			requiresAuth: true,
			title: 'Ladi Page Management'
		}
	},
	{ 
		path: '/ladi-pages/:id/edit', 
		name: 'ladi-page-editor',
		component: LadiPageEditor,
		meta: {
			requiresAuth: true,
			title: 'Ladi Page Editor'
		}
	},
	{ 
		path: '/ladi-pages/:id/view', 
		name: 'ladi-page-view',
		component: LadiPageView,
		meta: {
			requiresAuth: true,
			title: 'Ladi Page View' 
		}
	},

	// Public Route
	{ path: '/ladi/:slug', name: 'LadiPage', component: LadiPage, meta: { public: true } },
	{ path: '/register', name: 'RegisterPage', component: RegisterPage, meta: { public: true } },
	{ path: '/unsubscribe', name: 'UnSubscribePage', component: UnSubscribePage, meta: { public: true } },
	{ path: '/application', name: 'ApplicationPage', component: ApplicationPage, meta: { public: true } },
	//Connectors
	{
		path: '/connectors',
		name: 'Connectors',
		component: () => import('@/pages/APIIntegrationList.vue'),
		meta: {
			requiresAuth: true,
			title: 'External Social Management'
		}
	},
]


const scrollBehavior = (to, from, savedPosition) => {
	if (to.name === from.name) {
		to.meta?.scrollPos && (to.meta.scrollPos.top = 0)
		return { left: 0, top: 0 }
	}
	const scrollpos = to.meta?.scrollPos || { left: 0, top: 0 }

	if (scrollpos.top > 0) {
		setTimeout(() => {
			let el = document.querySelector("#list-rows")
			el?.scrollTo?.({
				top: scrollpos.top,
				left: scrollpos.left,
				behavior: "smooth",
			})
		}, 300)
	}
}

const router = createRouter({
	history: createWebHistory('/mbw_mira'),
	routes,
	scrollBehavior
})

router.beforeEach(async (to, from, next) => {
	const isPublicRoute = to.meta.public
	const { isLoggedIn } = sessionStore()

	if (!isPublicRoute && !isLoggedIn) {
		window.location.href = "/login?redirect-to=/mbw_mira/"
		return
	}

	if (isLoggedIn) {
		await userResource.promise
	}

	next()
})

export default router
