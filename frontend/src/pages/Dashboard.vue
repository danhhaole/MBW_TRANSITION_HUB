<template>
	<div class="min-h-screen bg-gray-50">
		<LayoutHeader>
			<template #left-header>
				<Breadcrumbs :items="breadcrumbs" />
			</template>
		</LayoutHeader>

		<div
			class="dashboard-page container mx-auto w-full min-h-screen p-4 md:p-6 bg-slate-50 text-slate-900"
		>
			<!-- Header -->
			<header class="mb-8">
				<h1 class="text-3xl font-extrabold text-slate-800">{{ __('Overview Dashboard') }}</h1>
				<p class="text-slate-500 mt-1">
					{{ __('Welcome back! Here is the status of your activities today.') }}
				</p>
				<div class="mt-4">
					<Button variant="outline" :loading="refreshLoading" @click="refreshData">
						<template #prefix>
							<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
			</header>

			<div class="flex flex-col lg:flex-row gap-6">
				<!-- Top block: My Tasks + Recently Completed -->
				<div class="flex flex-col lg:flex-row w-full gap-6">
					<div class="flex-1">
						<!-- My Tasks Section -->
						<section class="fade-in" style="animation-delay: 100ms">
							<h2 class="text-xl font-bold text-slate-800 mb-4">
								{{ __('My Tasks') }} (<span>{{ tasks.length }}</span>)
							</h2>

							<template v-if="tasksLoading">
								<Loading text="Loading data..." />
							</template>

							<template v-else-if="tasks.length === 0">
								<div class="text-center py-12">
									<div
										class="flex items-center justify-center w-20 h-20 mx-auto mb-4 bg-green-100 rounded-full"
									>
										<svg
											class="w-10 h-10 text-green-600"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h.01M19 10a9 9 0 11-18 0 9 9 0 0118 0z"
											/>
										</svg>
									</div>
									<p class="text-lg font-medium text-slate-900 mb-2">
										{{ __('Congratulations! You have completed all tasks.') }}
									</p>
								</div>
							</template>

							<template v-else>
								<div class="space-y-3">
									<div
										v-for="task in tasks"
										:key="task.id"
										class="bg-white border border-slate-200 rounded-lg p-4 flex items-center gap-4"
									>
										<div
											class="flex-shrink-0 w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center"
										>
											<svg
												v-if="task.status === 'PENDING_MANUAL'"
												class="w-5 h-5 text-slate-500"
												fill="none"
												stroke="currentColor"
												viewBox="0 0 24 24"
											>
												<path
													stroke-linecap="round"
													stroke-linejoin="round"
													stroke-width="2"
													d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
												/>
											</svg>
											<svg
												v-else
												class="w-5 h-5 text-slate-500"
												fill="none"
												stroke="currentColor"
												viewBox="0 0 24 24"
											>
												<path
													stroke-linecap="round"
													stroke-linejoin="round"
													stroke-width="2"
													d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
												/>
											</svg>
										</div>

										<div class="flex-1">
											<p class="font-semibold text-slate-800">
												{{ task.title }}:
												<span class="font-normal text-slate-600">{{
													task.candidate
												}}</span>
											</p>
											<p class="text-xs text-slate-500">
												{{ __('Campaign:') }} {{ task.campaign }}
											</p>
										</div>

										<div class="text-right flex-shrink-0">
											<p
												:class="[
													'text-xs font-semibold',
													getDueDateTextColor(task.dueDate),
												]"
											>
												{{ task.dueDate }}
											</p>
											<Button
												@click="openTaskModal(task)"
												:variant="'outline'"
												:ref_for="true"
												theme="gray"
												:disabled="taskUpdating"
												class="mt-2 px-3 py-1.5 bg-indigo-600 text-black text-xs font-semibold rounded-lg hover:bg-indigo-700 disabled:opacity-50"
											>
												{{ __('Update') }}
											</Button>
										</div>
									</div>
								</div>
							</template>
						</section>
					</div>
					<div class="flex-1">
						<!-- Recently Completed Section -->
						<section class="fade-in" style="animation-delay: 300ms">
							<h2 class="text-xl font-bold text-slate-800 mb-4">{{ __('Recently Completed') }}</h2>

							<template v-if="completedLoading">
								<Loading text="Loading..." />
							</template>

							<template v-else-if="completedCampaigns.length === 0">
								<div class="text-center py-8">
									<div
										class="flex items-center justify-center w-16 h-16 mx-auto mb-4 bg-slate-100 rounded-full"
									>
										<svg
											class="w-8 h-8 text-slate-400"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
											/>
										</svg>
									</div>
									<p class="text-sm text-slate-600">
										{{ __('No recently completed campaigns') }}
									</p>
								</div>
							</template>

							<template v-else>
								<div class="space-y-4">
									<div
										v-for="campaign in completedCampaigns"
										:key="campaign.id"
										class="bg-white border border-slate-200 rounded-lg p-4 flex items-center gap-4"
									>
										<div
											class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center"
										>
											<svg
												xmlns="http://www.w3.org/2000/svg"
												width="20"
												height="20"
												viewBox="0 0 24 24"
												fill="none"
												stroke="currentColor"
												stroke-width="2"
												stroke-linecap="round"
												stroke-linejoin="round"
												class="text-blue-600"
											>
												<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
												<polyline points="22 4 12 14.01 9 11.01" />
											</svg>
										</div>
										<div class="flex-1">
											<p class="font-semibold text-slate-800">{{ campaign.name }}</p>
											<p class="text-xs text-slate-500">
												{{ campaign.stats.newApplicants }} {{ __('new candidates') }}
											</p>
										</div>
									</div>
								</div>
							</template>
						</section>
					</div>
				</div>
			</div>
			<!-- Bottom block: Active Campaigns -->
			<div class="w-full mt-8">
				<section class="fade-in" style="animation-delay: 200ms">
					<h2 class="text-xl font-bold text-slate-800 mb-4">
						{{ __('Active Campaigns') }}
					</h2>

					<template v-if="campaignsLoading">
						<Loading text="Loading campaigns..." />
					</template>

					<template v-else-if="activeCampaigns.length === 0">
						<div class="text-center py-12">
							<div
								class="flex items-center justify-center w-20 h-20 mx-auto mb-4 bg-slate-100 rounded-full"
							>
								<svg
									class="w-10 h-10 text-slate-400"
									fill="none"
									stroke="currentColor"
									viewBox="0 0 24 24"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z"
									/>
								</svg>
							</div>
							<p class="text-slate-600">{{ __('No active campaigns yet') }}</p>
						</div>
					</template>

					<template v-else>
						<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
							<div
								v-for="campaign in activeCampaigns"
								:key="campaign.id"
								class="bg-white border border-slate-200 rounded-xl shadow-sm p-5 flex flex-col"
							>
								<div class="flex-1">
									<div class="flex justify-between items-start">
										<h3 class="font-bold text-slate-800">{{ campaign.name }}</h3>
										<span
											class="text-xs font-medium px-2 py-1 rounded-full bg-green-100 text-green-700"
										>
											{{ __('Running') }}
										</span>
									</div>

									<div class="mt-4 grid grid-cols-2 gap-4">
										<div class="flex items-center justify-center">
											<div class="relative w-24 h-24">
												<!-- Outer Progress Ring - Tỷ lệ mở (Xanh) -->
												<svg class="w-full h-full" viewBox="0 0 47 47">
													<circle
														class="stroke-current text-blue-200"
														cx="23.5"
														cy="23.5"
														r="20"
														fill="transparent"
														stroke-width="4"
													/>
													<circle
														class="progress-ring-circle stroke-current text-blue-600"
														cx="23.5"
														cy="23.5"
														r="20"
														fill="transparent"
														stroke-width="4"
														:stroke-dasharray="125.66"
														:stroke-dashoffset="
															125.66 -
															(125.66 * campaign.stats.openRate) / 100
														"
														transform="rotate(-90 23.5 23.5)"
														stroke-linecap="round"
													/>
												</svg>

												<!-- Inner Progress Ring - Tỷ lệ nhấp (Tím) -->
												<svg
													class="w-full h-full absolute inset-0"
													viewBox="0 0 31 31"
												>
													<circle
														class="stroke-current text-purple-200"
														cx="15.5"
														cy="15.5"
														r="11"
														fill="transparent"
														stroke-width="4"
													/>
													<circle
														class="progress-ring-circle stroke-current text-purple-600"
														cx="15.5"
														cy="15.5"
														r="11"
														fill="transparent"
														stroke-width="4"
														:stroke-dasharray="69.12"
														:stroke-dashoffset="
															69.12 -
															(69.12 * campaign.stats.clickRate) / 100
														"
														transform="rotate(-90 15.5 15.5)"
														stroke-linecap="round"
													/>
												</svg>

												<div
													class="absolute inset-0 flex flex-col items-center justify-center"
												>
													<span class="text-2xl font-bold text-slate-800">{{
														campaign.stats.newApplicants
													}}</span>
												</div>

												
											</div>
										</div>

										<div class="space-y-2 text-sm">
											<div>
												<p class="text-slate-500">{{ __('Target Candidates') }}</p>
												<p class="font-bold text-slate-800 text-lg">
													{{ campaign.stats.candidates }}
												</p>
											</div>
											<div>
												<p class="text-blue-600 font-medium">{{ __('Open Rate') }}</p>
												<p class="font-bold text-blue-600">
													{{ campaign.stats.openRate }}%
												</p>
											</div>
											<div>
												<p class="text-purple-600 font-medium">{{ __('Click Rate') }}</p>
												<p class="font-bold text-purple-600">
													{{ campaign.stats.clickRate }}%
												</p>
											</div>
										</div>
									</div>
								</div>

								<div class="mt-4 pt-4 border-t border-slate-200">
									<button
										class="w-full text-center text-sm font-semibold text-indigo-600 hover:text-indigo-700"
									>
										{{ __('View workflow details') }}
									</button>
								</div>
							</div>
						</div>
					</template>
				</section>
			</div>

			<!-- Task Update Modal -->
			<TaskUpdateModal
				v-model="taskModal"
				:task="selectedTask"
				@update:completed="handleTaskCompleted"
			/>

			<!-- Toast Container -->
			<ToastContainer
				:show="showToast"
				:message="toastMessage"
				:type="toastType"
				@close="closeToast"
			/>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { createResource } from 'frappe-ui'
