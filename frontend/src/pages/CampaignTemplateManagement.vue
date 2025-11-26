<template>
	<div class="flex h-screen bg-gray-50">
		<!-- Main Content Area -->
		<div class="flex-1 flex flex-col overflow-hidden">
			<!-- Layout Header -->
			<LayoutHeader>
				<template #left-header>
					<Breadcrumbs :items="breadcrumbs" />
				</template>
				<template #right-header>
					<Button variant="solid" theme="gray" @click="handleCreateTemplate">
						<template #prefix>
							<FeatherIcon name="plus" class="h-4 w-4" />
						</template>
						{{ __("Create Template") }}
					</Button>
				</template>
			</LayoutHeader>

			<!-- Main Content -->
			<div class="flex-1 overflow-auto">
				<div class="max-w-full mx-4 px-4 py-8">
					<!-- Page Header -->
					<div class="mb-8">
						<h1 class="text-2xl font-bold text-gray-900">
							{{ __('Campaign Template Library') }}
						</h1>
						<p class="text-sm text-gray-500 mt-1">
							{{
								__(
									'Browse and use pre-built campaign templates to automate your workflows',
								)
							}}
						</p>
					</div>

					<!-- Tabs -->
					<div class="bg-white rounded-lg shadow mb-6">
						<div class="border-b border-gray-200">
							<nav class="flex -mb-px">
								<button
									v-for="tab in tabs"
									:key="tab.id"
									@click="activeTab = tab.id"
									:class="[
										'px-6 py-4 text-sm font-medium border-b-2 transition-colors',
										activeTab === tab.id
											? 'border-blue-500 text-blue-600'
											: 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
									]"
								>
									{{ tab.label }}
									<span
										:class="[
											'ml-2 px-2 py-0.5 rounded-full text-xs',
											activeTab === tab.id
												? 'bg-blue-100 text-blue-600'
												: 'bg-gray-100 text-gray-600',
										]"
									>
										{{ tab.count }}
									</span>
								</button>
							</nav>
						</div>

						<!-- Filters and Search -->
						<div class="p-6 border-b border-gray-200">
							<div
								class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0"
							>
								<div class="flex-1 max-w-lg">
									<div class="relative">
										<FormControl type="text" v-model="searchText" :placeholder="__('Search templates...')" >
											<template #prefix>
												<FeatherIcon class="w-4" name="search" />
											</template>
										</FormControl>
									</div>
								</div>

								<div class="flex items-center space-x-3">
									<Select
										v-model="typeFilter"
										:options="typeOptions"
										class="w-40"
									/>

									<Button
										v-if="hasActiveFilters"
										variant="outline"
										theme="gray"
										@click="clearAllFilters"
									>
										<div class="flex items-center">
											<FeatherIcon name="x" class="w-4 h-4 mr-2" />
											{{ __('Clear Filters') }}
										</div>
									</Button>

									<Button
										variant="outline"
										theme="gray"
										@click="refreshData"
										:loading="loading"
									>
										<div class="flex items-center">
											<FeatherIcon name="refresh-cw" class="w-4 h-4 mr-2" />
											{{ __('Refresh') }}
										</div>
									</Button>
								</div>
							</div>
						</div>

						<!-- Template Cards Grid -->
						<div class="p-6">
							<!-- Loading State -->
							<div
								v-if="loading"
								class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
							>
								<div v-for="i in 8" :key="i" class="animate-pulse">
									<div class="bg-gray-200 h-48 rounded-lg"></div>
								</div>
							</div>

							<!-- Empty State -->
							<div
								v-else-if="!loading && displayedTemplates.length === 0"
								class="text-center py-12"
							>
								<FeatherIcon
									name="inbox"
									class="w-16 h-16 mx-auto mb-4 text-gray-400"
								/>
								<p class="text-gray-500">{{ __('No templates found') }}</p>
								<p class="text-sm text-gray-400 mt-1">
									{{ __('Try adjusting your filters') }}
								</p>
							</div>

							<!-- Template Cards -->
							<div
								v-else
								class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
							>
								<div
									v-for="template in displayedTemplates"
									:key="template.name"
									class="bg-white border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow group relative"
								>
									<!-- Action Dropdown (Hover) -->
									<div
										class="absolute top-2 left-2 z-10 opacity-0 group-hover:opacity-100 transition-opacity"
										@click.stop
									>
										<Dropdown
											:options="getTemplateActions(template)"
											placement="right"
										>
											<template v-slot="{ open }">
												<button
													class="w-8 h-8 bg-white text-gray-700 rounded-full hover:bg-gray-100 flex items-center justify-center shadow-lg border border-gray-200"
												>
													<FeatherIcon name="more-horizontal" class="h-4 w-4" />
												</button>
											</template>
										</Dropdown>
									</div>

									<!-- Template Thumbnail -->
									<div
										@click="viewTemplateDetails(template)"
										class="relative h-32 bg-gradient-to-br from-blue-50 to-blue-100 overflow-hidden cursor-pointer"
									>
										<img
											v-if="template.thumbnail"
											:src="template.thumbnail"
											:alt="template.template_name"
											class="w-full h-full object-cover"
										/>
										<div
											v-else
											class="flex items-center justify-center h-full"
										>
											<FeatherIcon
												:name="getTemplateIcon(template.campaign_type)"
												class="w-12 h-12 text-blue-400"
											/>
										</div>

										<!-- Badge Overlay -->
										<div
											class="absolute top-2 right-2 flex items-center space-x-1"
										>
											<span
												v-if="template.is_premium"
												class="inline-flex items-center px-2 py-1 rounded-md text-xs font-semibold bg-gradient-to-r from-yellow-400 to-orange-500 text-white shadow-md"
											>
												<FeatherIcon name="star" class="w-3 h-3 mr-1" />
												{{ __('Premium') }}
											</span>
											<span
												v-if="template.is_suggestion"
												class="inline-flex items-center px-2 py-1 rounded-md text-xs font-semibold bg-gradient-to-r from-green-400 to-emerald-500 text-white shadow-md"
											>
												<FeatherIcon name="thumbs-up" class="w-3 h-3 mr-1" />
												{{ __('Recommended') }}
											</span>
										</div>
									</div>

									<!-- Template Info -->
									<div class="p-4">
										<div class="flex items-start justify-between mb-2">
											<h3
												class="text-sm font-semibold text-gray-900 line-clamp-2 flex-1 group-hover:text-blue-600 transition-colors"
											>
												{{ template.template_name }}
											</h3>
										</div>

										<p class="text-xs text-gray-500 line-clamp-2 mb-3">
											{{ template.description || __('No description') }}
										</p>

										<!-- Template Meta -->
										<div class="flex items-center justify-between">
											<div class="flex items-center space-x-2">
												<Badge
													:theme="getTypeBadgeTheme(template.campaign_type)"
													size="sm"
												>
													{{ getTypeDisplay(template.campaign_type) }}
												</Badge>
											</div>

											<div class="flex items-center text-xs text-gray-400">
												<FeatherIcon name="users" class="w-3 h-3 mr-1" />
												{{ template.usage_count || 0 }}
											</div>
										</div>
									</div>
								</div>
							</div>

							<!-- Pagination -->
							<div
								v-if="pagination.total > 0"
								class="mt-8 pt-6 border-t border-gray-200"
							>
								<div class="flex items-center justify-between">
									<div class="text-sm text-gray-700">
										{{ __('Showing') }} {{ pagination.showing_from }}
										{{ __('to') }} {{ pagination.showing_to }} {{ __('of') }}
										{{ pagination.total }} {{ __('results') }}
									</div>

									<div class="flex items-center space-x-2">
										<Button
											variant="outline"
											theme="gray"
											size="sm"
											:disabled="!pagination.has_prev"
											@click="goToPage(pagination.page - 1)"
										>
											<FeatherIcon name="chevron-left" class="w-4 h-4" />
										</Button>

										<span class="text-sm text-gray-700">
											{{ __('Page') }} {{ pagination.page }}
										</span>

										<Button
											variant="outline"
											theme="gray"
											size="sm"
											:disabled="!pagination.has_next"
											@click="goToPage(pagination.page + 1)"
										>
											<FeatherIcon name="chevron-right" class="w-4 h-4" />
										</Button>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Template Detail Modal -->
		<CampaignTemplateDetailModal
			v-if="showDetailModal"
			:show="showDetailModal"
			:template="selectedTemplate"
			:loading="modalLoading"
			@close="showDetailModal = false"
			@use-template="handleUseTemplate"
		/>

		<!-- Use Template Modal -->
		<UseTemplateModal
			v-model="showUseTemplateModal"
			:template="templateToUse"
			@created="handleCampaignCreated"
		/>
	</div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Button, Select, Badge, FeatherIcon, FormControl, Breadcrumbs, Dropdown } from 'frappe-ui'
