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
							<FormControl v-model="filters.search" type="text" :placeholder="__('Search talent...')"
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

						<!-- Actions -->
						<div class="flex items-center justify-end space-x-3">
							<!-- Refresh Button -->
							<Button
								variant="outline"
								theme="gray"
								@click="handleRefresh"
								:loading="loading"
								class="flex items-center"
							>
								<template #prefix>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										class="h-4 w-4"
										:class="{ 'animate-spin': loading }"
										fill="none"
										viewBox="0 0 24 24"
										stroke="currentColor"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
										/>
									</svg>
								</template>
								{{ __('Refresh') }}
							</Button>

							<!-- Clear Filters -->
							<button v-if="hasFilters" @click="clearFilters"
								class="text-sm text-red-600 hover:text-red-800 font-medium px-3 py-2 rounded-lg hover:bg-red-50 transition-colors duration-200">
								{{ __('Clear Filters') }}
							</button>
						</div>
					</div>
				</div>
			</div>

			<!-- Loading State -->
			<Loading v-if="loading && candidatePools.length === 0" text="Loading talent..." />

			<!-- Content Views -->
			<div v-else>
				<!-- Table View -->
				<div class="bg-white rounded-lg border border-gray-200 overflow-hidden">
					<div class="overflow-x-auto">
						<table class="min-w-full divide-y divide-gray-200">
							<!-- Table Header -->
							<thead class="bg-gray-50">
	<tr>
		<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
			{{ __('Full Name') }}
		</th>
		<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
			{{ __('Contact Email') }}
		</th>
		<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
			{{ __('Contact Phone') }}
		</th>
		<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
			{{ __('Skills') }}
		</th>
		<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
			{{ __('Current Status') }}
		</th>
		<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
			{{ __('Actions') }}
		</th>
	</tr>
</thead>

<tbody class="bg-white divide-y divide-gray-200">
	<tr v-for="talent in candidatePools" :key="talent.name"
		class="hover:bg-gray-50 transition-colors duration-200 cursor-pointer"
		@click="openViewModal(talent)">
		
		<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
			{{ talent.full_name }}
		</td>
		<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
			{{ talent.contact_email }}
		</td>
		<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
			{{ talent.contact_phone }}
		</td>
		<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
			{{ talent.skills }}
		</td>
		<td class="px-6 py-4 whitespace-nowrap">
			<span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium"
				:class="getStatusClasses(talent.current_status)">
				{{ talent.current_status }}
			</span>
		</td>
		<td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
			<button
				class="inline-flex items-center justify-center w-8 h-8 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-full transition-colors duration-200"
				@click.stop="openViewModal(talent)" title="Xem chi tiết">
				<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
						d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
						d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
				</svg>
			</button>
		</td>
	</tr>
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
						{{ pagination.total }} {{ __('talent') }}
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
import { FormControl, Breadcrumbs, Avatar, Button } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Loading from '@/components/Loading.vue'
import CandidatePoolViewModal from '@/components/candidate-pool/CandidatePoolViewModal.vue'

const breadcrumbs = [{ label: __('Talent'), route: { name: 'Talent' } }]

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
const handleRefresh = async () => {
	try {
		await fetchCandidatePools()
		showSuccess(__('Data refreshed'))
	} catch (err) {
		showError(`Error refreshing data: ${err.message}`)
	}
}

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