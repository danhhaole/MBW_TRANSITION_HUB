<template>
	<div class="min-h-screen bg-gray-50">
		<LayoutHeader>
			<template #left-header>
				<Breadcrumbs :items="breadcrumbs" />
			</template>
		</LayoutHeader>

		<div class="talent-management-page container mx-auto w-full min-h-screen pt-10 bg-gray-50">

			<!-- Filters and Controls -->
			<div class="bg-white rounded-lg border border-gray-200 mb-6">
				<div class="p-4">
					<div class="grid grid-cols-1 md:grid-cols-6 gap-4 items-center">
						<!-- Search -->
						<div class="md:col-span-2">
							<FormControl v-model="filters.search" type="text" placeholder="Search talent..."
								:prefix-icon="'search'" />
						</div>

						<!-- Status Filter -->
						<div>
							<FormControl v-model="filters.current_status" type="select" :options="statusFilterOptions" />
						</div>

						<!-- Statistics Display -->
						<div class="md:col-span-2 text-sm text-gray-600">
							<span v-if="statistics.total">
								Total: {{ statistics.total }} | 
								Active: {{ statistics.active }} | 
								Hired: {{ statistics.hired }}
							</span>
						</div>

						<!-- Actions -->
						<div class="flex items-center justify-end space-x-3">
							<!-- Import Button -->
							<Button
								variant="outline"
								theme="blue"
								@click="handleImport"
								title="Import Talent"
								>
									<template #prefix>
										<FeatherIcon name="upload" class="h-4 w-4" />
									</template>
								Import
							</Button>

							<!-- Refresh Button -->
							<Button
								variant="outline"
								theme="gray"
								@click="handleRefresh"
								:loading="loading"
								class="flex items-center"
							>
								<template #prefix>
									<FeatherIcon name="refresh-cw" class="h-4 w-4" :class="{ 'animate-spin': loading }" />
								</template>
								Refresh
							</Button>

							<!-- Clear Filters -->
							<button v-if="hasFilters" @click="clearFilters"
								class="text-sm text-red-600 hover:text-red-800 font-medium px-3 py-2 rounded-lg hover:bg-red-50 transition-colors duration-200">
								Clear Filters
							</button>
						</div>
					</div>
				</div>
			</div>

			<!-- Loading State -->
			<Loading v-if="loading && talents.length === 0" text="Loading talent..." />

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
			Full Name
		</th>
		<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
			Contact Email
		</th>
		<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
			Contact Phone
		</th>
		<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
			Skills
		</th>
		<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
			Current Status
		</th>
		<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
			Actions
		</th>
	</tr>
</thead>

