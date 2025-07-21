<template>
	<div class="min-h-screen bg-gray-50">
		<LayoutHeader>
			<template #left-header>
				<Breadcrumbs :items="breadcrumbs" />
			</template>
			<template #right-header>
				<div class="flex items-center">
						<Button variant="solid" theme="gray" @click="openCreateModal" :loading="loading"
							class="">
							<template #prefix>
								<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
									stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
										d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
								</svg>
							</template>
							{{ __('Add Talent Pool') }}
						</Button>
					</div>
			</template>
		</LayoutHeader>

		<div class="candidate-management-page container mx-auto w-full min-h-screen pt-10 bg-gray-50">

			<!-- Header Section -->
			<!-- <div class="bg-white rounded-lg border border-gray-200 p-6 mb-6">
				<div class="flex items-center justify-between">
					<div>
						<h1 class="text-3xl font-bold text-black mb-2 flex items-center">
							<svg class="w-8 h-8 mr-3" fill="currentColor" viewBox="0 0 20 20">
								<path
									d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z" />
							</svg>
							{{ __('Candidate Management') }}
						</h1>
						<p class="text-gray-600 mb-0">
							{{ __('Manage and track candidate information in the system') }}
						</p>
					</div>

					
				</div>
			</div> -->

			<!-- Filters and Controls -->
			<div class="bg-white rounded-lg border border-gray-200 mb-6">
				<div class="p-4">
					<div class="flex flex-col lg:flex-row gap-4 items-start lg:items-center">
						<!-- Left side: Filters -->
						<div class="flex flex-col sm:flex-row gap-4 flex-1 min-w-0">
							<!-- Search -->
							<div class="flex-1 min-w-0 sm:max-w-xs">
								<FormControl v-model="filters.search" type="text" :placeholder="__('Search pools...')"
									:prefix-icon="'search'" @input="debouncedSearch" />
							</div>

							<!-- Status Filter -->
							<div class="sm:w-40">
								<FormControl v-model="filters.status" type="select" :options="statusFilterOptions"
									@change="updateStatus(filters.status)" />
							</div>

							<!-- Source Filter -->
							<div class="sm:w-48">
								<FormControl v-model="filters.source" type="select" :options="sourceFilterOptions"
									@change="updateSource(filters.source)" />
							</div>
						</div>

						<!-- Right side: Action buttons -->
						<div class="flex flex-col sm:flex-row gap-2 items-start sm:items-center">
							<!-- Import/Export/Refresh Buttons -->
							<div class="flex flex-wrap items-center gap-2">
								<Button
									variant="outline"
									theme="blue"
									@click="handleImport"
									:title="__('Import Candidates')"
								>
									<template #prefix>
										<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
										</svg>
									</template>
									{{ __('Import') }}
								</Button>
								<Button
									variant="outline"
									theme="green"
									@click="handleExport"
									:title="__('Export Candidates')"
								>
									<template #prefix>
										<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
										</svg>
									</template>
									{{ __('Export') }}
								</Button>
								<Button
									variant="outline"
									theme="gray"
									@click="handleRefresh"
									:loading="loading"
									:title="__('Refresh Data')"
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
							</div>

							<!-- Clear Filters -->
							<div v-if="hasFilters">
								<button @click="clearFilters"
									class="text-sm text-red-600 hover:text-red-800 font-medium px-3 py-2 rounded-lg hover:bg-red-50 transition-colors duration-200">
									{{ __('Clear Filters') }}
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Loading State -->
			<div v-if="loading && candidates.length === 0" class="text-center py-12">
				<div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-100 mb-4">
					<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
				</div>
				<p class="text-gray-600">{{ __('Loading candidate list...') }}</p>
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
										{{ __('Talent Pool') }}
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										{{ __('Contact Info') }}
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										{{ __('Skills') }}
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										{{ __('Status') }}
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										{{ __('Engagement Score') }}
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
											<div class="h-4 bg-gray-200 rounded w-48 mb-2"></div>
											<div class="h-3 bg-gray-200 rounded w-32"></div>
										</td>
										<td class="px-6 py-4 whitespace-nowrap">
											<div class="flex space-x-1">
												<div class="h-6 bg-gray-200 rounded w-16"></div>
												<div class="h-6 bg-gray-200 rounded w-20"></div>
											</div>
										</td>
										<td class="px-6 py-4 whitespace-nowrap">
											<div class="h-6 bg-gray-200 rounded w-20"></div>
										</td>
										<td class="px-6 py-4 whitespace-nowrap">
											<div class="h-4 bg-gray-200 rounded w-16"></div>
										</td>
										<td class="px-6 py-4 whitespace-nowrap">
											<div class="flex items-center space-x-1">
												<div class="w-8 h-8 bg-gray-200 rounded-full"></div>
												<div class="w-8 h-8 bg-gray-200 rounded-full"></div>
												<div class="w-8 h-8 bg-gray-200 rounded-full"></div>
											</div>
										</td>
									</tr>
								</template>

								<!-- Candidate Rows -->
								<template v-else-if="candidates.length > 0">
									<tr v-for="candidate in candidates" :key="candidate.name"
										class="hover:bg-gray-50 transition-colors duration-200 cursor-pointer"
										@click="openViewModal(candidate)">
										<!-- Candidate Info -->
										<td class="px-6 py-4 whitespace-nowrap">
											<div class="flex items-center">
												<div class="flex-shrink-0 mr-4">
													<Avatar :shape="'circle'" :image="candidate.avatar"
														:label="getAvatarText(candidate.full_name)" size="md" />
												</div>
												<div class="min-w-0 flex-1">
													<div class="text-sm font-medium text-gray-900 truncate">
														{{ candidate.full_name }}
													</div>
													<div class="text-sm text-gray-500 truncate">
														{{ candidate.headline || 'Chưa có thông tin' }}
													</div>
												</div>
											</div>
										</td>

										<!-- Contact Info -->
										<td class="px-6 py-4 whitespace-nowrap">
											<div class="text-sm text-gray-900 truncate">
												{{ candidate.email }}
											</div>
											<!-- Đã bỏ dòng location vì không còn trường này trong TalentProfiles -->
										</td>

										<!-- Skills -->
										<td class="px-6 py-4 whitespace-nowrap">
											<div class="flex flex-wrap gap-1 max-w-xs">
												<span v-for="skill in getTopSkills(candidate.skills, 2)" :key="skill"
													class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200">
													{{ skill }}
												</span>
												<span v-if="processSkills(candidate.skills).length > 2"
													class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-600 border border-gray-200">
													+{{ processSkills(candidate.skills).length - 2 }}
												</span>
											</div>
										</td>

										<!-- Status -->
										<td class="px-6 py-4 whitespace-nowrap">
											<span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium"
												:class="getStatusClasses(candidate.status)">
												{{ formatCandidateStatus(candidate.status).text }}
											</span>
										</td>

										<!-- Engagement Score -->
										<td class="px-6 py-4 whitespace-nowrap">
											<div class="flex items-center">
												<div class="w-16 mr-2">
													<div class="w-full bg-gray-200 rounded-full h-1.5">
														<div class="h-1.5 rounded-full transition-all duration-300"
															:class="getEngagementBarColor(calculateEngagementScore(candidate))"
															:style="`width: ${calculateEngagementScore(candidate)}%`">
														</div>
													</div>
												</div>
												<span class="text-xs font-medium text-gray-700">
													{{ calculateEngagementScore(candidate) }}%
												</span>
											</div>
										</td>

										<!-- Actions -->
										<td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
											<div class="flex items-center space-x-1">
												<button
													class="inline-flex items-center justify-center w-8 h-8 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-full transition-colors duration-200"
													@click.stop="openViewModal(candidate)" title="Xem chi tiết">
													<svg class="w-4 h-4" fill="none" stroke="currentColor"
														viewBox="0 0 24 24">
														<path stroke-linecap="round" stroke-linejoin="round"
															stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
														<path stroke-linecap="round" stroke-linejoin="round"
															stroke-width="2"
															d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
													</svg>
												</button>
												<button
													class="inline-flex items-center justify-center w-8 h-8 text-gray-600 hover:text-gray-800 hover:bg-gray-50 rounded-full transition-colors duration-200"
													@click.stop="openEditModal(candidate)" title="Chỉnh sửa">
													<svg class="w-4 h-4" fill="none" stroke="currentColor"
														viewBox="0 0 24 24">
														<path stroke-linecap="round" stroke-linejoin="round"
															stroke-width="2"
															d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
													</svg>
												</button>
												<button
													class="inline-flex items-center justify-center w-8 h-8 text-red-600 hover:text-red-800 hover:bg-red-50 rounded-full transition-colors duration-200"
													@click.stop="handleDeleteCandidate(candidate)" title="Xóa ứng viên">
													<svg class="w-4 h-4" fill="none" stroke="currentColor"
														viewBox="0 0 24 24">
														<path stroke-linecap="round" stroke-linejoin="round"
															stroke-width="2"
															d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
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
													{{ hasFilters ? __('No talent pool found') : __('No talent pool found')
													}}
												</h3>
												<p class="text-sm text-gray-500 max-w-sm mb-6">
													{{ hasFilters
														? __('Try changing the filter to find a suitable talent pool.')
														: __('Start by adding the first talent pool.')
													}}
												</p>
												<button v-if="!hasFilters"
													class="inline-flex items-center px-4 py-2 bg-black text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors"
													@click="openCreateModal">
													<svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor"
														viewBox="0 0 24 24">
														<path stroke-linecap="round" stroke-linejoin="round"
															stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
													</svg>
													{{ __('Add Talent Pool') }}
												</button>
												<button v-else
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
						<span class="text-sm text-gray-700">Số items mỗi trang:</span>
						<div class="w-20">
							<FormControl :model-value="pagination.limit" type="select" :options="itemsPerPageOptions"
								@change="changeItemsPerPage" />
						</div>
					</div>

					<!-- Page info -->
					<div class="text-sm text-gray-600">
						Hiển thị {{ pagination.showing_from }} đến {{ pagination.showing_to }} trong
						tổng số {{ pagination.total }} ứng viên
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
							Trang {{ pagination.page }} / {{ pagination.pages }}
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
			<CandidateViewModal v-model="viewModal.show" :candidate="viewModal.candidate" :loading="viewModal.loading"
				:error="viewModal.error" @edit-candidate="openEditModal" @delete-candidate="handleDeleteCandidate"
				@duplicate-candidate="handleDuplicateCandidate" />

			<!-- Edit Modal -->
			<CandidateEditModal v-model="editModal.show" :candidate="editModal.candidate" :loading="editModal.loading"
				:saving="editModal.saving" :filter-options="filterOptions || {}" @save-candidate="handleSaveCandidate"
				@cancel="editModal.show = false" />

			<!-- Delete Confirmation Dialog -->
			<div v-if="deleteDialog.show"
				class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center">
				<div class="bg-white rounded-lg max-w-md w-full mx-4">
					<div class="p-6">
						<div class="flex items-center mb-4">
							<div class="flex-shrink-0">
								<svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
										d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
								</svg>
							</div>
							<div class="ml-3">
								<h3 class="text-lg font-medium text-gray-900">Xác nhận xóa</h3>
							</div>
						</div>

						<div class="mb-4">
							<p class="text-sm text-gray-500 mb-3">
								Bạn có chắc chắn muốn xóa ứng viên này không?
							</p>
							<div class="bg-gray-50 p-3 rounded-lg">
								<div class="font-medium text-gray-900">
									{{ deleteDialog.candidate?.full_name }}
								</div>
								<div class="text-sm text-gray-500">
									{{ deleteDialog.candidate?.email }}
								</div>
							</div>
							<p class="text-xs text-red-600 mt-2">Hành động này không thể hoàn tác.</p>
						</div>

						<div class="flex justify-end space-x-3">
							<button @click="deleteDialog.show = false" :disabled="deleteDialog.loading"
								class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50">
								Hủy
							</button>
							<button @click="confirmDelete" :disabled="deleteDialog.loading"
								class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 flex items-center">
								<span v-if="deleteDialog.loading"
									class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
								Xóa
							</button>
						</div>
					</div>
				</div>
			</div>

			<!-- Toast notifications handled by ToastContainer -->
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useCandidate } from '@/composables/useCandidate'
import { useToast } from '@/composables/useToast'
import { FormControl, Breadcrumbs, Button } from 'frappe-ui'
import { CandidateViewModal, CandidateEditModal } from '@/components/candidate'
import { Avatar } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'



