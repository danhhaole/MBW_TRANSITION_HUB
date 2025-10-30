<template>
	<div class="flex h-screen bg-gray-50">
		<!-- Vertical Menu Sidebar -->
		<div class="w-64 bg-white border-r border-gray-200 flex flex-col">
			<!-- Header -->
			<div class="p-6 border-b border-gray-200">
				<h1 class="text-xl font-bold text-gray-900">Talent Manager</h1>
				<p class="text-sm text-gray-500 mt-1">Manage pools & talents</p>
			</div>

			<!-- Menu Items -->
			<nav class="flex-1 p-4">
				<button
					v-for="item in menuItems"
					:key="item.id"
					@click="activeSection = item.id"
					:class="[
						'w-full flex items-center gap-3 px-4 py-3 rounded-lg mb-2 transition-all',
						activeSection === item.id
							? 'bg-blue-50 text-blue-700 shadow-sm'
							: 'text-gray-700 hover:bg-gray-50',
					]"
				>
					<FeatherIcon
						:name="item.icon"
						:class="[
							'w-5 h-5',
							activeSection === item.id ? 'text-blue-600' : 'text-gray-500',
						]"
					/>
					<span
						:class="[
							'flex-1 text-left font-medium',
							activeSection === item.id ? 'text-blue-700' : 'text-gray-700',
						]"
					>
						{{ item.label }}
					</span>
					<Badge
						:variant="activeSection === item.id ? 'subtle' : 'outline'"
						:theme="activeSection === item.id ? 'blue' : 'gray'"
					>
						{{ item.count }}
					</Badge>
				</button>
			</nav>

			<!-- Footer -->
			<div class="p-4 border-t border-gray-200">
				<Button variant="solid" theme="blue" class="w-full" @click="handleNewItem">
					<template #prefix>
						<FeatherIcon name="plus" class="w-4 h-4" />
					</template>
					{{ activeSection === 'pools' ? 'New Pool' : 'Add Talent' }}
				</Button>
			</div>
		</div>

		<!-- Main Content Area -->

		<div class="flex-1 flex flex-col overflow-hidden">
			<!-- Top Bar -->
			<div class="bg-white border-b border-gray-200 px-6 py-4">
				<div class="flex items-center justify-between">
					<div>
						<h2 class="text-2xl font-semibold text-gray-900">
							{{ activeSection === 'pools' ? 'Talent Pools' : 'All Talents' }}
						</h2>
						<p class="text-sm text-gray-500 mt-1">
							{{
								activeSection === 'pools'
									? `Manage your ${segments.length} talent pools`
									: `Browse ${talents.length} talents in your system`
							}}
						</p>
					</div>
					<div class="flex items-center gap-3">
						<Input
							v-if="activeSection === 'pools'"
							type="text"
							:placeholder="`Search pools...`"
							:model-value="talentSegmentStore.searchText"
    						@input="handleSearchInput"
							class="w-64"
						>
							<template #prefix>
								<FeatherIcon name="search" class="w-4 h-4 text-gray-400" />
							</template>
						</Input>
						<Button variant="outline">
							<template #prefix>
								<FeatherIcon name="filter" class="w-4 h-4" />
							</template>
							Filter
						</Button>
					</div>
				</div>
			</div>

			<!-- Content List -->
			<div class="flex-1 overflow-auto p-6">
				<!-- Pools Grid View -->
				<div
					v-if="activeSection === 'pools'"
					class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
				>
					<Card
						v-for="segment in segments"
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
									<Button variant="ghost" icon="more-vertical" @click="open" />
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
								<div class="text-xs text-gray-500 mb-1">Candidates</div>
								<div class="text-2xl font-bold text-gray-900">
									{{ segment.candidate_count }}
								</div>
							</div>
							<div>
								<div class="text-xs text-gray-500 mb-1">Engagement Rate</div>
								<div class="flex items-center gap-2">
									<Progress :value="segment.engagement_rate" class="flex-1" />
									<span class="text-sm font-semibold text-gray-900">
										{{ segment.engagement_rate }}%
									</span>
								</div>
							</div>
							<div>
								<div class="text-xs text-gray-500 mb-1">Top Skills</div>
								<div class="flex flex-wrap gap-2">
									<span
										v-for="(skill, index) in parseCriteria(segment.criteria)"
										:key="index"
										class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium"
									>
										{{ skill }}
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
								Manage Pool →
							</Button>
						</div>
					</Card>
				</div>

				<!-- Talents Table View -->
				<Card v-else>
					<div>
						{{ talents }}
					</div>

					<!-- <div class="overflow-x-auto">
						<table class="w-full">
							<thead class="bg-gray-50 border-b border-gray-200">
								<tr>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Name
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Role
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Pool
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Contact
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Status
									</th>
									<th
										class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Actions
									</th>
								</tr>
							</thead>
							<tbody class="divide-y divide-gray-200">
								<tr
									v-for="talent in talents"
									:key="talent.id"
									class="hover:bg-gray-50 transition-colors"
								>
									<td class="px-6 py-4 whitespace-nowrap">
										<div class="flex items-center gap-3">
											<Avatar
												:label="talent.name"
												:image="talent.avatar"
												size="md"
											/>
											<div>
												<div class="font-medium text-gray-900">
													{{ talent.name }}
												</div>
												<div class="text-sm text-gray-500">
													{{ talent.experience }}
												</div>
											</div>
										</div>
									</td>
									<td class="px-6 py-4 whitespace-nowrap">
										<div class="text-sm text-gray-900">{{ talent.role }}</div>
										<div class="text-sm text-gray-500">
											{{ talent.location }}
										</div>
									</td>
									<td class="px-6 py-4 whitespace-nowrap">
										<div class="text-sm text-gray-900">{{ talent.pool }}</div>
									</td>
									<td class="px-6 py-4 whitespace-nowrap">
										<div class="text-sm text-gray-900">{{ talent.email }}</div>
										<div class="text-sm text-gray-500">{{ talent.phone }}</div>
									</td>
									<td class="px-6 py-4 whitespace-nowrap">
										<Badge
											:variant="
												talent.status === 'Active' ? 'subtle' : 'outline'
											"
											:theme="talent.status === 'Active' ? 'green' : 'gray'"
										>
											{{ talent.status }}
										</Badge>
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-right">
										<Button
											variant="ghost"
											theme="blue"
											size="sm"
											@click="viewTalent(talent)"
										>
											View
										</Button>
										<Button
											variant="ghost"
											theme="gray"
											size="sm"
											@click="editTalent(talent)"
										>
											Edit
										</Button>
									</td>
								</tr>
							</tbody>
						</table>
					</div> -->
				</Card>
			</div>
		</div>

		<TalentPoolDialog
			v-model="showTalentPoolDialog"
			:segment="selectedPool"
			@success="handlePoolCreated"
			@cancel="showTalentPoolDialog = false"
		/>

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
							<Button variant="ghost" class="w-7" @click="showDeleteDialog = false">
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
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { Button, Input, Card, Badge, Avatar, FeatherIcon, Dropdown, Progress } from 'frappe-ui'
import TalentPoolDialog from '@/components/talent-segment/TalentPoolDialog.vue'
import { useTalentSegmentStore } from '@/stores/talentSegment'
import { useTalentStore } from '@/stores/talent'
import { useRouter } from 'vue-router'
import { useToast } from '@/composables/useToast'

