<template>
	<div class="min-h-screen bg-gray-50">
		<LayoutHeader>
			<template #left-header>
				<Breadcrumbs :items="breadcrumbs" />
			</template>
		</LayoutHeader>

		<div class="candidate-pool-management-page container mx-auto w-full min-h-screen pt-10 bg-gray-50">

			<!-- Filters and Controls -->
			<div class="bg-white rounded-lg border border-gray-200 mb-6">
				<div class="p-4">
					<div class="grid grid-cols-1 md:grid-cols-6 gap-4 items-center">
						<!-- Search -->
						<div class="md:col-span-2">
							<FormControl v-model="filters.search" type="text" :placeholder="__('Search candidate pools...')"
								:prefix-icon="'search'" @input="debouncedSearch" />
						</div>

						<!-- Status Filter -->
						<div>
							<FormControl v-model="filters.status" type="select" :options="statusFilterOptions"
								@change="updateStatus(filters.status)" />
						</div>

						<!-- Statistics Display -->
						<div class="md:col-span-2 text-sm text-gray-600">
							<span v-if="stats.total">
								{{ __('Total') }}: {{ stats.total }} | 
								{{ __('Hired') }}: {{ stats.hired }} | 
								{{ __('Avg Score') }}: {{ stats.avg_evaluation_score }}
							</span>
						</div>

						<!-- Clear Filters -->
						<div class="flex justify-end">
							<button v-if="hasFilters" @click="clearFilters"
								class="text-sm text-red-600 hover:text-red-800 font-medium px-3 py-2 rounded-lg hover:bg-red-50 transition-colors duration-200">
								{{ __('Clear Filters') }}
							</button>
						</div>
					</div>
				</div>
			</div>

			<!-- Loading State -->
			<div v-if="loading && candidatePools.length === 0" class="text-center py-12">
				<div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-100 mb-4">
					<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
				</div>
				<p class="text-gray-600">{{ __('Loading candidate pools...') }}</p>
			</div>

			<!-- Content Views -->
			<div v-else>
				<!-- Table View -->
				<div class="bg-white rounded-lg border border-gray-200 overflow-hidden">
					<div class="overflow-x-auto">
						<table class="min-w-full divide-y divide-gray-200">
							<!-- Table Header -->
							<thead class="bg-gray-50">
								<tr>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										{{ __('Applicant') }}
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										{{ __('Status') }}
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										{{ __('Evaluation Score') }}
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										{{ __('Shortlist Date') }}
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										{{ __('Hired Date') }}
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										{{ __('Actions') }}
									</th>
								</tr>
							</thead>

							<!-- Table Body -->
							<tbody class="bg-white divide-y divide-gray-200">
								<!-- Loading State -->
								<template v-if="loading">
									<tr v-for="n in 10" :key="n" class="animate-pulse">
										<td class="px-6 py-4 whitespace-nowrap">
											<div class="flex items-center">
												<div class="w-10 h-10 bg-gray-300 rounded-full mr-4"></div>
												<div>
													<div class="h-4 bg-gray-300 rounded w-32 mb-2"></div>
													<div class="h-3 bg-gray-200 rounded w-24"></div>
												</div>
											</div>
										</td>
										<td class="px-6 py-4 whitespace-nowrap">
											<div class="h-6 bg-gray-200 rounded w-20"></div>
										</td>
										<td class="px-6 py-4 whitespace-nowrap">
											<div class="h-4 bg-gray-200 rounded w-16"></div>
										</td>
										<td class="px-6 py-4 whitespace-nowrap">
											<div class="h-4 bg-gray-200 rounded w-24"></div>
										</td>
										<td class="px-6 py-4 whitespace-nowrap">
											<div class="h-4 bg-gray-200 rounded w-24"></div>
										</td>
										<td class="px-6 py-4 whitespace-nowrap">
											<div class="w-8 h-8 bg-gray-200 rounded-full"></div>
										</td>
									</tr>
								</template>

								<!-- Candidate Pool Rows -->
								<template v-else-if="candidatePools.length > 0">
									<tr v-for="pool in candidatePools" :key="pool.name"
										class="hover:bg-gray-50 transition-colors duration-200 cursor-pointer"
										@click="openViewModal(pool)">
										<!-- Applicant Info -->
										<td class="px-6 py-4 whitespace-nowrap">
											<div class="flex items-center">
												<div class="flex-shrink-0 mr-4">
													<Avatar :shape="'circle'" :label="pool.avatarText" size="md" />
												</div>
												<div class="min-w-0 flex-1">
													<div class="text-sm font-medium text-gray-900 truncate">
														{{ pool.applicant_name || pool.applicant_id }}
													</div>
													<div class="text-sm text-gray-500 truncate">
														{{ pool.applicant_email || 'Chưa có email' }}
													</div>
													<div class="text-sm text-gray-500 truncate">
														{{ pool.applicant_position || 'Chưa có vị trí' }}
													</div>
												</div>
											</div>
										</td>

										<!-- Status -->
										<td class="px-6 py-4 whitespace-nowrap">
											<span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium"
												:class="getStatusClasses(pool.statusInfo.color)">
												{{ pool.statusInfo.text }}
											</span>
										</td>

										<!-- Evaluation Score -->
										<td class="px-6 py-4 whitespace-nowrap">
											<div class="flex items-center">
												<span class="text-sm font-medium text-gray-900 mr-2">
													{{ pool.evaluation_score ? pool.evaluation_score.toFixed(1) : '-' }}
												</span>
												<div v-if="pool.evaluation_score" class="w-16">
													<div class="w-full bg-gray-200 rounded-full h-1.5">
														<div class="h-1.5 rounded-full transition-all duration-300"
															:class="getScoreBarColor(pool.scoreColor)"
															:style="`width: ${Math.min(pool.evaluation_score, 100)}%`">
														</div>
													</div>
												</div>
											</div>
										</td>

										<!-- Shortlist Date -->
										<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
											{{ pool.formattedShortlistDate }}
										</td>

										<!-- Hired Date -->
										<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
											{{ pool.formattedHiredDate }}
										</td>

										<!-- Actions -->
										<td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
											<div class="flex items-center space-x-1">
												<button
													class="inline-flex items-center justify-center w-8 h-8 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-full transition-colors duration-200"
													@click.stop="openViewModal(pool)" title="Xem chi tiết">
													<svg class="w-4 h-4" fill="none" stroke="currentColor"
														viewBox="0 0 24 24">
														<path stroke-linecap="round" stroke-linejoin="round"
															stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
														<path stroke-linecap="round" stroke-linejoin="round"
															stroke-width="2"
															d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
													</svg>
												</button>
											</div>
										</td>
									</tr>
								</template>

								<!-- Empty State -->
								<template v-else>
									<tr>
										<td colspan="6" class="px-6 py-12 text-center">
											<div class="flex flex-col items-center justify-center">
												<svg class="w-16 h-16 text-gray-300 mb-4" fill="none"
													stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round"
														stroke-width="1"
														d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
												</svg>
												<h3 class="text-lg font-medium text-gray-900 mb-2">
													{{ hasFilters ? __('No candidate pools found') : __('No candidate pools found')
													}}
												</h3>
												<p class="text-sm text-gray-500 max-w-sm mb-6">
													{{ hasFilters
														? __('Try changing the filter to find suitable candidate pools.')
														: __('No candidate pools available.')
													}}
												</p>
												<button v-if="hasFilters"
													class="inline-flex items-center px-4 py-2 border border-gray-300 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-50 transition-colors"
													@click="clearFilters">
													{{ __('Clear Filters') }}
												</button>
											</div>
										</td>
									</tr>
								</template>
							</tbody>
						</table>
					</div>
				</div>

				<!-- Pagination -->
				<div v-if="pagination.total > 0"
					class="bg-white rounded-lg border border-gray-200 p-4 mt-6 flex items-center justify-between">
					<!-- Items per page selector -->
					<div class="flex items-center space-x-2">
						<span class="text-sm text-gray-700">{{ __('Items per page') }}:</span>
						<div class="w-20">
							<FormControl :model-value="pagination.limit" type="select" :options="itemsPerPageOptions"
								@change="changeItemsPerPage" />
						</div>
					</div>

					<!-- Page info -->
					<div class="text-sm text-gray-600">
						{{ __('Showing') }} {{ pagination.showing_from }} {{ __('to') }} {{ pagination.showing_to }} {{ __('of') }}
						{{ pagination.total }} {{ __('candidate pools') }}
					</div>

					<!-- Page navigation -->
					<div class="flex items-center space-x-1">
						<button :disabled="!pagination.has_prev" @click="goToPage(1)"
							class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed">
							<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
									d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
							</svg>
						</button>

						<button :disabled="!pagination.has_prev" @click="goToPage(pagination.page - 1)"
							class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed">
							<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
									d="M15 19l-7-7 7-7" />
							</svg>
						</button>

						<span class="mx-3 text-sm text-gray-700">
							{{ __('Page') }} {{ pagination.page }} / {{ pagination.pages }}
						</span>

						<button :disabled="!pagination.has_next" @click="goToPage(pagination.page + 1)"
							class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed">
							<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
									d="M9 5l7 7-7 7" />
							</svg>
						</button>

						<button :disabled="!pagination.has_next" @click="goToPage(pagination.pages)"
							class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed">
							<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
									d="M13 5l7 7-7 7M5 5l7 7-7 7" />
							</svg>
						</button>
					</div>
				</div>
			</div>

			<!-- View Modal -->
			<CandidatePoolViewModal v-model="viewModal.show" :candidatePool="viewModal.candidatePool" 
				:loading="viewModal.loading" :error="viewModal.error" />
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCandidatePool } from '@/composables/useCandidatePool'
import { useToast } from '@/composables/useToast'
import { FormControl, Breadcrumbs, Avatar } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import CandidatePoolViewModal from '@/components/candidate-pool/CandidatePoolViewModal.vue'