import {
	calculateEngagementScore,
	formatCandidateStatus,
	getAvatarText,
	processSkills
} from '@/services/candidateService'

const breadcrumbs = [{ label: __('Talent Pools'), route: { name: 'CandidateManagement' } }]

// Router
const router = useRouter()


// Composables
const {
	candidates,
	loading,
	error,
	pagination,
	filters,
	filterOptions,
	stats,
	hasData,
	isEmpty,

	fetchCandidates,
	getCandidate,
	createCandidate,
	updateCandidate,
	deleteCandidate,

	goToPage,
	changeItemsPerPage,
	updateSearch,
	updateStatus,
	updateSource,
	updateSkills,
	clearFilters,

	initialize,
} = useCandidate()

const { showToast, showSuccess, showError } = useToast()

// Debug logs removed

// Local state (removed currentView since we only have card view)

// Modal states
const viewModal = ref({
	show: false,
	candidate: null,
	loading: false,
	error: null,
})

const editModal = ref({
	show: false,
	candidate: null,
	loading: false,
	saving: false,
})

const deleteDialog = ref({
	show: false,
	candidate: null,
	loading: false,
})

// Removed snackbar state - using useToast instead

// Computed
const hasCandidates = computed(() => hasData.value)
const hasFilters = computed(() => {
	return (
		filters.search ||
		filters.status ||
		filters.source ||
		(filters.skills && filters.skills.length > 0)
	)
})