const { showSuccess, showError } = useToast()

// Active section
const activeSection = ref('pools')
const router = useRouter()
// Menu items
const menuItems = [
	{ id: 'pools', label: 'Talent Pools', icon: 'layers', count: 6 },
	{ id: 'talents', label: 'All Talents', icon: 'users', count: 5 },
]

// Store
const talentSegmentStore = useTalentSegmentStore()
const talentPoolStore = useTalentStore()

console.log('talentPoolStore', talentPoolStore)

// Pools
const searchPool = ref('')
const showTalentPoolDialog = ref(false)
const selectedPool = ref(null)
const showDeleteDialog = ref(false)
const deletingPool = ref(null)
const loading = ref(false)
const deleteDialogOptions = {
	title: 'Delete Talent Pool',
	size: 'sm',
	modalClass: 'max-w-md',
}
const segments = computed(() => talentSegmentStore.talentSegments)
// Talents
const talents = computed(() => talentPoolStore.talents)

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

// Xử lý việc mở dialog để tạo mới
const handleNewItem = () => {
	console.log('Create new>>>>', activeSection.value)
	if (activeSection.value == 'pools') {
		showTalentPoolDialog.value = true
		selectedPool.value = null
	}
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
        talentSegmentStore.setSearchText(event)
        talentSegmentStore.fetchTalentSegments()
    }, 500)
}

const viewTalent = (talent) => {
	console.log('View talent', talent.name)
}

const editTalent = (talent) => {
	console.log('Edit talent', talent.name)
}



onMounted(async () => {
	await talentSegmentStore.fetchTalentSegments()
	await talentPoolStore.fetchTalents()
})

onUnmounted(() => {
    if (searchPool.value) {
        clearTimeout(searchPool.value)
    }
})
</script>

<style scoped>
/* Custom styles nếu cần */
</style>