import { Button } from 'frappe-ui'
import CampaignCard from '@/components/campaign/CampaignCard.vue'
import TaskUpdateModal from '@/components/shared/TaskUpdateModal.vue'
import { ToastContainer } from '@/components/shared'
import Loading from '@/components/Loading.vue'
import {
	candidateCampaignService,
	actionService,
	candidateService,
} from '../services/universalService'
import { useCampaignStore } from '@/stores/campaign'
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Breadcrumbs } from 'frappe-ui'

// Translation helper function


// Campaign store
const campaignStore = useCampaignStore()

// Reactive data
const tasks = ref([])
const activeCampaigns = ref([])
const completedCampaigns = ref([])
const taskModal = ref(false)
const selectedTask = ref(null)

// Separate loading states for each section
const tasksLoading = ref(false)
const campaignsLoading = ref(false) 
const completedLoading = ref(false)
const taskUpdating = ref(false)
const refreshLoading = ref(false)

// Toast state
const toastMessage = ref('')
const toastType = ref('success')
const showToast = ref(false)

// Computed properties
const urgentTasks = computed(() => {
	return tasks.value.filter(
		(task) =>
			(task.dueDate === 'Hôm nay' || task.dueDate === 'Quá hạn') &&
			task.status === 'PENDING_MANUAL',
	)
})