// Filter Options
const statusFilterOptions = computed(() => [
	{ label: __('All Statuses'), value: '' },
	{ label: 'NEW', value: 'NEW' },
	{ label: 'SOURCED', value: 'SOURCED' },
	{ label: 'NURTURING', value: 'NURTURING' },
	{ label: 'ENGAGED', value: 'ENGAGED' },
	{ label: 'ARCHIVED', value: 'ARCHIVED' }
])

const sourceFilterOptions = computed(() => [
	{ label: __('All Sources'), value: '' },
	{ label: __('Manual'), value: 'Manual' },
	{ label: __('LinkedIn'), value: 'LinkedIn' },
	{ label: __('Email'), value: 'Email' },
	{ label: __('Referral'), value: 'Referral' },
	{ label: __('ATS Import'), value: 'ATS Import' },
	{ label: __('Website'), value: 'Website' }
])

const skillFilterOptions = computed(() => {
	return [
		// Programming Languages
		{ label: 'JavaScript', value: 'javascript' },
		{ label: 'TypeScript', value: 'typescript' },
		{ label: 'Python', value: 'python' },
		{ label: 'Java', value: 'java' },
		{ label: 'C#', value: 'csharp' },
		{ label: 'C++', value: 'cpp' },
		{ label: 'PHP', value: 'php' },
		{ label: 'Go', value: 'go' },
		{ label: 'Rust', value: 'rust' },
		{ label: 'Ruby', value: 'ruby' },
		{ label: 'Swift', value: 'swift' },
		{ label: 'Kotlin', value: 'kotlin' },

		// Frontend Frameworks
		{ label: 'React', value: 'react' },
		{ label: 'Vue.js', value: 'vuejs' },
		{ label: 'Angular', value: 'angular' },
		{ label: 'Next.js', value: 'nextjs' },
		{ label: 'Nuxt.js', value: 'nuxtjs' },
		{ label: 'Svelte', value: 'svelte' },

		// Backend Frameworks
		{ label: 'Node.js', value: 'nodejs' },
		{ label: 'Express.js', value: 'expressjs' },
		{ label: 'Django', value: 'django' },
		{ label: 'Flask', value: 'flask' },
		{ label: 'Spring Boot', value: 'springboot' },
		{ label: 'Laravel', value: 'laravel' },
		{ label: 'ASP.NET', value: 'aspnet' },
		{ label: 'FastAPI', value: 'fastapi' },

		// Databases
		{ label: 'MySQL', value: 'mysql' },
		{ label: 'PostgreSQL', value: 'postgresql' },
		{ label: 'MongoDB', value: 'mongodb' },
		{ label: 'Redis', value: 'redis' },
		{ label: 'SQLite', value: 'sqlite' },
		{ label: 'Oracle', value: 'oracle' },
		{ label: 'SQL Server', value: 'sqlserver' },

		// Cloud & DevOps
		{ label: 'AWS', value: 'aws' },
		{ label: 'Azure', value: 'azure' },
		{ label: 'Google Cloud', value: 'gcp' },
		{ label: 'Docker', value: 'docker' },
		{ label: 'Kubernetes', value: 'kubernetes' },
		{ label: 'Jenkins', value: 'jenkins' },
		{ label: 'CI/CD', value: 'cicd' },
		{ label: 'Terraform', value: 'terraform' },

		// Tools & Technologies
		{ label: 'Git', value: 'git' },
		{ label: 'Linux', value: 'linux' },
		{ label: 'Agile', value: 'agile' },
		{ label: 'Scrum', value: 'scrum' },
		{ label: 'REST API', value: 'restapi' },
		{ label: 'GraphQL', value: 'graphql' },
		{ label: 'Microservices', value: 'microservices' },
		{ label: 'Machine Learning', value: 'ml' },
		{ label: 'Data Science', value: 'datascience' },
		{ label: 'AI', value: 'ai' },
	]
})

