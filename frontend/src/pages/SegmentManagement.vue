<template>
	<div class="flex h-screen bg-gray-50">
		<div class="flex-1 flex flex-col overflow-hidden">
			<!-- Layout Header -->
			<LayoutHeader>
				<template #left-header>
					<Breadcrumbs :items="breadcrumbs" />
				</template>
				<template #right-header>
					<Button variant="solid" theme="gray" @click="openDialogSegmentOption = true">
						<template #prefix>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-4 w-4"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M12 4v16m8-8H4"
								/>
							</svg>
						</template>
						{{ __('Create Pool') }}
					</Button>
				</template>
			</LayoutHeader>

			<div class="flex-1 overflow-auto">
				<div class="max-w-full mx-2 px-6 py-6">
					<!-- Header -->
					<div class="flex items-center justify-between mb-6">
						<!-- Search -->
						<div class="flex items-center gap-2">
							<Input
								type="text"
								:placeholder="__('Search pool')"
								:model-value="talentSegmentStore.searchText"
								@input="handleSearchInput"
								class="w-64"
							>
								<template #prefix>
									<FeatherIcon name="search" class="w-4 h-4 text-gray-400" />
								</template>
							</Input>
						</div>
						<div class="flex items-center gap-2">
							<!-- <Button variant="outline">
								<template #prefix>
									<FeatherIcon name="filter" class="w-4 h-4" />
								</template>
								{{__("Filter")}}
							</Button> -->
							<!-- Refresh Button -->
							<Button
								variant="outline"
								theme="gray"
								@click="handleRefresh"
                                :loading="loading"
								class="flex items-center py-4"
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
					</div>
					<!-- Main Content -->
					<div class="">
						<div
							v-if="talentSegmentStore.talentSegments.length > 0"
							class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
						>
							<Card
								v-for="segment in talentSegmentStore.talentSegments"
								:key="segment.name"
								class="hover:shadow-md transition-shadow"
							>
								<!-- Card Header -->
								<div class="flex items-start justify-between">
									<div
										class="w-6 h-6 bg-blue-50 rounded-lg flex items-center justify-center"
									>
										<FeatherIcon name="code" class="w-6 h-6 text-blue-600" />
									</div>
									<Dropdown :options="poolActions(segment)">
										<template #default="{ open }">
											<Button
												variant="ghost"
												icon="more-vertical"
												@click="open"
											/>
										</template>
									</Dropdown>
								</div>
								<h3 class="font-semibold text-gray-900 mt-1 mb-2">
									{{ segment.title }}
								</h3>
								<div class="flex items-center gap-2 mb-3 text-xs text-gray-500">
									<FeatherIcon name="clock" class="w-3 h-3" />
									<span>Last updated: {{ segment.formatted_modified }}</span>
								</div>

								<!-- Card Body -->
								<div class="space-y-3">
									<div>
										<div class="text-xs text-gray-500 mb-1">Talents</div>
										<div class="text-2xl font-bold text-gray-900">
											{{ segment.candidate_count }}
										</div>
									</div>
									<div>
										<div class="text-xs text-gray-500 mb-1">
											{{__("Engagement Rate")}}
										</div>
										<div class="flex items-center gap-2">
											<Progress
												:value="segment.engagement_rate"
												class="flex-1"
											/>
											<span class="text-sm font-semibold text-gray-900">
												{{ segment.engagement_rate }}%
											</span>
										</div>
									</div>
									<div>
										<div class="text-xs text-gray-500 mb-1">Top Skills</div>
										<div class="flex flex-wrap gap-2">
											<template
												v-if="parseCriteria(segment.criteria).length > 0"
											>
												<span
													v-for="(skill, index) in parseCriteria(
														segment.criteria,
													)"
													:key="index"
													class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium"
												>
													{{ skill }}
												</span>
											</template>
											<span v-else class="text-gray-500 text-sm px-3 py-1">
												{{ __('No skill') }}
											</span>
										</div>
									</div>
								</div>

								<!-- Card Footer -->
								<div class="pt-3">
									<Button
										variant="ghost"
										theme="blue"
										class="w-full justify-start"
										@click="GoDetails(segment)"
									>
										{{__("Manage Pool")}} →
									</Button>
								</div>
							</Card>
						</div>
						<div v-else class="text-center py-12">
							<div class="text-gray-500">
								<FeatherIcon
									name="search"
									class="w-12 h-12 mx-auto mb-4 text-gray-300"
								/>
								<p class="text-lg font-medium text-gray-500">
									{{ __('No pools found') }}
								</p>
								<p
									class="text-sm text-gray-400 my-1"
									v-if="talentSegmentStore.searchText"
								>
									{{ __('No results for') }} "{{
										talentSegmentStore.searchText
									}}"
								</p>
								<Button
									variant="solid" theme="gray"
									@click="showTalentPoolDialog = true"
								>
									<template #prefix>
										<FeatherIcon name="plus" class="w-4 h-4" />
									</template>
									{{ __('Create New Pool') }}
								</Button>
							</div>
						</div>
					</div>

					<div v-if="talentSegmentStore.pagination.pages > 1">
						<!-- Add this after the grid view section -->
						<div
							class="border rounded-lg bg-white mt-2 px-6 py-4 border-t border-gray-200 flex items-center justify-between"
						>
							<!-- Mobile pagination -->
							<div class="flex-1 flex justify-between sm:hidden">
								<Button
									variant="outline"
									theme="gray"
									size="sm"
									:disabled="talentSegmentStore.pagination.page === 1"
									@click="previousPageSegment"
								>
									{{ __('Previous') }}
								</Button>
								<Button
									variant="outline"
									theme="gray"
									size="sm"
									:disabled="!talentSegmentStore.pagination.has_next"
									@click="nextPageSegment"
								>
									{{ __('Next') }}
								</Button>
							</div>

							<!-- Desktop pagination -->
							<div
								class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between"
							>
								<div>
									<p class="text-sm text-gray-700">
										{{ __('Showing') }}
										<span class="font-medium">{{
											talentSegmentStore.pagination.showing_from || 0
										}}</span>
										{{ __('to') }}
										<span class="font-medium">{{
											talentSegmentStore.pagination.showing_to || 0
										}}</span>
										{{ __('of') }}
										<span class="font-medium">{{
											talentSegmentStore.pagination.total || 0
										}}</span>
										{{ __('results') }}
									</p>
								</div>
								<div>
									<nav
										class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
										aria-label="Pagination"
									>
										<!-- Previous Button -->
										<Button
											variant="outline"
											theme="gray"
											size="sm"
											:disabled="talentSegmentStore.pagination.page === 1"
											@click="previousPageSegment"
											class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
										>
											<span class="sr-only">{{ __('Previous') }}</span>
											<FeatherIcon name="chevron-left" class="h-5 w-5" />
										</Button>

										<!-- Page Numbers -->
										<template
											v-for="pageNumber in visiblePageNumbersSegment"
											:key="pageNumber"
										>
											<Button
												v-if="pageNumber === '...'"
												variant="ghost"
												theme="gray"
												size="sm"
												disabled
												class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700"
											>
												{{ pageNumber }}
											</Button>
											<Button
												v-else
												variant="outline"
												:theme="
													talentSegmentStore.pagination.page ===
													pageNumber
														? 'blue'
														: 'gray'
												"
												size="sm"
												@click="goToPageSegment(pageNumber)"
												class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium"
												:class="
													talentSegmentStore.pagination.page ===
													pageNumber
														? 'bg-blue-50 text-blue-600 z-10'
														: 'bg-white text-gray-500 hover:bg-gray-50'
												"
											>
												{{ pageNumber }}
											</Button>
										</template>

										<!-- Next Button -->
										<Button
											variant="outline"
											theme="gray"
											size="sm"
											:disabled="!talentSegmentStore.pagination.has_next"
											@click="nextPageSegment"
											class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
										>
											<span class="sr-only">{{ __('Next') }}</span>
											<FeatherIcon name="chevron-right" class="h-5 w-5" />
										</Button>
									</nav>
								</div>
							</div>
						</div>
					</div>
				</div>
				<!-- Create option dialog 3 option segment -->

				<Dialog
					v-model="openDialogSegmentOption"
					:options="{
						title: '',
						size: '3xl',
					}"
				>
					<template #body-title>
						<div class="mb-6">
							<h3 class="text-lg font-semibold text-gray-900">
								{{ __('Create Talent Pool') }}
							</h3>
							<p class="text-sm text-gray-500">
								{{ __('Please choose how you want to create a talent pool.') }}
							</p>
						</div>
					</template>

					<template #body-content>
						<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
							<!-- Create Manually -->
							<div
								@click="openManualSegmentCreation"
								class="border border-gray-200 rounded-lg p-4 cursor-pointer hover:border-blue-500 hover:shadow-sm transition-all"
							>
								<div class="flex flex-col items-center text-center">
									<div
										class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center text-blue-600 mb-3"
									>
										<svg
											xmlns="http://www.w3.org/2000/svg"
											class="h-6 w-6"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
											/>
										</svg>
									</div>
									<h4 class="font-medium text-gray-900">
										{{ __('Create Manually') }}
									</h4>
									<p class="text-xs text-gray-500 mt-1">
										{{ __('Create a new talent pool from scratch.') }}
									</p>
								</div>
							</div>

							<!-- AI Suggestions -->
							<div
								@click="openAISegmentSuggestion"
								class="border border-gray-200 rounded-lg p-4 cursor-pointer hover:border-purple-500 hover:shadow-sm transition-all"
							>
								<div class="flex flex-col items-center text-center">
									<div
										class="w-12 h-12 rounded-full bg-purple-50 flex items-center justify-center text-purple-600 mb-3"
									>
										<svg
											xmlns="http://www.w3.org/2000/svg"
											class="h-6 w-6"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M13 10V3L4 14h7v7l9-11h-7z"
											/>
										</svg>
									</div>
									<h4 class="font-medium text-gray-900">
										{{ __('AI Suggestions') }}
									</h4>
									<p class="text-xs text-gray-500 mt-1">
										{{ __('Get AI-powered pool suggestions.') }}
									</p>
								</div>
							</div>

							<!-- Sync from ATS -->
							<div
								@click="syncFromATS"
								class="border border-gray-200 rounded-lg p-4 cursor-pointer hover:border-green-500 hover:shadow-sm transition-all"
							>
								<div class="flex flex-col items-center text-center">
									<div
										class="w-12 h-12 rounded-full bg-green-50 flex items-center justify-center text-green-600 mb-3"
									>
										<svg
											xmlns="http://www.w3.org/2000/svg"
											class="h-6 w-6"
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
									</div>
									<h4 class="font-medium text-gray-900">
										{{ __('Sync from ATS') }}
									</h4>
									<p class="text-xs text-gray-500 mt-1">
										{{ __('Import pools from your ATS system.') }}
									</p>
								</div>
							</div>
						</div>
					</template>

					<template #actions>
						<div class="flex justify-end pt-4 border-t border-gray-200 mt-6">
							<Button
								variant="outline"
								theme="gray"
								@click="openDialogSegmentOption = false"
								class="px-4"
							>
								{{ __('Cancel') }}
							</Button>
						</div>
					</template>
				</Dialog>

				<!-- Create Edit form segment -->
				<TalentPoolDialog
					v-model="showTalentPoolDialog"
					:segment="selectedPool"
					@success="handlePoolCreated"
					@cancel="showTalentPoolDialog = false"
				/>

				<!-- ATS Sync Dialog -->
				<ATSSyncDialog
					v-model="showATSSyncDialog"
					@success="handleSyncSuccess"
				/>

				<!-- AI Suggestion Modal -->
				<Dialog
					v-model="showAISuggestionModal"
					:options="{
						title: 'Tạo pool từ gợi ý AI',
						size: '3xl',
					}"
				>
					<template #body-content>
						<div class="space-y-4">
							<!-- URL Input -->
							<div class="flex gap-2">
								<Input
									v-model="companyURL"
									type="text"
									:placeholder="__('Nhập URL website công ty')"
									class="flex-1"
								/>
								<Button
									variant="solid" theme="gray"
									:loading="isFetchingPositions"
									@click="fetchAISuggestions"
								>
									<template #prefix>
										<FeatherIcon name="search" class="w-4 h-4" />
									</template>
									{{ __('Lấy thông tin sử dụng AI') }}
								</Button>
							</div>

							<!-- Loading State -->
							<div v-if="isFetchingPositions" class="text-center py-8">
								<LoadingIndicator class="w-8 h-8 mx-auto" />
								<p class="mt-2 text-sm text-gray-600">
									{{ __('Đang tải các vị trí làm việc...') }}
								</p>
							</div>

							<!-- Positions List -->
							<div
								v-else-if="aiPositions.length > 0"
								class="border rounded-lg divide-y"
							>
								<!-- Select All header row -->
								<div class="p-4 bg-gray-50 border-b flex items-center">
									<input
										type="checkbox"
										:checked="areAllPositionsSelected"
										@change="toggleAllPositions"
										class="h-4 w-4 text-blue-600 rounded border-gray-300"
									/>
									<span class="ml-3 text-sm font-medium text-gray-700">{{
										__('Select All')
									}}</span>
									<span class="ml-auto text-sm font-medium text-gray-700">{{
										__('Department')
									}}</span>
								</div>

								<!-- Positions list -->
								<div
									v-for="position in aiPositions"
									:key="position.id"
									class="p-4 hover:bg-gray-50 flex items-center"
								>
									<input
										type="checkbox"
										:checked="selectedPositions.includes(position.id)"
										@change="togglePositionSelection(position.id)"
										class="h-4 w-4 text-blue-600 rounded border-gray-300"
									/>
									<span class="ml-3 text-gray-900 font-medium">
										{{ position.title }}
									</span>
									<span class="ml-auto text-sm text-gray-500">
										{{ position.department }}
									</span>
								</div>
							</div>

							<!-- Empty State -->
							<div
								v-else-if="!isFetchingPositions"
								class="text-center py-8 border rounded-lg"
							>
								<p class="text-gray-500">
									{{
										__(
											'Nhập URL và nhấn "Lấy thông tin" để xem các vị trí làm việc',
										)
									}}
								</p>
							</div>
						</div>
					</template>

					<template #actions>
						<div class="flex justify-end space-x-3 pt-4">
							<Button variant="outline" theme="gray" @click="closeAISuggestionModal">
								Hủy
							</Button>
							<Button
								variant="solid" theme="gray"
								:disabled="selectedPositions.length === 0"
								@click="createPoolsFromSelection"
							>
								Tạo pool ({{ selectedPositions.length }})
							</Button>
						</div>
					</template>
				</Dialog>

				<Dialog v-model="showDeleteDialog" :options="deleteDialogOptions">
					<template #body>
						<div class="bg-white px-4 pb-6 pt-5 sm:px-6">
							<div class="mb-5 flex items-center justify-between">
								<div>
									<h3 class="text-2xl font-semibold leading-6 text-gray-900">
										{{ __('Confirm Delete') }}
									</h3>
								</div>
								<div class="flex items-center gap-1">
									<Button
										variant="ghost"
										class="w-7"
										@click="showDeleteDialog = false"
									>
										<FeatherIcon name="x" class="h-4 w-4" />
									</Button>
								</div>
							</div>
							<div>
								<div class="sm:flex sm:items-start">
									<div
										class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10"
									>
										<svg
											class="h-6 w-6 text-red-600"
											xmlns="http://www.w3.org/2000/svg"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
											/>
										</svg>
									</div>
									<div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
										<h3 class="text-lg leading-6 font-medium text-gray-900">
											{{ __('Delete Talent Pool') }}
										</h3>
										<div class="mt-2">
											<p class="text-sm text-gray-500">
												{{ __('Are you sure you want to delete') }} "{{
													deletingPool?.title
												}}"? {{ __('This action cannot be undone.') }}
											</p>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="px-4 pb-7 pt-4 sm:px-6">
							<div class="flex justify-end items-center gap-3">
								<Button
									variant="outline"
									theme="gray"
									@click="showDeleteDialog = false"
									:disabled="loading"
								>
									{{ __('Cancel') }}
								</Button>
								<Button
									variant="solid"
									theme="red"
									@click="confirmDelete"
									:loading="loading"
								>
									{{ __('Delete') }}
								</Button>
							</div>
						</div>
					</template>
				</Dialog>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import {
	Breadcrumbs,
	Button,
	Input,
	Card,
	FeatherIcon,
	Dropdown,
	Progress,
	Dialog,
	LoadingIndicator,
} from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import ATSSyncDialog from '@/components/ATSSyncDialog.vue'
import TalentPoolDialog from '@/components/talent-segment/TalentPoolDialog.vue'
import { useRouter } from 'vue-router'
import { useToast } from '@/composables/useToast'
import { useTalentSegmentStore } from '@/stores/talentSegment'
// Breadcrumbs
const breadcrumbs = [{ label: __('Pools'), route: { name: 'SegmentPool' } }]
const { showSuccess, showError } = useToast()
const router = useRouter()
// Store
const talentSegmentStore = useTalentSegmentStore()
const searchPool = ref('')
const openDialogSegmentOption = ref(false)
const showTalentPoolDialog = ref(false)
const selectedPool = ref(null)
const showDeleteDialog = ref(false)
const deletingPool = ref(null)
const showAISuggestionModal = ref(false)
const companyURL = ref('')
const isFetchingPositions = ref(false)
const aiPositions = ref([])
const selectedPositions = ref([])
const showATSSyncDialog = ref(false)
const loading = computed(() => talentSegmentStore.loading)

