import { createRouter, createWebHistory } from 'vue-router'

import { userResource } from '@/stores/user'
import { sessionStore } from '@/stores/session'

// Talent Segment


const routes = [
	{ path: '/', name: 'Dashboard', component: () => import('@/pages/Dashboard.vue') },
	{ alias: '/talentsegment', path: '/talentsegment', name: 'Talet Segment', component: () => import('@/pages/TalentSegment.vue') },
	{ alias: '/candidate', path: '/candidate', name: 'Candidate', component: () => import('@/pages/Candidate.vue') },
	{ alias: '/campaigns', path: '/campaigns', name: 'CampaignManagement', component: import('@/pages/CampaignManagement.vue') },
	{ path: '/campaigns/:id', name: 'CampaignDetailView', component: import('@/pages/CampaignDetailView.vue') },
	{ path: '/job-openings', name: 'JobOpeningManagement', component: () => import('@/pages/JobOpeningManagement.vue') },
	{ path: '/job-openings/:id', name: 'JobOpeningDetailView', component: () => import('@/pages/JobOpeningDetailView.vue') },
	{ path: '/candidates-simple', name: 'CandidateManagementSimple', component: () => import('@/pages/CandidateManagementSimple.vue') },
	{ path: '/candidates-simple/:id', name: 'CandidateDetailSimpleView', component: () => import('@/pages/CandidateDetailSimpleView.vue') },
	{ alias: '/report', path: '/report', name: 'Report', component: () => import('@/pages/Report.vue') },
	{ alias: '/settings', path: '/settings', name: 'Settings', component: () => import('@/pages/Settings.vue') },
	{ path: '/:invalidpath', name: 'Invalid Page', component: () => import('@/pages/InvalidPage.vue') },
	{ path: '/my-actions', name: 'MyActions', component: () => import('@/pages/MyActions.vue') },

	// Talent Segment
	{ path: '/talent-segments', name: 'TalentSegments', component: ()=>import('@/pages/TalentSegmentManagement.vue') },
	{ path: '/talent-segments/:id', name: 'TalentSegmentDetail', component: () =>import('@/pages/TalentSegmentDetailView.vue') },
	{ path: '/talent-segments/:id/detail', name: 'TalentSegmentDetailView', component: () =>import('@/pages/TalentSegmentDetailView.vue') },

	// Candidate
	{ path: '/candidates', name: 'CandidateManagement', component: ()=> import('@/pages/CandidateManagement.vue') },
	{ path: '/candidates/:id', name: 'CandidateDetailView', component: () => import('@/pages/CandidateDetailView.vue') },

	// Mira Interaction & Action
	{ path: '/interactions', name: 'InteractionManagement', component: ()=>import('@/pages/InteractionManagement.vue') },
	{ path: '/actions', name: 'ActionManagement', component: () =>import('@/pages/ActionManagement.vue') },

	// Email Log
	{ path: '/email-logs', name: 'EmailLogManagement', component: ()=>import('@/pages/EmailLogManagement.vue') },

	// Data Sources
	{ path: '/data-sources', name: 'CandidateDataSourceManagement', component: ()=>import('@/pages/CandidateDataSourceManagement.vue') },
	{ path: '/data-sources-direct', name: 'CandidateDataSourceManagementDirect', component: ()=>import('@/pages/CandidateDataSourceManagementDirect.vue') },

	// Campaign Templates
	{ path: '/campaign-templates', name: 'CampaignTemplateManagement', component: () => import('@/pages/CampaignTemplateManagement.vue') },
	{ path: '/campaign-template/:id', name: 'CampaignTemplateDetail', component: () => import('@/pages/CampaignTemplateDetail.vue') },

	// Candidate Pool
	{ path: '/candidate-pools', name: 'CandidatePoolManagement', component: ()=>import('@/pages/CandidatePoolManagement.vue') },

	

	// Email Editor
	{ path: '/email-editor', name: 'EmailEditor', component: ()=>import('@/pages/EmailEditor.vue') },
	{ path: '/ladi-editor', name: 'LadiPageEditor', component: ()=>import('@/pages/LadiPageEditor.vue') },
	{ path: '/ladi-view', name: 'LadiPageView', component: ()=>import('@/pages/LadiPageView.vue') },
	{ path: '/applicant-pool', name: 'ApplicantPoolManagement', component: ()=>import('@/pages/ApplicantPoolManagement.vue') },

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
		component: ()=>import('@/pages/LadiPageEditor.vue'),
		meta: {
			requiresAuth: true,
			title: 'Ladi Page Editor'
		}
	},
	{ 
		path: '/ladi-pages/:id/view', 
		name: 'ladi-page-view',
		component: ()=>import('@/pages/LadiPageView.vue'),
		meta: {
			requiresAuth: true,
			title: 'Ladi Page View' 
		}
	},

	// Public Route
	{ path: '/ladi/:slug', name: 'LadiPage', component: ()=>import('@/pages/Public/LadiPage.vue'), meta: { public: true } },
	{ path: '/register', name: 'RegisterPage', component: ()=>import('@/pages/Public/RegisterPage.vue'), meta: { public: true } },
	{ path: '/unsubscribe', name: 'UnSubscribePage', component: ()=>import('@/pages/Public/UnSubscribePage.vue'), meta: { public: true } },
	{ path: '/application', name: 'ApplicationPage', component: ()=>import('@/pages/Public/ApplicationPage.vue'), meta: { public: true } },
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
