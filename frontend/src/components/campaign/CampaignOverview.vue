<template>
	<div class="space-y-6">
		<!-- Tương tác Section - Compact horizontal layout -->
		<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
			<div class="flex items-center mb-6">
				<svg
					class="w-5 h-5 mr-2 text-blue-600"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
					/>
				</svg>
				<h3 class="text-base font-semibold text-gray-900">{{ __('Interactions') }}</h3>
			</div>

			<!-- Compact horizontal stats with dividers -->
			<div class="flex flex-wrap items-stretch divide-x divide-gray-200">
				<!-- Lượt gửi -->
				<div class="flex flex-col px-6 first:pl-0">
					<div class="text-xs text-gray-500 mb-1">{{ __('Sent') }}</div>
					<div class="text-2xl font-bold text-gray-900">{{ stats.sent }}</div>
				</div>

				<!-- Người nhận -->
				<div class="flex flex-col px-6">
					<div class="text-xs text-gray-500 mb-1">{{ __('Delivered') }}</div>
					<div class="text-2xl font-bold text-gray-900">
						{{ stats.delivered }}
						<span class="text-sm text-gray-500">({{ stats.deliveredPercent }})</span>
					</div>
				</div>

				<!-- Tỷ lệ mở (OR) -->
				<div class="flex flex-col px-6">
					<div class="text-xs text-gray-500 mb-1">{{ __('Open Rate (OR)') }}</div>
					<div class="text-2xl font-bold text-gray-900">
						{{ stats.openRate }}
						<span class="text-sm text-gray-500">({{ stats.openCount }})</span>
					</div>
				</div>

				<!-- Tỷ lệ click (CTR) -->
				<div class="flex flex-col px-6">
					<div class="text-xs text-gray-500 mb-1">{{ __('Click Rate (CTR)') }}</div>
					<div class="text-2xl font-bold text-gray-900">
						{{ stats.clickRate }}
						<span class="text-sm text-gray-500">({{ stats.clickCount }})</span>
					</div>
				</div>

				<!-- Tỷ lệ hủy đăng ký -->
				<div class="flex flex-col px-6">
					<div class="text-xs text-gray-500 mb-1">{{ __('Unsubscribe Rate') }}</div>
					<div class="text-2xl font-bold text-gray-900">
						{{ stats.unsubscribeRate }}
						<span class="text-sm text-gray-500">({{ stats.unsubscribeCount }})</span>
					</div>
				</div>

				<!-- Tỷ lệ tương tác lỗi -->
				<div class="flex flex-col px-6">
					<div class="text-xs text-gray-500 mb-1">{{ __('Error Rate') }}</div>
					<div class="text-2xl font-bold text-gray-900">
						{{ stats.errorRate }}
						<span class="text-sm text-gray-500">({{ stats.errorCount }})</span>
					</div>
				</div>

				<!-- Tỷ lệ trả lời -->
				<div class="flex flex-col px-6">
					<div class="text-xs text-gray-500 mb-1">{{ __('Reply Rate') }}</div>
					<div class="text-2xl font-bold text-gray-900">
						{{ stats.replyRate }}
						<span class="text-sm text-gray-500">({{ stats.replyCount }})</span>
					</div>
				</div>
			</div>
		</div>

		<!-- Grid 2 columns for Link Clicks and Top Talents -->
		<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
			<!-- Hoạt động click liên kết -->
			<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
				<div class="flex items-center mb-4">
					<svg
						class="w-5 h-5 mr-2 text-blue-600"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
						/>
					</svg>
					<h3 class="text-base font-semibold text-gray-900">
						{{ __('Link Click Activity') }}
					</h3>
				</div>

				<div class="text-sm text-gray-500 mb-3">
					{{ __('Track all links clicked in your emails.') }}
				</div>

				<!-- Link clicks table -->
				<div class="border rounded-lg overflow-hidden">
					<table class="min-w-full divide-y divide-gray-200">
						<thead class="bg-gray-50">
							<tr>
								<th
									class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase"
								>
									{{ __('Link Name') }}
								</th>
								<th
									class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase"
								>
									{{ __('Clicks') }}
								</th>
							</tr>
						</thead>
						<tbody class="bg-white divide-y divide-gray-200">
							<tr v-if="linkClicks.length === 0">
								<td colspan="2" class="px-4 py-8 text-center text-sm text-gray-500">
									{{ __('No link click data yet') }}
								</td>
							</tr>
							<tr
								v-else
								v-for="link in linkClicks"
								:key="link.url"
								class="hover:bg-gray-50"
							>
								<td class="px-4 py-3">
									<a
										:href="link.url"
										target="_blank"
										class="text-sm text-blue-600 hover:text-blue-800 hover:underline truncate block"
									>
										{{ link.url }}
									</a>
								</td>
								<td class="px-4 py-3 text-right text-sm text-gray-900">
									{{ link.clicks }}
								</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>

			<!-- Top talent mở tin nhắn -->
			<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
				<div class="flex items-center mb-4">
					<svg
						class="w-5 h-5 mr-2 text-blue-600"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"
						/>
					</svg>
					<h3 class="text-base font-semibold text-gray-900">
						{{ __('Top Engaged Talents') }}
					</h3>
				</div>

				<div class="text-sm text-gray-500 mb-3">
					{{ __('List of recipients with the highest engagement with your messages.') }}
				</div>

				<!-- Top talents table -->
				<div class="border rounded-lg overflow-hidden">
					<table class="min-w-full divide-y divide-gray-200">
						<thead class="bg-gray-50">
							<tr>
								<th
									class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase"
								>
									{{ __('Talent') }}
								</th>
								<th
									class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase"
								>
									{{ __('Clicks') }}
								</th>
							</tr>
						</thead>
						<tbody class="bg-white divide-y divide-gray-200">
							<tr v-if="topTalents.length === 0">
								<td colspan="2" class="px-4 py-8 text-center text-sm text-gray-500">
									{{ __('No interaction data yet') }}
								</td>
							</tr>
							<tr
								v-else
								v-for="talent in topTalents"
								:key="talent.id"
								class="hover:bg-gray-50"
							>
								<td class="px-4 py-3">
									<div class="text-sm font-medium text-gray-900">
										{{ talent.name }}
									</div>
									<div class="text-xs text-gray-500">{{ talent.email }}</div>
								</td>
								<td class="px-4 py-3 text-right text-sm text-gray-900">
									{{ talent.clicks }}
								</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { call } from 'frappe-ui'