const breadcrumbs = [{ label: __('Candidate Pools'), route: { name: 'CandidatePoolManagement' } }]

// Router
const router = useRouter()

// Composables
const {
	candidatePools,
	loading,
	error,
	pagination,
	filters,
	filterOptions,
	stats,
	hasData,
	isEmpty,
	hasFilters,

	fetchCandidatePools,
	getCandidatePool,

	goToPage,
	changeItemsPerPage,
	updateSearch,
	updateStatus,
	clearFilters,

	initialize,
} = useCandidatePool()

const { showToast, showSuccess, showError } = useToast()

// Modal states
const viewModal = ref({
	show: false,
	candidatePool: null,
	loading: false,
	error: null,
})

// Computed
const statusFilterOptions = computed(() => [
	{ label: __('All Statuses'), value: '' },
	{ label: __('Shortlisted'), value: 'Shortlisted' },
	{ label: __('Offered'), value: 'Offered' },
	{ label: __('Hired'), value: 'Hired' },
	{ label: __('Rejected'), value: 'Rejected' }
])

const itemsPerPageOptions = [
	{ label: '12', value: 12 },
	{ label: '24', value: 24 },
	{ label: '36', value: 36 },
	{ label: '48', value: 48 },
]

// Helper methods
const getStatusClasses = (color) => {
	switch (color) {
		case 'success':
			return 'bg-green-50 text-green-700'
		case 'warning':
			return 'bg-yellow-50 text-yellow-700'
		case 'error':
			return 'bg-red-50 text-red-700'
		case 'info':
			return 'bg-blue-50 text-blue-700'
		default:
			return 'bg-gray-50 text-gray-700'
	}
}