<tbody class="bg-white divide-y divide-gray-200">
	<tr v-for="talent in talents" :key="talent.name"
		class="hover:bg-gray-50 transition-colors duration-200 cursor-pointer"
		@click="openViewModal(talent)">
		
		<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
			{{ talent.full_name }}
		</td>
		<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
			{{ talent.email }}
		</td>
		<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
			{{ talent.phone }}
		</td>
		<td class="px-6 py-4 text-sm text-gray-900">
			<div class="flex flex-wrap gap-1">
				<Badge 
					v-for="skill in processSkills(talent.skills)" 
					:key="skill" 
					theme="blue" 
					variant="subtle"
					class="text-xs"
				>
					{{ skill }}
				</Badge>
				<span v-if="!talent.skills || processSkills(talent.skills).length === 0" class="text-gray-400">-</span>
			</div>
		</td>
		<td class="px-6 py-4 whitespace-nowrap">
			<Badge :theme="getStatusTheme(talent.current_status)">
				{{ talent.current_status }}
			</Badge>
		</td>
		<td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
			<div class="flex items-center space-x-2">
				<button
					class="inline-flex items-center justify-center w-8 h-8 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-full transition-colors duration-200"
					@click.stop="openTalentDetail(talent)" title="Xem chi tiết">
					<FeatherIcon name="eye" class="h-4 w-4" />
				</button>
				<button
					class="inline-flex items-center justify-center w-8 h-8 text-gray-600 hover:text-gray-800 hover:bg-gray-50 rounded-full transition-colors duration-200"
					@click.stop="openViewModal(talent)" title="Xem nhanh">
					<FeatherIcon name="maximize-2" class="h-4 w-4" />
				</button>
			</div>
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
						<span class="text-sm text-gray-700">Items per page:</span>
						<div class="w-20">
							<Select :model-value="pagination.limit" :options="itemsPerPageOptions"
								@change="changeItemsPerPage" />
						</div>
					</div>

					<!-- Page info -->
					<div class="text-sm text-gray-600">
						Showing {{ pagination.showing_from }} to {{ pagination.showing_to }} of
						{{ pagination.total }} talent
					</div>

					<!-- Page navigation -->
					<div class="flex items-center space-x-1">
						<button :disabled="!pagination.has_prev" @click="goToPage(1)"
							class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed">
							<FeatherIcon name="chevrons-left" class="h-4 w-4" />
						</button>

						<button :disabled="!pagination.has_prev" @click="goToPage(pagination.page - 1)"
							class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed">
							<FeatherIcon name="chevron-left" class="h-4 w-4" />
						</button>

						<span class="mx-3 text-sm text-gray-700">
							Page {{ pagination.page }} / {{ Math.ceil(pagination.total / pagination.limit) }}
						</span>

						<button :disabled="!pagination.has_next" @click="goToPage(pagination.page + 1)"
							class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed">
							<FeatherIcon name="chevron-right" class="h-4 w-4" />
						</button>

						<button :disabled="!pagination.has_next" @click="goToPage(Math.ceil(pagination.total / pagination.limit))"
							class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed">
							<FeatherIcon name="chevrons-right" class="h-4 w-4" />
						</button>
					</div>
				</div>
			</div>

			<!-- View Modal -->
			<TalentViewModal v-model="viewModal.show" :talent="viewModal.talent" 
				:loading="viewModal.loading" :error="viewModal.error" />

			<UploadExcelTalentModal
			v-model="showUploadModal"
			@created="handleTalentCreated"
			@close="closeUploadModal"
			/>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useTalentStore } from '@/stores/talent'
import { useToast } from '@/composables/useToast'
import { Button, Select, Badge, Breadcrumbs, FeatherIcon, FormControl } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Loading from '@/components/Loading.vue'
import TalentViewModal from '@/components/talent/TalentViewModal.vue'
import UploadExcelTalentModal from '@/components/UploadExcelTalentModal.vue'

const breadcrumbs = [{ label: 'Talent', route: { name: 'Talent' } }]

// Router
const router = useRouter()

// Store
const talentStore = useTalentStore()

// Composables
const { showToast, showSuccess, showError } = useToast()

// Reactive data from store
const talents = computed(() => talentStore.talents)
const loading = computed(() => talentStore.loading)
const error = computed(() => talentStore.error)
const pagination = computed(() => talentStore.pagination)
const filters = computed(() => talentStore.filters)
const statistics = computed(() => talentStore.statistics)

// Modal states
const viewModal = ref({
	show: false,
	talent: null,
	loading: false,
	error: null,
})

const showUploadModal = ref(false)

// Computed
const statusFilterOptions = computed(() => [
	{ label: 'All Statuses', value: '' },
	{ label: 'Active', value: 'Active' },
	{ label: 'Passive', value: 'Passive' },
	{ label: 'Not Interested', value: 'Not Interested' },
	{ label: 'Hired', value: 'Hired' }
])

const itemsPerPageOptions = [
	{ label: '12', value: 12 },
	{ label: '24', value: 24 },
	{ label: '36', value: 36 },
	{ label: '48', value: 48 },
]

const hasFilters = computed(() => {
	return filters.value.search || filters.value.current_status
})

// Helper methods
const getStatusTheme = (status) => {
	switch (status) {
		case 'Active':
			return 'green'
		case 'Passive':
			return 'yellow'
		case 'Not Interested':
			return 'red'
		case 'Hired':
			return 'blue'
		default:
			return 'gray'
	}
}