// Mock data for positions - replace with actual API call
const mockPositions = [
	{ id: 1, title: 'Frontend Developer', department: 'Engineering' },
	{ id: 2, title: 'Backend Developer', department: 'Engineering' },
	{ id: 3, title: 'Product Manager', department: 'Product' },
	{ id: 4, title: 'UX/UI Designer', department: 'Design' },
	{ id: 5, title: 'Data Scientist', department: 'Data' },
]
const deleteDialogOptions = {
	title: 'Delete Talent Pool',
	size: 'sm',
	modalClass: 'max-w-md',
}

const poolActions = (pool) => [
	{
		label: 'Edit Pool',
		icon: 'edit',
		onClick: () => handleEditPool(pool),
	},
	{
		label: 'Delete Pool',
		icon: 'trash-2',
		onClick: () => handleDetelePoool(pool),
	},
]

const segments = computed(() => talentSegmentStore.talentSegments)
const handleRefresh = async () => {
  await fetchSegments();

  showSuccess(__("Data refreshed"), "info", 2000);
};
// Computed property for segment pagination numbers
const visiblePageNumbersSegment = computed(() => {
	const totalPages = Math.ceil(
		talentSegmentStore.pagination.total / talentSegmentStore.pagination.limit,
	)
	const currentPage = talentSegmentStore.pagination.page
	const pageNumbers = []
	const maxVisiblePages = 5

	if (totalPages <= maxVisiblePages) {
		for (let i = 1; i <= totalPages; i++) {
			pageNumbers.push(i)
		}
	} else {
		pageNumbers.push(1)

		let startPage = Math.max(2, currentPage - 1)
		let endPage = Math.min(totalPages - 1, currentPage + 1)

		if (currentPage <= 3) {
			endPage = 4
		} else if (currentPage >= totalPages - 2) {
			startPage = totalPages - 3
		}

		if (startPage > 2) {
			pageNumbers.push('...')
		}

		for (let i = startPage; i <= endPage; i++) {
			pageNumbers.push(i)
		}

		if (endPage < totalPages - 1) {
			pageNumbers.push('...')
		}

		if (totalPages > 1) {
			pageNumbers.push(totalPages)
		}
	}

	return pageNumbers
})