// Breadcrumbs
const breadcrumbs = [
	{ label: __('Dashboard'), route: { name: 'Dashboard' } }
]

// Load Tasks from Action doctype
const loadTasks = async () => {
	try {
		tasksLoading.value = true
		const result = await actionService.getList({
			filters: {
				status: ['in', ['PENDING_MANUAL']],
			},
			fields: [
				'name',
				'status',
				'scheduled_at',
				'executed_at',
				'talent_campaign_id',
				'campaign_step',
				'assignee_id',
			],
			order_by: 'scheduled_at asc',
			page_length: 10,
		})

		if (result.success) {
			// Transform actions to tasks format
			const actionsWithDetails = await Promise.all(
				result.data.map(async (action) => {
					// Get candidate campaign details
					console.log("action", action)		
					if(action.talent_campaign_id){
						const ccResult = await candidateCampaignService.getFormData(
							action.talent_campaign_id,
						)
						if (ccResult.success) {
							const candidateResult = await candidateService.getFormData(
								ccResult.data.talent_id,
							)
							const campaignResult = await campaignStore.getCampaignDetails(
								ccResult.data.campaign_id
							)

							return {
								id: action.name,
								title: getActionTitle(action.status),
								type: action.status,
								candidate: candidateResult.success
									? candidateResult.data.candidate_name ||
										candidateResult.data.full_name
									: 'Unknown',
								campaign: campaignResult
									? campaignResult.campaign_name
									: 'Unknown',
								dueDate: formatDueDate(action.scheduled_at),
								status: action.status,
								description: `${getActionTitle(action.status)} cho chiến dịch ${campaignResult ? campaignResult.campaign_name : 'Unknown'}`,
								candidateCampaignId: action.talent_campaign_id,
							}
						}
					}
					return null
				}),
			)

			tasks.value = actionsWithDetails.filter((task) => task !== null)
		}
	} catch (error) {
		console.error('Error loading tasks:', error)
		tasks.value = []
	} finally {
		tasksLoading.value = false
	}
}