const itemsPerPageOptions = [
	{ label: '12', value: 12 },
	{ label: '24', value: 24 },
	{ label: '36', value: 36 },
	{ label: '48', value: 48 },
]

// Helper methods for candidate list display
const getTopSkills = (skills, limit) => {
	if (!skills) return []
	
	// Handle JSON skills from TalentPool
	let skillsArray = []
	if (typeof skills === 'string') {
		try {
			skillsArray = JSON.parse(skills)
		} catch (e) {
			skillsArray = skills.split(',').map(s => s.trim()).filter(s => s)
		}
	} else if (Array.isArray(skills)) {
		skillsArray = skills
	} else if (typeof skills === 'object' && skills !== null) {
		skillsArray = Object.values(skills)
	}
	
	return skillsArray.slice(0, limit || 3)
}

const getStatusClasses = (status) => {
	const statusConfig = formatCandidateStatus(status)

	switch (statusConfig.color) {
		case 'success':
			return 'bg-green-50 text-green-700'
		case 'warning':
			return 'bg-yellow-50 text-yellow-700'
		case 'error':
			return 'bg-red-50 text-red-700'
		case 'info':
			return 'bg-blue-50 text-blue-700'
		case 'purple':
			return 'bg-purple-50 text-purple-700'
		default:
			return 'bg-gray-50 text-gray-700'
	}
}