// Pagination methods for segments
const previousPageSegment = () => {
	if (talentSegmentStore.pagination.page > 1) {
		talentSegmentStore.pagination.page--
		fetchSegments()
	}
}

const nextPageSegment = () => {
	if (talentSegmentStore.pagination.has_next) {
		talentSegmentStore.pagination.page++
		fetchSegments()
	}
}

const goToPageSegment = (pageNumber) => {
	if (pageNumber !== '...' && pageNumber !== talentSegmentStore.pagination.page) {
		talentSegmentStore.pagination.page = pageNumber
		fetchSegments()
	}
}

// Update your fetchSegments method to include pagination
const fetchSegments = async () => {
	await talentSegmentStore.fetchTalentSegments({
		page: talentSegmentStore.pagination.page,
		limit: talentSegmentStore.pagination.limit,
		searchText: talentSegmentStore.searchText, // Include current search text
	})
}

const parseCriteria = (criteria) => {
	try {
		if (!criteria) return []
		// Parse JSON string
		const parsed = JSON.parse(criteria)
		if (!Array.isArray(parsed)) return []

		// Lấy phần tử đầu tiên: ["skills", "==", "React, Python"]
		const item = parsed[0]
		if (!Array.isArray(item) || item.length < 3) return []

		// Lấy giá trị "React, Python" -> tách bằng dấu phẩy
		return item[2].split(',').map((s) => s.trim())
	} catch (e) {
		console.error('Error parsing criteria:', e)
		return []
	}
}
const openManualSegmentCreation = () => {
	openDialogSegmentOption.value = false
	showTalentPoolDialog.value = true
	selectedPool.value = null
}