// Load Active Campaigns
const loadActiveCampaigns = async () => {
	try {
		campaignsLoading.value = true
		const result = await campaignStore.getFilteredCampaigns({
			status: 'ACTIVE',
			limit: 6,
			page: 1
		})

		if (result && result.data) {
			// Get stats for each campaign
			const campaignsWithStats = await Promise.all(
				result.data.map(async (campaign) => {
					const ccResult = await candidateCampaignService.getList({
						filters: { campaign_id: campaign.name },
						fields: ['status', 'creation'],
						page_length: 1000,
					})

					let stats = { total: 0, active: 0, completed: 0, newApplicants: 0 }
					if (ccResult.success) {
						stats.total = ccResult.data.length
						stats.active = ccResult.data.filter((cc) => cc.status === 'ACTIVE').length
						stats.completed = ccResult.data.filter(
							(cc) => cc.status === 'COMPLETED',
						).length
						// Use total count as newApplicants (total candidates in campaign)
						stats.newApplicants = stats.total
					}

					return {
						id: campaign.name,
						name: campaign.campaign_name,
						description: campaign.description,
						status: campaign.status.toLowerCase(),
						stats: {
							...stats,
							candidates: stats.total, // Total candidates in campaign
							openRate:
								stats.total > 0
									? ((stats.active / stats.total) * 100).toFixed(1)
									: 0,
							clickRate:
								stats.total > 0
									? ((stats.completed / stats.total) * 100).toFixed(1)
									: 0,
						},
					}
				}),
			)

			activeCampaigns.value = campaignsWithStats
		}
	} catch (error) {
		console.error('Error loading active campaigns:', error)
		activeCampaigns.value = []
	} finally {
		campaignsLoading.value = false
	}
}

// Load Completed Campaigns (recently completed)
const loadCompletedCampaigns = async () => {
	try {
		completedLoading.value = true
		// Get recently executed actions to show completed campaigns
		const actionsResult = await actionService.getList({
			filters: { status: 'EXECUTED' },
			fields: ['name', 'executed_at', 'talent_campaign_id'],
			order_by: 'executed_at desc',
			page_length: 20,
		})

		if (actionsResult.success) {
			// Group by campaign and get campaign details
			const campaignMap = new Map()

			for (const action of actionsResult.data) {
				if(action.talent_campaign_id){
				const ccResult = await candidateCampaignService.getFormData(
					action.talent_campaign_id,
				)
				if (ccResult.success) {
					const campaignId = ccResult.data.campaign_id
					if (!campaignMap.has(campaignId)) {
						const campaignResult = await campaignStore.getCampaignDetails(campaignId)
						if (campaignResult) {
							campaignMap.set(campaignId, {
								id: campaignId,
								name: campaignResult.campaign_name,
								completedTasks: 1,
								lastCompleted: action.executed_at,
							})
						}
					} else {
						campaignMap.get(campaignId).completedTasks++
					}
				}					
				}
			}

			// Convert to array and sort by last completed
			const campaigns = Array.from(campaignMap.values())
				.sort((a, b) => new Date(b.lastCompleted) - new Date(a.lastCompleted))
				.slice(0, 5)
				.map((campaign) => ({
					id: campaign.id,
					name: campaign.name,
					stats: {
						newApplicants: campaign.completedTasks, // Show completed tasks as "new applicants"
					},
				}))

			completedCampaigns.value = campaigns
		}
	} catch (error) {
		console.error('Error loading completed campaigns:', error)
		completedCampaigns.value = []
	} finally {
		completedLoading.value = false
	}
}

