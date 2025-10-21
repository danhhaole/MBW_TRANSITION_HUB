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
										class="bg-white border border-slate-200 rounded-lg p-4 flex items-center gap-4 cursor-pointer hover:shadow-md transition-shadow"
										@click="openTaskModal(task)"
									>
										<div
											class="flex-shrink-0 w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center"
										>
											<svg
												class="w-5 h-5 text-slate-500"
												fill="none"
												stroke="currentColor"
												viewBox="0 0 24 24"
											>
												<path
													stroke-linecap="round"
													stroke-linejoin="round"
													stroke-width="2"
													d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
												/>
											</svg>
										</div>

										<div class="flex-1">
											<h3 class="text-sm font-medium text-slate-900">{{ task.title }}</h3>
											<p class="text-xs text-slate-500 mt-1">
												{{ task.candidate }} • {{ task.campaign }}
											</p>
										</div>

										<div class="text-right">
											<span
												class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
												:class="getDueDateBadgeColor(task.dueDate)"
											>
												{{ task.dueDate }}
											</span>
										</div>
									</div>
								</div>
							</template>
						</section>
					</div>

					<div class="flex-1">
						<!-- Active Campaigns Section -->
						<section class="fade-in" style="animation-delay: 200ms">
							<h2 class="text-xl font-bold text-slate-800 mb-4">
								{{ __('Active Campaigns') }} (<span>{{ activeCampaigns.length }}</span>)
							</h2>

							<template v-if="campaignsLoading">
								<Loading text="Loading campaigns..." />
							</template>

							<template v-else-if="activeCampaigns.length === 0">
								<div class="text-center py-12">
									<div
										class="flex items-center justify-center w-20 h-20 mx-auto mb-4 bg-blue-100 rounded-full"
									>
										<svg
											class="w-10 h-10 text-blue-600"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
											/>
										</svg>
									</div>
									<p class="text-lg font-medium text-slate-900 mb-2">
										{{ __('No active campaigns') }}
									</p>
								</div>
							</template>

							<template v-else>
								<div class="space-y-3">
									<CampaignCard
										v-for="campaign in activeCampaigns"
										:key="campaign.id"
										:campaign="campaign"
									/>
								</div>
							</template>
						</section>
					</div>
				</div>
			</div>

			<!-- Recently Completed Section -->
			<section class="mt-8 fade-in" style="animation-delay: 300ms">
				<h2 class="text-xl font-bold text-slate-800 mb-4">
					{{ __('Recently Completed') }} (<span>{{ completedCampaigns.length }}</span>)
				</h2>

				<template v-if="completedLoading">
					<Loading text="Loading completed campaigns..." />
				</template>

				<template v-else-if="completedCampaigns.length === 0">
					<div class="text-center py-12">
						<div
							class="flex items-center justify-center w-20 h-20 mx-auto mb-4 bg-gray-100 rounded-full"
						>
							<svg
								class="w-10 h-10 text-gray-600"
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
						<p class="text-lg font-medium text-slate-900 mb-2">
							{{ __('No recently completed campaigns') }}
						</p>
					</div>
				</template>

				<template v-else>
					<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
						<div
							v-for="campaign in completedCampaigns"
							:key="campaign.id"
							class="bg-white border border-slate-200 rounded-lg p-4"
						>
							<h3 class="text-sm font-medium text-slate-900">{{ campaign.name }}</h3>
							<p class="text-xs text-slate-500 mt-1">
								{{ campaign.completedTasks }} {{ __('tasks completed') }}
							</p>
							<p class="text-xs text-slate-400 mt-1">
								{{ __('Last completed') }}: {{ formatDate(campaign.lastCompleted) }}
							</p>
						</div>
					</div>
				</template>
			</section>
		</div>

		<!-- Task Update Modal -->
		<TaskUpdateModal
			v-model="taskModal"
			:task="selectedTask"
			:loading="taskUpdating"
			@update="updateTask"
			@close="closeTaskModal"
		/>
	</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Button } from 'frappe-ui'