const openAISegmentSuggestion = () => {
	// Add your AI suggestion logic here
	console.log('Open AI Suggestion')
	openDialogSegmentOption.value = false
	showAISuggestionModal.value = true
	// Reset state when opening modal
	companyURL.value = ''
	aiPositions.value = []
	selectedPositions.value = []
}

//FAKE
const areAllPositionsSelected = computed(() => {
	return (
		aiPositions.value.length > 0 &&
		aiPositions.value.every((pos) => selectedPositions.value.includes(pos.id))
	)
})

const toggleAllPositions = () => {
	if (areAllPositionsSelected.value) {
		// If all are selected, deselect all
		selectedPositions.value = []
	} else {
		// Otherwise select all positions
		selectedPositions.value = aiPositions.value.map((pos) => pos.id)
	}
}

const closeAISuggestionModal = () => {
	showAISuggestionModal.value = false
}

const fetchAISuggestions = async () => {
	if (!companyURL.value.trim()) {
		// Show error message
		return
	}

	isFetchingPositions.value = true
	selectedPositions.value = []

	try {
		// TODO: Replace with actual API call
		// const response = await fetchAISuggestedPositions(companyURL.value)
		// aiPositions.value = response.data.positions

		// Mock API call
		await new Promise((resolve) => setTimeout(resolve, 1000))
		aiPositions.value = mockPositions
	} catch (error) {
		console.error('Error fetching AI suggestions:', error)
		// Show error message to user
	} finally {
		isFetchingPositions.value = false
	}
}