// Update task using frappe.client.set_value
const updateTaskResource = createResource({
	url: 'frappe.client.set_value',
	method: 'POST',
})

// Helper functions
const showToastMessage = (message, type = 'success') => {
	toastMessage.value = message
	toastType.value = type
	showToast.value = true
}

const closeToast = () => {
	showToast.value = false
	toastMessage.value = ''
}

const getActionTitle = (actionStatus) => {
	const titles = {
		SCHEDULED: __('Scheduled'),
		EXECUTED: __('Completed'),
		SKIPPED: __('Skipped'),
		FAILED: __('Failed'),
		PENDING_MANUAL: __('Pending Confirmation'),
	}
	return titles[actionStatus] || __('Task')
}

const formatDueDate = (dueDate) => {
	if (!dueDate) return __('Not specified')

	const due = new Date(dueDate)
	const today = new Date()
	const tomorrow = new Date(today)
	tomorrow.setDate(tomorrow.getDate() + 1)

	// Reset time for date comparison
	due.setHours(0, 0, 0, 0)
	today.setHours(0, 0, 0, 0)
	tomorrow.setHours(0, 0, 0, 0)

	if (due.getTime() === today.getTime()) {
		return __('Today')
	} else if (due.getTime() === tomorrow.getTime()) {
		return __('Tomorrow')
	} else if (due < today) {
		return __('Overdue')
	} else {
		return due.toLocaleDateString('vi-VN', {
			day: '2-digit',
			month: '2-digit',
		})
	}
}

const getDueDateColor = (dueDate) => {
	switch (dueDate) {
		case __('Hôm nay'):
		case __('Quá hạn'):
			return 'error'
		case __('Ngày mai'):
			return 'warning'
		default:
			return 'info'
	}
}

const getDueDateBadgeColor = (dueDate) => {
	switch (dueDate) {
		case __('Hôm nay'):
		case __('Quá hạn'):
			return 'bg-red-100 text-red-800'
		case __('Ngày mai'):
			return 'bg-yellow-100 text-yellow-800'
		default:
			return 'bg-blue-100 text-blue-800'
	}
}

const getTaskColor = (dueDate) => {
	switch (dueDate) {
		case __('Hôm nay'):
		case __('Quá hạn'):
			return 'error'
		case __('Ngày mai'):
			return 'warning'
		default:
			return 'grey-lighten-3'
	}
}

const getTaskBgColor = (dueDate) => {
	switch (dueDate) {
		case __('Hôm nay'):
		case __('Quá hạn'):
			return 'bg-red-500'
		case __('Ngày mai'):
			return 'bg-yellow-500'
		default:
			return 'bg-gray-400'
	}
}

const getDueDateTextColor = (dueDate) => {
	switch (dueDate) {
		case __('Hôm nay'):
		case __('Quá hạn'):
			return 'text-red-600'
		case __('Ngày mai'):
			return 'text-yellow-600'
		default:
			return 'text-slate-600'
	}
}

// Methods
const openTaskModal = (task) => {
	selectedTask.value = task
	taskModal.value = true
}

