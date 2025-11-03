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
					<Button variant="solid" theme="gray" @click="showFormModal = true">
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
							{{ __('Flow Template Library') }}
						</h1>
						<p class="text-sm text-gray-500 mt-1">
							{{
								__(
									'Browse and use pre-built flow templates to automate your workflows',
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

									<Select
										v-model="channelFilter"
										:options="channelOptions"
										
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
									<!-- Action Buttons (Hover) -->
									<div
										class="absolute top-2 left-2 z-10 flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity"
									>
										<button
											@click.stop="viewTemplateDetails(template)"
											class="w-8 h-8 bg-blue-500 text-white rounded-full hover:bg-blue-600 flex items-center justify-center shadow-lg"
											title="View Details"
										>
											<FeatherIcon name="eye" class="h-4 w-4" />
										</button>
										<button
											@click.stop="handleEditTemplate(template)"
											class="w-8 h-8 bg-green-500 text-white rounded-full hover:bg-green-600 flex items-center justify-center shadow-lg"
											title="Edit Template"
										>
											<FeatherIcon name="edit-2" class="h-4 w-4" />
										</button>
										<button
											@click.stop="confirmDelete(template)"
											class="w-8 h-8 bg-red-500 text-white rounded-full hover:bg-red-600 flex items-center justify-center shadow-lg"
											title="Delete Template"
										>
											<FeatherIcon name="trash-2" class="h-4 w-4" />
										</button>
									</div>

									<!-- Template Thumbnail -->
									<div
										@click="viewTemplateDetails(template)"
										class="relative h-32 bg-gradient-to-br from-blue-50 to-blue-100 overflow-hidden cursor-pointer"
									>
										<img
											v-if="template.thumbnail"
											:src="template.thumbnail"
											:alt="template.name_template"
											class="w-full h-full object-cover"
										/>
										<div
											v-else
											class="flex items-center justify-center h-full"
										>
											<FeatherIcon
												:name="getTemplateIcon(template.type)"
												class="w-12 h-12 text-blue-400"
											/>
										</div>

										<!-- Badge Overlay -->
										<div
											class="absolute top-2 right-2 flex items-center space-x-1"
										>
											<Badge
												v-if="template.is_premium"
												theme="purple"
												size="sm"
											>
												{{ __('Premium') }}
											</Badge>
											<Badge
												v-if="template.is_suggestion"
												theme="green"
												size="sm"
											>
												{{ __('Recommended') }}
											</Badge>
										</div>
									</div>

									<!-- Template Info -->
									<div class="p-4">
										<div class="flex items-start justify-between mb-2">
											<h3
												class="text-sm font-semibold text-gray-900 line-clamp-2 flex-1 group-hover:text-blue-600 transition-colors"
											>
												{{ template.name_template }}
											</h3>
										</div>

										<p class="text-xs text-gray-500 line-clamp-2 mb-3">
											{{ template.description || __('No description') }}
										</p>

										<!-- Template Meta -->
										<div class="flex items-center justify-between">
											<div class="flex items-center space-x-2">
												<Badge
													:theme="template.type_badge_color"
													size="sm"
												>
													{{ template.display_type }}
												</Badge>
												<div
													v-if="template.channel"
													class="flex items-center text-xs text-gray-500"
												>
													<FeatherIcon
														:name="getChannelIcon(template.channel)"
														class="w-3 h-3 mr-1"
													/>
													{{ template.channel }}
												</div>
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
		<FlowTemplateDetailModal
			v-if="showDetailModal"
			:show="showDetailModal"
			:template="selectedTemplate"
			:loading="modalLoading"
			@close="showDetailModal = false"
			@use-template="handleUseTemplate"
		/>

		<!-- Template Form Modal (Create/Edit) -->
		<FlowTemplateFormModal
			v-if="showFormModal"
			:show="showFormModal"
			:template="editingTemplate"
			:loading="modalLoading"
			@close="handleFormModalClose"
			@submit="handleFormSubmit"
		/>
	</div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Button, Select, Badge, FeatherIcon, FormControl, Breadcrumbs } from 'frappe-ui'
import { useFlowTemplateStore } from '@/stores/flowTemplate'
import { useToast } from '@/composables/useToast'
// import AutomationSidebar from '@/components/AutomationSidebar.vue'
import FlowTemplateDetailModal from '@/components/flowTemplate/FlowTemplateDetailModal.vue'
import FlowTemplateFormModal from '@/components/flowTemplate/FlowTemplateFormModal.vue'
import LayoutHeader from "@/components/LayoutHeader.vue"
import { debounce } from 'lodash'

// Composables
const router = useRouter()
const templateStore = useFlowTemplateStore()
const toast = useToast()

// Breadcrumbs
const breadcrumbs = [{ label: __('Flow Templates'), route: { name: 'FlowTemplateManagement' } }]

// Reactive state
const activeTab = ref('system')
const searchText = ref('')
const typeFilter = ref('')
const channelFilter = ref('')
const showDetailModal = ref(false)
const showFormModal = ref(false)
const selectedTemplate = ref(null)
const editingTemplate = ref(null)
const modalLoading = ref(false)

// Tabs configuration
const tabs = computed(() => [
	{
		id: 'system',
		label: __('System Templates'),
		count: templateStore.statistics.system_templates,
	},
	{
		id: 'my',
		label: __('My Templates'),
		count: templateStore.statistics.my_templates,
	},
])

// Filter options
const typeOptions = [
	{ label: __('All Types'), value: '' },
	{ label: __('Flow'), value: 'FLOW' },
	{ label: __('Sequence'), value: 'SEQUENCE' },
	{ label: __('Campaign'), value: 'CAMPAIGN' },
]

const channelOptions = [
	{ label: __('All Channels'), value: '' },
	{ label: 'Email', value: 'Email' },
	{ label: 'SMS', value: 'SMS' },
	{ label: 'Zalo', value: 'Zalo' },
	{ label: 'Messenger', value: 'Messenger' },
]

// Computed
const loading = computed(() => templateStore.loading)
const pagination = computed(() => templateStore.pagination)

const displayedTemplates = computed(() => {
	if (activeTab.value === 'system') {
		return templateStore.systemTemplates
	} else {
		return templateStore.myTemplates
	}
})

const hasActiveFilters = computed(() => {
	return searchText.value || typeFilter.value || channelFilter.value
})

// Methods
const loadTemplates = async (options = {}) => {
	try {
		// Set filter for current tab
		if (activeTab.value === 'system') {
			templateStore.setDefaultFilter(1)
		} else {
			templateStore.setDefaultFilter(0)
		}

		const result = await templateStore.fetchTemplates(options)

		if (!result.success) {
			toast.error(result.error || __('Unable to load templates'))
		}
	} catch (error) {
		console.error('Error loading templates:', error)
		toast.error(__('An error occurred while loading templates'))
	}
}

const loadStatistics = async () => {
	try {
		await templateStore.fetchStatistics()
	} catch (error) {
		console.error('Error loading statistics:', error)
	}
}

const refreshData = async () => {
	try {
		await Promise.all([loadTemplates({ page: 1 }), loadStatistics()])
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
	channelFilter.value = ''
	templateStore.clearFilters()
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

const handleUseTemplate = async (template) => {
	try {
		// Show loading
		modalLoading.value = true
		
		// Call store action to create flow from template
		const result = await templateStore.useTemplate(
			template.name,
			`${template.name_template} - ${new Date().toLocaleString()}`
		)
		
		if (result.success) {
			toast.success(result.message || __('Flow created successfully from template!'))
			showDetailModal.value = false
			
			// Navigate to flow editor
			// TODO: Update this path based on your flow editor route
			router.push(`/flows/${result.flow_name}/edit`)
		} else {
			toast.error(result.error || __('Failed to create flow from template'))
		}
	} catch (error) {
		console.error('Error using template:', error)
		toast.error(__('An error occurred while creating flow'))
	} finally {
		modalLoading.value = false
	}
}

const handleCreateNew = () => {
	router.push('/flow-templates/new')
}

const handleEditTemplate = (template) => {
	router.push(`/flow-templates/${template.name}/edit`)
}

const confirmDelete = async (template) => {
	if (
		confirm(
			`Are you sure you want to delete "${template.name_template}"?\n\nThis action cannot be undone.`,
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

const handleFormModalClose = () => {
	showFormModal.value = false
	editingTemplate.value = null
}

const handleCreateFromSidebar = (section) => {
	if (section === 'flow-templates') {
		handleCreateNew()
	}
}

const handleFormSubmit = async (formData) => {
	try {
		modalLoading.value = true

		let result
		if (editingTemplate.value) {
			// Update existing template
			result = await templateStore.updateTemplate(editingTemplate.value.name, formData)

			if (result.success) {
				toast.success(__('Template updated successfully'))
				showFormModal.value = false
				editingTemplate.value = null
				await loadTemplates({ page: pagination.value.page })
				await loadStatistics()
			} else {
				toast.error(result.error || __('Failed to update template'))
			}
		} else {
			// Create new template
			result = await templateStore.createTemplate(formData)

			if (result.success) {
				toast.success(__('Template created successfully'))
				showFormModal.value = false
				await loadTemplates({ page: 1 })
				await loadStatistics()
			} else {
				toast.error(result.error || __('Failed to create template'))
			}
		}
	} catch (error) {
		console.error('Error submitting form:', error)
		toast.error(__('An error occurred while saving template'))
	} finally {
		modalLoading.value = false
	}
}

const getTemplateIcon = (type) => {
	const iconMap = {
		FLOW: 'git-branch',
		SEQUENCE: 'list',
		CAMPAIGN: 'mail',
	}
	return iconMap[type] || 'file'
}

const getChannelIcon = (channel) => {
	const iconMap = {
		Email: 'mail',
		SMS: 'message-square',
		Zalo: 'message-circle',
		Messenger: 'facebook',
	}
	return iconMap[channel] || 'send'
}

// Debounced search function
const debouncedSearch = debounce((searchValue) => {
	templateStore.setSearch(searchValue)
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

watch(channelFilter, (newValue) => {
	templateStore.setChannelFilter(newValue)
	loadTemplates({ page: 1 })
})

watch(activeTab, () => {
	// Reset filters when switching tabs
	searchText.value = ''
	typeFilter.value = ''
	channelFilter.value = ''
	templateStore.clearFilters()
	loadTemplates({ page: 1 })
})

// Lifecycle
onMounted(async () => {
	await Promise.all([loadTemplates(), loadStatistics()])
})
</script>