const getEngagementBarColor = (score) => {
	if (score >= 80) return 'bg-green-500'
	if (score >= 60) return 'bg-blue-500'
	if (score >= 40) return 'bg-yellow-500'
	if (score >= 20) return 'bg-orange-500'
	return 'bg-red-500'
}

// Methods - removed showSnackbar, using useToast instead

const openCreateModal = () => {
	editModal.value = {
		show: true,
		candidate: null,
		loading: false,
		saving: false,
	}
}

const openViewModal = (candidate) => {
	// Navigate to candidate detail view instead of opening modal
	router.push(`/candidates/${candidate.name}`)
}

const openEditModal = (candidate) => {
	editModal.value = {
		show: true,
		candidate: candidate,
		loading: false,
		saving: false,
	}
}

const handleDeleteCandidate = (candidate) => {
	deleteDialog.value = {
		show: true,
		candidate: candidate,
		loading: false,
	}
}

// Prevent double delete
let isDeleting = false

const confirmDelete = async () => {
	// Prevent double delete
	if (isDeleting) {
		console.log('Already deleting, ignoring duplicate call')
		return
	}

	try {
		isDeleting = true
		deleteDialog.value.loading = true
		await deleteCandidate(deleteDialog.value.candidate.name)

		deleteDialog.value.show = false
		viewModal.value.show = false

		showSuccess('Candidate deleted successfully')
	} catch (err) {
		showError(`Error deleting candidate: ${err.message}`)
	} finally {
		deleteDialog.value.loading = false
		isDeleting = false
	}
}