import { useCampaignTemplateStore } from '@/stores/campaignTemplate'
import { useToast } from '@/composables/useToast'
import LayoutHeader from "@/components/LayoutHeader.vue"
import CampaignTemplateDetailModal from '@/components/campaignTemplate/CampaignTemplateDetailModal.vue'
import UseTemplateModal from '@/components/campaign-template/UseTemplateModal.vue'
import { debounce } from 'lodash'

// Composables
const router = useRouter()
const templateStore = useCampaignTemplateStore()
const toast = useToast()

// Breadcrumbs
const breadcrumbs = [{ label: __('Campaign Templates'), route: { name: 'CampaignTemplateManagement' } }]

// Reactive state
const activeTab = ref('system')
const searchText = ref('')
const typeFilter = ref('')
const showDetailModal = ref(false)
const selectedTemplate = ref(null)
const modalLoading = ref(false)
const showUseTemplateModal = ref(false)
const templateToUse = ref(null)

// Tab counts - stored locally and updated when switching tabs
const systemCount = ref(0)
const myCount = ref(0)

// Tabs configuration
const tabs = computed(() => [
	{
		id: 'system',
		label: __('System Templates'),
		count: systemCount.value,
	},
	{
		id: 'my',
		label: __('My Templates'),
		count: myCount.value,
	},
])