import CampaignCard from '@/components/campaign/CampaignCard.vue'
import TaskUpdateModal from '@/components/shared/TaskUpdateModal.vue'
import Loading from '@/components/Loading.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Breadcrumbs } from 'frappe-ui'
import { useDashboardStore } from '@/stores/dashboard'
import { useToast } from '@/composables/useToast'
import { storeToRefs } from 'pinia'

// Store
const dashboardStore = useDashboardStore()

// Use store state with reactivity
const {
  tasks,
  activeCampaigns,
  completedCampaigns,
  loading,
  tasksLoading,
  campaignsLoading,
  completedLoading,
  statistics,
  urgentTasks
} = storeToRefs(dashboardStore)

// Toast
const toast = useToast()

// Local reactive data
const taskModal = ref(false)
const selectedTask = ref(null)
const taskUpdating = ref(false)
const refreshLoading = ref(false)

// Breadcrumbs
const breadcrumbs = [
	{ label: __('Dashboard'), route: { name: 'Dashboard' } }
]

// Load Tasks using store
const loadTasks = async () => {
	try {
		const result = await dashboardStore.fetchTasks()
		if (!result.success) {
			toast.error(result.error || 'Failed to load tasks')
		}
	} catch (error) {
		console.error('Error loading tasks:', error)
		toast.error('Failed to load tasks')
	}
}

// Load Active Campaigns using store
const loadActiveCampaigns = async () => {
	try {
		const result = await dashboardStore.fetchActiveCampaigns()
		if (!result.success) {
			toast.error(result.error || 'Failed to load active campaigns')
		}
	} catch (error) {
		console.error('Error loading active campaigns:', error)
		toast.error('Failed to load active campaigns')
	}
}

// Load Completed Campaigns using store
const loadCompletedCampaigns = async () => {
	try {
		const result = await dashboardStore.fetchCompletedCampaigns()
		if (!result.success) {
			toast.error(result.error || 'Failed to load completed campaigns')
		}
	} catch (error) {
		console.error('Error loading completed campaigns:', error)
		toast.error('Failed to load completed campaigns')
	}
}

// Task actions
const openTaskModal = (task) => {
	selectedTask.value = task
	taskModal.value = true
}

const closeTaskModal = () => {
	taskModal.value = false
	selectedTask.value = null
}

const updateTask = async (taskId, newStatus) => {
	try {
		taskUpdating.value = true
		const result = await dashboardStore.updateTaskStatus(taskId, newStatus)
		
		if (result.success) {
			toast.success('Task updated successfully')
			closeTaskModal()
		} else {
			toast.error(result.error || 'Failed to update task')
		}
	} catch (error) {
		console.error('Error updating task:', error)
		toast.error('Failed to update task')
	} finally {
		taskUpdating.value = false
	}
}

// Refresh all data
const refreshData = async () => {
	refreshLoading.value = true
	try {
		const result = await dashboardStore.refreshAll()
		if (result.success) {
			toast.success('Data refreshed successfully')
		} else {
			toast.error('Failed to refresh some data')
		}
	} catch (error) {
		console.error('Error refreshing data:', error)
		toast.error('Failed to refresh data')
	} finally {
		refreshLoading.value = false
	}
}

// Helper functions
const getDueDateBadgeColor = (dueDate) => {
	switch (dueDate) {
		case 'Hôm nay':
		case 'Quá hạn':
			return 'bg-red-100 text-red-800'
		case 'Ngày mai':
			return 'bg-yellow-100 text-yellow-800'
		default:
			return 'bg-blue-100 text-blue-800'
	}
}

const formatDate = (dateString) => {
	if (!dateString) return 'N/A'
	
	try {
		const date = new Date(dateString)
		return date.toLocaleDateString('vi-VN', {
			year: 'numeric',
			month: '2-digit',
			day: '2-digit',
			hour: '2-digit',
			minute: '2-digit'
		})
	} catch (error) {
		return dateString
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