const getScoreBarColor = (color) => {
	switch (color) {
		case 'green':
			return 'bg-green-500'
		case 'blue':
			return 'bg-blue-500'
		case 'yellow':
			return 'bg-yellow-500'
		case 'red':
			return 'bg-red-500'
		default:
			return 'bg-gray-500'
	}
}

// Methods
const openViewModal = async (pool) => {
	viewModal.value = {
		show: true,
		candidatePool: null,
		loading: true,
		error: null,
	}

	try {
		const candidatePool = await getCandidatePool(pool.name)
		if (candidatePool) {
			viewModal.value.candidatePool = candidatePool
		} else {
			viewModal.value.error = 'Không thể tải thông tin candidate pool'
		}
	} catch (err) {
		viewModal.value.error = err.message
		showError(`Error loading candidate pool: ${err.message}`)
	} finally {
		viewModal.value.loading = false
	}
}

// Debounced search
let searchTimeout = null
const debouncedSearch = () => {
	if (searchTimeout) {
		clearTimeout(searchTimeout)
	}

	searchTimeout = setTimeout(() => {
		updateSearch(filters.search)
	}, 500)
}

// Initialize on mount
onMounted(async () => {
	try {
		await initialize()
	} catch (err) {
		showError(`Error loading data: ${err.message}`)
	}
})
</script>

<style scoped>
/* Custom scrollbar */
.candidate-pool-management-page ::-webkit-scrollbar {
	width: 8px;
	height: 8px;
}

.candidate-pool-management-page ::-webkit-scrollbar-track {
	background: #f1f5f9;
	border-radius: 4px;
}

.candidate-pool-management-page ::-webkit-scrollbar-thumb {
	background: #cbd5e1;
	border-radius: 4px;
}

.candidate-pool-management-page ::-webkit-scrollbar-thumb:hover {
	background: #94a3b8;
}

/* Smooth transitions */
.candidate-pool-management-page button {
	transition: all 0.2s ease-in-out;
}

.candidate-pool-management-page input,
.candidate-pool-management-page select {
	transition: all 0.2s ease-in-out;
}

/* Loading animation */
@keyframes spin {
	from {
		transform: rotate(0deg);
	}

	to {
		transform: rotate(360deg);
	}
}

.animate-spin {
	animation: spin 1s linear infinite;
}
</style> 