// Filter options
const typeOptions = [
	{ label: __('All Types'), value: '' },
	{ label: __('Attraction'), value: 'ATTRACTION' },
	{ label: __('Nurturing'), value: 'NURTURING' },
	{ label: __('Recruitment'), value: 'RECRUITMENT' },
]

// Computed
const loading = computed(() => templateStore.loading)
const pagination = computed(() => templateStore.pagination)

const displayedTemplates = computed(() => {
	// Data is already filtered from server, no need to filter client-side
	return templateStore.templates
})

const hasActiveFilters = computed(() => {
	return searchText.value || typeFilter.value
})

// Get scope filter based on active tab
const getScopeFilter = () => {
	if (activeTab.value === 'system') {
		// System templates: PUBLIC or ORGANIZATION
		return ['in', ['PUBLIC', 'ORGANIZATION']]
	} else {
		// My templates: PRIVATE
		return 'PRIVATE'
	}
}

// Methods
const loadTemplates = async (options = {}) => {
	try {
		// Add scope_type filter based on active tab
		const scopeFilter = getScopeFilter()
		const result = await templateStore.fetchTemplates({
			...options,
			scopeFilter: scopeFilter
		})
		if (result.success) {
			// Update count for current tab
			if (activeTab.value === 'system') {
				systemCount.value = result.count || templateStore.pagination.total || 0
			} else {
				myCount.value = result.count || templateStore.pagination.total || 0
			}
		} else {
			toast.error(result.error || __('Unable to load templates'))
		}
	} catch (error) {
		console.error('Error loading templates:', error)
		toast.error(__('An error occurred while loading templates'))
	}
}

// Load counts for both tabs using direct API call (don't update store)
const loadTabCounts = async () => {
	try {
		const { call } = await import('frappe-ui')
		
		// Load system templates count
		const systemResult = await call('mbw_mira.api.doc.get_list_data', {
			doctype: 'Mira Campaign Template',
			fields: ['name'],
			filters: { scope_type: ['in', ['PUBLIC', 'ORGANIZATION']] },
			limit_page_length: 1
		})
		if (systemResult && systemResult.success) {
			systemCount.value = systemResult.count || 0
		}
		
		// Load my templates count
		const myResult = await call('mbw_mira.api.doc.get_list_data', {
			doctype: 'Mira Campaign Template',
			fields: ['name'],
			filters: { scope_type: 'PRIVATE' },
			limit_page_length: 1
		})
		if (myResult && myResult.success) {
			myCount.value = myResult.count || 0
		}
	} catch (error) {
		console.error('Error loading tab counts:', error)
	}
}