// Prevent double save
let isSaving = false

const handleSaveCandidate = async (candidateData) => {
	console.log('handleSaveCandidate called with:', candidateData)

	// Prevent double save
	if (isSaving) {
		console.log('Already saving, ignoring duplicate call')
		return
	}

	try {
		isSaving = true
		editModal.value.saving = true
		console.log('Setting saving to true')
		console.log(editModal.value.candidate)

		if (editModal.value.candidate) {
			// Update existing candidate
			console.log('Updating candidate:', editModal.value.candidate.name)
			await updateCandidate(editModal.value.candidate.name, candidateData)
			showSuccess('Candidate updated successfully')
		} else {
			// Create new candidate
			console.log('Creating new candidate')
			await createCandidate(candidateData)
			showSuccess('New candidate created successfully')
		}

		console.log('Closing modal')
		editModal.value.show = false
	} catch (err) {
		console.error('Error in handleSaveCandidate:', err)
		showError(`Error saving candidate: ${err.message}`)
	} finally {
		console.log('Setting saving to false')
		editModal.value.saving = false
		isSaving = false
	}
}

const handleDuplicateCandidate = (candidate) => {
	// Create a copy without the unique fields
	const duplicateData = {
		...candidate,
		full_name: `${candidate.full_name} (Copy)`,
		email: `copy_${Date.now()}_${candidate.email}`,
		name: undefined, // Let system generate new name
	}

	editModal.value = {
		show: true,
		candidate: duplicateData,
		loading: false,
		saving: false,
	}
}

// Removed export function since we don't have table view

// Import/Export functions
const handleImport = () => {
	// Create file input element
	const input = document.createElement('input')
	input.type = 'file'
	input.accept = '.csv,.xlsx,.xls'
	input.style.display = 'none'

	input.onchange = (event) => {
		const file = event.target.files[0]
		if (file) {
			// TODO: Implement actual import logic
			showError('Import functionality is under development')
			console.log('Selected file for import:', file.name)
		}
	}

	document.body.appendChild(input)
	input.click()
	document.body.removeChild(input)
}

const handleExport = () => {
	try {
		// TODO: Implement actual export logic
		// For now, just show a message
		showError('Export functionality is under development')
		console.log('Export candidates requested')

		// Sample CSV export structure (commented out until actual implementation)
		/*
		const csvHeaders = ['Họ tên', 'Email', 'Điện thoại', 'Kỹ năng', 'Trạng thái', 'Nguồn']
		const csvData = candidates.value.map(candidate => [
			candidate.full_name,
			candidate.email,
			candidate.phone,
			candidate.skills?.join('; ') || '',
			candidate.status,
			candidate.source
		])
		
		const csvContent = [csvHeaders, ...csvData]
			.map(row => row.map(field => `"${field || ''}"`).join(','))
			.join('\n')
		
		const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
		const link = document.createElement('a')
		link.href = URL.createObjectURL(blob)
		link.download = `candidates_${new Date().toISOString().split('T')[0]}.csv`
		link.click()
		*/
	} catch (err) {
		showError(`Error exporting: ${err.message}`)
	}
}

const handleRefresh = async () => {
	try {
		await fetchCandidates()
		showSuccess(__('Data refreshed successfully'))
	} catch (err) {
		showError(`Error refreshing data: ${err.message}`)
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

// Removed view watching since we only have card view

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
.candidate-management-page ::-webkit-scrollbar {
	width: 8px;
	height: 8px;
}

.candidate-management-page ::-webkit-scrollbar-track {
	background: #f1f5f9;
	border-radius: 4px;
}

.candidate-management-page ::-webkit-scrollbar-thumb {
	background: #cbd5e1;
	border-radius: 4px;
}

.candidate-management-page ::-webkit-scrollbar-thumb:hover {
	background: #94a3b8;
}

/* Smooth transitions */
.candidate-management-page button {
	transition: all 0.2s ease-in-out;
}

.candidate-management-page input,
.candidate-management-page select {
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
