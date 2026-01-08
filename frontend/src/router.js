import { createRouter, createWebHistory } from 'vue-router'

import { userResource } from '@/stores/user'
import { sessionStore } from '@/stores/session'

// Talent Segment


const routes = [
	{ path: '/', name: 'Dashboard', component: () => import('@/pages/Dashboard.vue') },
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
	history: createWebHistory('/mbw_transition_hub'),
	routes,
	scrollBehavior
})

router.beforeEach(async (to, from, next) => {
	const isPublicRoute = to.meta.public
	const { isLoggedIn } = sessionStore()

	if (!isPublicRoute && !isLoggedIn) {
		window.location.href = "/login?redirect-to=/mbw_transition_hub"
		return
	}

	if (isLoggedIn) {
		await userResource.promise
	}

	next()
})

export default router