const togglePositionSelection = (positionId) => {
	const index = selectedPositions.value.indexOf(positionId)
	if (index === -1) {
		selectedPositions.value.push(positionId)
	} else {
		selectedPositions.value.splice(index, 1)
	}
}

const createPoolsFromSelection = async () => {
	if (selectedPositions.value.length === 0) return

	try {
		const selectedPositionData = aiPositions.value.filter((p) =>
			selectedPositions.value.includes(p.id),
		)

		// TODO: Replace with actual API call to create pools
		// await createPools(selectedPositionData)

		// Mock API call
		await new Promise((resolve) => setTimeout(resolve, 1000))

		// Show success message
		console.log('Created pools for positions:', selectedPositionData)

		// Close modal and refresh pools list
		closeAISuggestionModal()
		await fetchSegments() // Assuming this refreshes your pools list
	} catch (error) {
		console.error('Error creating pools:', error)
		// Show error message to user
	}
}

const syncFromATS = async () => {
	openDialogSegmentOption.value = false
	showATSSyncDialog.value = true
}

const handleSyncSuccess = async () => {
	// Refresh segment list after successful sync
	await fetchSegments()
	showSuccess(__('Positions synced successfully'))
}

const handlePoolCreated = async () => {
	await talentSegmentStore.fetchTalentSegments()
	showTalentPoolDialog.value = false
	selectedPool.value = null
}