const processSkills = (skillsStr) => {
	if (!skillsStr) return []
	
	console.log('Processing skills:', skillsStr, typeof skillsStr)
	
	// If it's already an array, return it
	if (Array.isArray(skillsStr)) {
		return skillsStr.map(skill => String(skill).trim()).filter(skill => skill.length > 0)
	}
	
	// Convert to string if it's not
	const str = String(skillsStr)
	
	// Handle JSON array format like "['Linux', 'Firewall', 'Security Policies']"
	try {
		// Try to parse as JSON first
		const parsed = JSON.parse(str)
		if (Array.isArray(parsed)) {
			return parsed.map(skill => String(skill).trim()).filter(skill => skill.length > 0)
		}
	} catch (e) {
		// If not valid JSON, continue to other formats
	}
	
	// Handle Python-like array format ['item1', 'item2', 'item3']
	if (str.startsWith('[') && str.endsWith(']')) {
		try {
			// Remove brackets and split by comma, then clean up quotes
			const content = str.slice(1, -1)
			const items = content.split(',').map(item => {
				return item.trim().replace(/^['"]|['"]$/g, '') // Remove quotes
			}).filter(item => item.length > 0)
			return items
		} catch (e) {
			console.warn('Failed to parse array-like string:', str)
		}
	}
	
	// Handle comma-separated string
	return str.split(',').map(skill => skill.trim()).filter(skill => skill.length > 0)
}

// Methods
const handleRefresh = async () => {
	try {
		await talentStore.fetchTalents()
		showSuccess('Data refreshed')
	} catch (err) {
		showError(`Error refreshing data: ${err.message}`)
	}
}

const handleImport = () => {
	showUploadModal.value = true
}

const handleTalentCreated = async (result) => {
	showSuccess(`Successfully created ${result.success} talent`)
	await talentStore.fetchTalents()
}

const closeUploadModal = () => {
	showUploadModal.value = false
}

const openTalentDetail = (talent) => {
	router.push({ name: 'TalentDetail', params: { id: talent.name } })
}

const openViewModal = async (talent) => {
	viewModal.value = {
		show: true,
		talent: null,
		loading: true,
		error: null,
	}

	try {
		const result = await talentStore.getTalent(talent.name)
		if (result.success) {
			viewModal.value.talent = result.data
		} else {
			viewModal.value.error = 'Không thể tải thông tin talent'
		}
	} catch (err) {
		viewModal.value.error = err.message
		showError(`Error loading talent: ${err.message}`)
	} finally {
		viewModal.value.loading = false
	}
}

const goToPage = async (page) => {
	await talentStore.fetchTalents({ page })
}

const changeItemsPerPage = async (limit) => {
	await talentStore.fetchTalents({ page: 1, limit })
}

const clearFilters = async () => {
	talentStore.clearFilters()
	await talentStore.fetchTalents({ page: 1 })
}

// Watchers for filters
watch(() => filters.value.search, async (newValue) => {
	if (newValue !== undefined) {
		await talentStore.searchTalents(newValue)
	}
}, { debounce: 500 })

watch(() => filters.value.current_status, async (newValue) => {
	if (newValue !== undefined) {
		await talentStore.fetchTalents({ page: 1 })
	}
})

// Initialize on mount
onMounted(async () => {
	try {
		await Promise.all([
			talentStore.fetchTalents(),
			talentStore.fetchStatistics()
		])
	} catch (err) {
		showError(`Error loading data: ${err.message}`)
	}
})
</script>

<style scoped>
/* Custom scrollbar */
.talent-management-page ::-webkit-scrollbar {
	width: 8px;
	height: 8px;
}

.talent-management-page ::-webkit-scrollbar-track {
	background: #f1f5f9;
	border-radius: 4px;
}

.talent-management-page ::-webkit-scrollbar-thumb {
	background: #cbd5e1;
	border-radius: 4px;
}

.talent-management-page ::-webkit-scrollbar-thumb:hover {
	background: #94a3b8;
}

/* Smooth transitions */
.talent-management-page button {
	transition: all 0.2s ease-in-out;
}

.talent-management-page input,
.talent-management-page select {
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