const handleTaskCompleted = async (taskData) => {
	try {
		taskUpdating.value = true

		// Update action status based on the selected action
		await updateTaskResource.submit({
			doctype: 'Action',
			name: taskData.taskId,
			fieldname: 'status',
			value: taskData.action,
		})

		// Update appropriate datetime field based on action
		if (taskData.action === 'EXECUTED') {
			// Set executed_at to current time in Frappe format
			const now = new Date()
			const frappeFormat =
				now.getFullYear() +
				'-' +
				String(now.getMonth() + 1).padStart(2, '0') +
				'-' +
				String(now.getDate()).padStart(2, '0') +
				' ' +
				String(now.getHours()).padStart(2, '0') +
				':' +
				String(now.getMinutes()).padStart(2, '0') +
				':' +
				String(now.getSeconds()).padStart(2, '0')

			await updateTaskResource.submit({
				doctype: 'Action',
				name: taskData.taskId,
				fieldname: 'executed_at',
				value: frappeFormat,
			})
		} else if (taskData.action === 'SCHEDULED' && taskData.scheduledDate) {
			// Set scheduled_at to the specified date in Frappe format
			const scheduledDateTime = new Date(taskData.scheduledDate)
			const frappeFormat =
				scheduledDateTime.getFullYear() +
				'-' +
				String(scheduledDateTime.getMonth() + 1).padStart(2, '0') +
				'-' +
				String(scheduledDateTime.getDate()).padStart(2, '0') +
				' ' +
				String(scheduledDateTime.getHours()).padStart(2, '0') +
				':' +
				String(scheduledDateTime.getMinutes()).padStart(2, '0') +
				':' +
				String(scheduledDateTime.getSeconds()).padStart(2, '0')

			await updateTaskResource.submit({
				doctype: 'Action',
				name: taskData.taskId,
				fieldname: 'scheduled_at',
				value: frappeFormat,
			})
		}

		// Store notes in the result field as JSON if provided
		if (taskData.notes) {
			const now = new Date()
			const frappeFormat =
				now.getFullYear() +
				'-' +
				String(now.getMonth() + 1).padStart(2, '0') +
				'-' +
				String(now.getDate()).padStart(2, '0') +
				' ' +
				String(now.getHours()).padStart(2, '0') +
				':' +
				String(now.getMinutes()).padStart(2, '0') +
				':' +
				String(now.getSeconds()).padStart(2, '0')

			await updateTaskResource.submit({
				doctype: 'Action',
				name: taskData.taskId,
				fieldname: 'result',
				value: JSON.stringify({
					notes: taskData.notes,
					action: taskData.action,
					updated_by: 'user',
					updated_at: frappeFormat,
				}),
			})
		}
		// Show success message
		const actionMessages = {
			EXECUTED: 'Task completed',
			SCHEDULED: 'Task scheduled',
			SKIPPED: 'Task skipped',
			FAILED: 'Task marked as failed',
		}

		showToastMessage(actionMessages[taskData.action] || 'Task updated', 'success')

		// Only reload tasks section since only tasks were updated
		await loadTasks()
		
		// Also reload completed campaigns if task was executed (completed)
		if (taskData.action === 'EXECUTED') {
			await loadCompletedCampaigns()
		}
	} catch (error) {
		console.error('Error updating task:', error)
		showToastMessage('Could not update task. Please try again.', 'error')
	} finally {
		taskUpdating.value = false
	}
}

const refreshData = async () => {
	refreshLoading.value = true
	try {
		await Promise.all([loadTasks(), loadActiveCampaigns(), loadCompletedCampaigns()])
	} catch (error) {
		console.error('Error refreshing data:', error)
		showToastMessage('Could not load data. Please try again.', 'error')
	} finally {
		refreshLoading.value = false
	}
}

// Lifecycle
onMounted(() => {
	refreshData()
})
</script>

<style scoped>
.dashboard-page {
	font-family:
		'Inter',
		system-ui,
		-apple-system,
		sans-serif;
	background-color: #f8fafc; /* bg-slate-50 */
}

.dashboard-page button {
	transition: all 0.2s ease-in-out;
}

.dashboard-page .hover\:shadow-md:hover {
	box-shadow:
		0 4px 6px -1px rgba(0, 0, 0, 0.1),
		0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Fade-in animation */
@keyframes fadeIn {
	from {
		opacity: 0;
		transform: translateY(10px);
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
}

.fade-in {
	animation: fadeIn 0.5s ease-out forwards;
}

/* Progress ring animation */
.progress-ring-circle {
	transition: stroke-dashoffset 1s cubic-bezier(0.4, 0, 0.2, 1);
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