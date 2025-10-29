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
							type="text"
							:placeholder="`Search ${activeSection}...`"
							v-model="searchQuery"
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
							<Dropdown :options="poolActions">
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
								@click="managePool(segment)"
							>
								Manage Pool →
							</Button>
						</div>
					</Card>
				</div>

				<!-- Talents Table View -->
				<Card v-else>
					<template #header>
						<div class="flex items-center justify-between">
							<h3 class="text-lg font-semibold text-gray-900">Talent List</h3>
						</div>
					</template>

					<div class="overflow-x-auto">
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
					</div>
				</Card>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { Button, Input, Card, Badge, Avatar, FeatherIcon, Dropdown, Progress } from 'frappe-ui'
import { useTalentSegmentStore } from '@/stores/talentSegment'
import { useTalentPoolStore } from '@/stores/talentPool'

// Active section
const activeSection = ref('pools')
const searchQuery = ref('')
// Menu items
const menuItems = [
	{ id: 'pools', label: 'Talent Pools', icon: 'layers', count: 6 },
	{ id: 'talents', label: 'All Talents', icon: 'users', count: 5 },
]

// Store
const talentSegmentStore = useTalentSegmentStore()
const talentPoolStore = useTalentPoolStore()

// Pools
const segments = computed(() => talentSegmentStore.talentSegments)

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
onMounted(async () => {
	const segments = await talentSegmentStore.fetchTalentSegments()
	console.log('segments', segments)
})

const talents = ref([
	{
		id: 't1',
		name: 'Nguyễn Văn A',
		role: 'Senior Python Developer',
		pool: 'Develop Python',
		status: 'Active',
		email: 'nguyen.a@email.com',
		phone: '+84 123 456 789',
		location: 'Hanoi, Vietnam',
		experience: '5+ years',
		avatar: null,
	},
	{
		id: 't2',
		name: 'Trần Thị B',
		role: 'Full Stack Developer',
		pool: 'Software Developers',
		status: 'Active',
		email: 'tran.b@email.com',
		phone: '+84 987 654 321',
		location: 'Ho Chi Minh, Vietnam',
		experience: '3+ years',
		avatar: null,
	},
	{
		id: 't3',
		name: 'Lê Văn C',
		role: 'Frontend Developer',
		pool: 'Software Developers',
		status: 'Inactive',
		email: 'le.c@email.com',
		phone: '+84 555 123 456',
		location: 'Da Nang, Vietnam',
		experience: '2+ years',
		avatar: null,
	},
	{
		id: 't4',
		name: 'Phạm Thị D',
		role: 'UI/UX Designer',
		pool: 'UI/UX & Product Designers',
		status: 'Active',
		email: 'pham.d@email.com',
		phone: '+84 444 567 890',
		location: 'Hanoi, Vietnam',
		experience: '4+ years',
		avatar: null,
	},
	{
		id: 't5',
		name: 'Hoàng Văn E',
		role: 'Sales Manager',
		pool: 'Sales & Account Managers',
		status: 'Active',
		email: 'hoang.e@email.com',
		phone: '+84 333 789 012',
		location: 'Ho Chi Minh, Vietnam',
		experience: '6+ years',
		avatar: null,
	},
])

const poolActions = [
	{
		label: 'Edit Pool',
		icon: 'edit',
		onClick: () => console.log('Edit pool'),
	},
	{
		label: 'Delete Pool',
		icon: 'trash-2',
		onClick: () => console.log('Delete pool'),
	},
]

const handleNewItem = () => {
	console.log('Create new', activeSection.value)
}

const managePool = (pool) => {
	console.log('Manage pool', pool.name)
}

const viewTalent = (talent) => {
	console.log('View talent', talent.name)
}

const editTalent = (talent) => {
	console.log('Edit talent', talent.name)
}
</script>

<style scoped>
/* Custom styles nếu cần */
</style>