const props = defineProps({
	campaignId: {
		type: String,
		required: true,
	},
})

// Loading states
const loadingStats = ref(false)
const loadingLinkClicks = ref(false)
const loadingTopTalents = ref(false)

// Stats data from API
const stats = ref({
	sent: 0,
	delivered: 0,
	deliveredPercent: '0%',
	openRate: '0%',
	openCount: 0,
	clickRate: '0%',
	clickCount: 0,
	unsubscribeRate: '0%',
	unsubscribeCount: 0,
	errorRate: '0%',
	errorCount: 0,
	replyRate: '0%',
	replyCount: 0,
})

const linkClicks = ref([])
const topTalents = ref([])

// Load campaign statistics from API
const loadStats = async () => {
	if (!props.campaignId) return
	
	loadingStats.value = true
	try {
		const response = await call('mbw_mira.api.interaction.get_campaign_stats', {
			campaign_id: props.campaignId
		})
		
		if (response.status === 'success' && response.stats) {
			const s = response.stats
			stats.value = {
				sent: s.sent || 0,
				delivered: s.delivered || 0,
				deliveredPercent: s.delivered_percent || '0%',
				openRate: s.open_rate || '0%',
				openCount: s.open_count || 0,
				clickRate: s.click_rate || '0%',
				clickCount: s.click_count || 0,
				unsubscribeRate: s.unsubscribe_rate || '0%',
				unsubscribeCount: s.unsubscribe_count || 0,
				errorRate: s.error_rate || '0%',
				errorCount: s.error_count || 0,
				replyRate: s.reply_rate || '0%',
				replyCount: s.reply_count || 0,
			}
		}
	} catch (error) {
		console.error('Error loading campaign stats:', error)
	} finally {
		loadingStats.value = false
	}
}

// Load link click data from API
const loadLinkClicks = async () => {
	if (!props.campaignId) return
	
	loadingLinkClicks.value = true
	try {
		const response = await call('mbw_mira.api.interaction.get_campaign_link_clicks', {
			campaign_id: props.campaignId,
			limit: 20
		})
		
		if (response.status === 'success') {
			linkClicks.value = response.link_clicks || []
		}
	} catch (error) {
		console.error('Error loading link clicks:', error)
	} finally {
		loadingLinkClicks.value = false
	}
}

// Load top talents from API
const loadTopTalents = async () => {
	if (!props.campaignId) return
	
	loadingTopTalents.value = true
	try {
		const response = await call('mbw_mira.api.interaction.get_campaign_top_talents', {
			campaign_id: props.campaignId,
			limit: 10
		})
		
		if (response.status === 'success') {
			topTalents.value = (response.top_talents || []).map(talent => ({
				id: talent.talent_id,
				name: talent.full_name || talent.email || talent.talent_id,
				email: talent.email || '',
				clicks: talent.clicks || 0,
				opens: talent.opens || 0,
				replies: talent.replies || 0,
				total: talent.total_interactions || 0
			}))
		}
	} catch (error) {
		console.error('Error loading top talents:', error)
	} finally {
		loadingTopTalents.value = false
	}
}

// Load all data
const loadAllData = () => {
	loadStats()
	loadLinkClicks()
	loadTopTalents()
}

// Watch for campaignId changes
watch(() => props.campaignId, (newId) => {
	if (newId) {
		loadAllData()
	}
}, { immediate: false })

onMounted(() => {
	loadAllData()
})
</script>