const refreshData = async () => {
	try {
		await Promise.all([loadTabCounts(), loadTemplates({ page: 1 })])
		toast.success(__('Refreshed successfully'))
	} catch (error) {
		console.error('Error refreshing data:', error)
		toast.error(__('Failed to refresh data'))
	}
}

const goToPage = (page) => {
	loadTemplates({ page })
}

const clearAllFilters = () => {
	searchText.value = ''
	typeFilter.value = ''
	templateStore.resetFilters()
	loadTemplates({ page: 1 })
}

const viewTemplateDetails = async (template) => {
	try {
		modalLoading.value = true
		const result = await templateStore.fetchTemplateById(template.name)

		if (result.success) {
			selectedTemplate.value = result.data
			showDetailModal.value = true
		} else {
			toast.error(result.error || __('Unable to load template details'))
		}
	} catch (error) {
		console.error('Error loading template details:', error)
		toast.error(__('An error occurred while loading template details'))
	} finally {
		modalLoading.value = false
	}
}

const handleUseTemplate = (template) => {
	// Open modal instead of confirm
	templateToUse.value = template
	showUseTemplateModal.value = true
}

// Get dropdown actions for template card
const getTemplateActions = (template) => [
	{
		label: __('Use Template'),
		icon: 'play',
		onClick: () => handleUseTemplate(template)
	},
	{
		label: __('View Details'),
		icon: 'eye',
		onClick: () => viewTemplateDetails(template)
	},
	{
		label: __('Edit'),
		icon: 'edit-2',
		onClick: () => handleEditTemplate(template)
	},
	{
		label: __('Delete'),
		icon: 'trash-2',
		theme: 'red',
		onClick: () => confirmDelete(template)
	}
]

// Handle campaign created from modal
const handleCampaignCreated = (data) => {
	toast.success(__('Campaign created successfully!'))
	showDetailModal.value = false
	showUseTemplateModal.value = false
	
	// Navigate to campaign list based on type
	const typeRoutes = {
		'ATTRACTION': '/attraction',
		'NURTURING': '/nurture',
		'RECRUITMENT': '/recruitment'
	}
	
	const route = typeRoutes[data.campaign_type] || '/campaigns'
	router.push(route)
}

const handleCreateTemplate = () => {
	router.push({ name: 'CampaignTemplateCreate' })
}

const handleEditTemplate = (template) => {
	router.push({ name: 'CampaignTemplateEdit', params: { id: template.name } })
}

const confirmDelete = async (template) => {
	if (
		confirm(
			`Are you sure you want to delete "${template.template_name}"?\n\nThis action cannot be undone.`,
		)
	) {
		try {
			const result = await templateStore.deleteTemplate(template.name)
			if (result.success) {
				toast.success(__('Template deleted successfully'))
				await loadTemplates()
			} else {
				toast.error(result.error || __('Failed to delete template'))
			}
		} catch (error) {
			console.error('Error deleting template:', error)
			toast.error(__('An error occurred while deleting template'))
		}
	}
}


const getTemplateIcon = (type) => {
	const iconMap = {
		ATTRACTION: 'user-plus',
		NURTURING: 'heart',
		RECRUITMENT: 'briefcase',
	}
	return iconMap[type] || 'file'
}

const getTypeBadgeTheme = (type) => {
	const themeMap = {
		ATTRACTION: 'blue',
		NURTURING: 'green',
		RECRUITMENT: 'purple',
	}
	return themeMap[type] || 'gray'
}

const getTypeDisplay = (type) => {
	const displayMap = {
		ATTRACTION: 'Attraction',
		NURTURING: 'Nurturing',
		RECRUITMENT: 'Recruitment',
	}
	return displayMap[type] || type
}

// Debounced search function
const debouncedSearch = debounce((searchValue) => {
	templateStore.setSearchText(searchValue)
	loadTemplates({ page: 1 })
}, 500)

// Watchers
watch(searchText, (newValue) => {
	debouncedSearch(newValue)
})

watch(typeFilter, (newValue) => {
	templateStore.setTypeFilter(newValue)
	loadTemplates({ page: 1 })
})

watch(activeTab, () => {
	searchText.value = ''
	typeFilter.value = ''
	templateStore.resetFilters()
	loadTemplates({ page: 1 })
})

// Lifecycle
onMounted(async () => {
	// Load counts for both tabs first
	await loadTabCounts()
	// Then load current tab data
	await loadTemplates()
})
</script>