const GoDetails = (pool) => {
	console.log('Manage pool', pool.name)
	router.push(`/talent-segments/${pool.name}`)
}

const handleEditPool = (pool) => {
	console.log('Edit pool', pool)
	selectedPool.value = pool
	showTalentPoolDialog.value = true
}

const handleDetelePoool = (pool) => {
	deletingPool.value = pool
	showDeleteDialog.value = true
}

const confirmDelete = async () => {
	if (deletingPool.value) {
		try {
			loading.value = true
			await talentSegmentStore.deleteTalentSegment(deletingPool.value.name)
			showSuccess(__('Talent pool deleted successfully'))
			showDeleteDialog.value = false
			deletingPool.value = null
			await talentSegmentStore.fetchTalentSegments()
		} catch (error) {
			console.error('Error deleting pool:', error)
			showError(error.message || __('Failed to delete talent pool'))
		} finally {
			loading.value = false
		}
	}
}

const handleSearchInput = (event) => {
	// Clear any existing timeout
	if (searchPool.value) {
		clearTimeout(searchPool.value)
	}

	// Set a new timeout to fetch after user stops typing (500ms delay)
	searchPool.value = setTimeout(() => {
		// Reset to first page when searching
		talentSegmentStore.pagination.page = 1
		talentSegmentStore.setSearchText(event)
		// Force refresh with updated search text
		talentSegmentStore.fetchTalentSegments({
			page: 1,
			limit: talentSegmentStore.pagination.limit,
			searchText: event, // Pass search text directly to the API
		})
	}, 500)
}

onMounted(async () => {
	await talentSegmentStore.fetchTalentSegments()
})

onUnmounted(() => {
	if (searchPool.value) {
		clearTimeout(searchPool.value)
	}
})
</script>
