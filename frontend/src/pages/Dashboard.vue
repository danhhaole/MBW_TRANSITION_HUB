<template>
	<div class="min-h-screen bg-slate-50">
		<LayoutHeader>
			<template #left-header>
				<Breadcrumbs :items="breadcrumbs" />
			</template>
		</LayoutHeader>

		<div class="dashboard-page container mx-auto w-full min-h-screen p-6">
			<!-- Header -->
			<header class="mb-6">
				<h1 class="text-2xl font-bold text-slate-900">
					{{ __('Marketing Tuyển dụng Dashboard') }}
				</h1>
				<p class="text-sm text-slate-600 mt-1">
					{{ __('Theo dõi hiệu quả chiến dịch tuyển dụng và nuôi dưỡng talent pool') }}
				</p>
			</header>

			<!-- Time Filter -->
			<div class="mb-6 flex items-center justify-between">
				<div class="flex items-center gap-3">
					<label class="text-sm font-medium text-slate-700">
						{{ __('Khoảng thời gian:') }}
					</label>
					<select
						v-model="selectedTimeRange"
						class="text-sm px-3 py-1.5 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent bg-white"
						@change="handleTimeRangeChange"
					>
						<option value="30d">{{ __('30 ngày') }}</option>
						<option value="90d">{{ __('90 ngày') }}</option>
						<option value="ytd">{{ __('Năm nay') }}</option>
						<option value="q4">{{ __('Quý 4/2025') }}</option>
					</select>
				</div>
				<Button variant="ghost" size="sm" :loading="loading" @click="refreshData">
					<template #prefix>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
						</svg>
					</template>
					{{ __('Làm mới') }}
				</Button>
			</div>

			<!-- KPI Cards -->
			<div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-6">
				<StatCard
					:label="__('Tổng Hồ sơ')"
					:value="marketingMetrics.totalTalentPool"
					value-format="number"
					icon-bg-class="bg-blue-50"
					icon-bg-hover-class="bg-blue-100"
					icon-color-class="text-blue-600"
				>
					<template #icon>
						<svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
						</svg>
					</template>
				</StatCard>

				<StatCard
					:label="__('Hồ sơ mới')"
					:value="`+${marketingMetrics.newTalents}`"
					icon-bg-class="bg-emerald-50"
					icon-bg-hover-class="bg-emerald-100"
					icon-color-class="text-emerald-600"
					:meta="__('Trong khoảng thời gian đã chọn')"
				>
					<template #icon>
						<svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
						</svg>
					</template>
				</StatCard>

				<StatCard
					:label="__('Talent Nóng (MQL)')"
					:value="marketingMetrics.hotTalents"
					value-format="number"
					icon-bg-class="bg-orange-50"
					icon-bg-hover-class="bg-orange-100"
					icon-color-class="text-orange-600"
					:meta="__('Tương tác cao')"
				>
					<template #icon>
						<svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
						</svg>
					</template>
				</StatCard>

				<StatCard
					:label="__('Chuyển đổi (SQL)')"
					:value="marketingMetrics.convertedTalents"
					value-format="number"
					icon-bg-class="bg-green-50"
					icon-bg-hover-class="bg-green-100"
					icon-color-class="text-green-600"
					:meta="__('Trong khoảng thời gian đã chọn')"
				>
					<template #icon>
						<svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
					</template>
				</StatCard>

				<StatCard
					:label="__('Chi phí/Talent')"
					:value="marketingMetrics.costPerLead"
					value-format="currency"
					icon-bg-class="bg-purple-50"
					icon-bg-hover-class="bg-purple-100"
					icon-color-class="text-purple-600"
					:meta="__('Mục tiêu: $6.0')"
				>
					<template #icon>
						<svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
					</template>
				</StatCard>
			</div>

			<!-- Charts Row -->
			<div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
				<FunnelChart 
					:title="__('Phễu Nuôi dưỡng')"
					:data="funnelChartData"
					chart-height="320px"
				/>

				<SourcePieChart 
					:title="__('Nguồn gốc Talent')"
					:data="sourceChartData"
					chart-height="320px"
				/>

				<CampaignBarChart 
					:title="__('Top 5 Chiến dịch (CTR)')"
					:data="campaignChartData"
					chart-height="320px"
				/>
			</div>

			<!-- Bottom Row -->
			<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
				<!-- Tasks -->
				<TaskList
					:title="__('Tác vụ Talent Nóng')"
					:tasks="taskListData"
					:clickable="true"
					@task-click="handleTaskClick"
				/>

				<!-- Conversion Table -->
				<DataTable
					:title="__('Chuyển đổi Theo Kênh')"
					:columns="conversionColumns"
					:data="conversionBySource"
					row-key="channel"
				>
					<template #cell-rate="{ value }">
						<span :class="parseFloat(value) >= 5 ? 'text-green-600 font-semibold' : 'text-gray-700 font-semibold'">
							{{ value }}%
						</span>
					</template>
				</DataTable>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { Button, Breadcrumbs } from 'frappe-ui'
import { useDashboardStore } from '@/stores/dashboard'
import { useToast } from '@/composables/useToast'
import LayoutHeader from '@/components/LayoutHeader.vue'
import FunnelChart from '@/components/charts/FunnelChart.vue'
import SourcePieChart from '@/components/charts/SourcePieChart.vue'
import CampaignBarChart from '@/components/charts/CampaignBarChart.vue'
import StatCard from '@/components/shared/StatCard.vue'
import TaskList from '@/components/shared/TaskList.vue'
import DataTable from '@/components/shared/DataTableInChart.vue'

// Store
const dashboardStore = useDashboardStore()
const toast = useToast()

// Store refs
const {
	marketingMetrics,
	funnelData,
	sourceData,
	campaignPerformance,
	conversionBySource,
	loading
} = storeToRefs(dashboardStore)

// Local state
const selectedTimeRange = ref('90d')

// Breadcrumbs
const breadcrumbs = [
	{ label: __('Dashboard'), route: { name: 'Dashboard' } },
	// { label: __('Marketing Recruitment') }
]

// Conversion table columns
const conversionColumns = [
	{ key: 'channel', label: __('Kênh'), align: 'left' },
	{ key: 'total', label: __('Total'), align: 'right', format: 'number' },
	{ key: 'hired', label: __('Hired'), align: 'right', format: 'number' },
	{ key: 'rate', label: __('Tỷ lệ'), align: 'right' }
]

// Computed - Task list data
const taskListData = computed(() => {
	// Mock data - replace with real data from store when available
	return [
		{ 
			id: 1,
			text: 'Chuyển giao cho Recruiter: Le Nguyen (Đã mở 5 lần)', 
			status: 'bg-red-500',
			assignee: 'John Doe',
			dueDate: '2025-11-15'
		},
		{ 
			id: 2,
			text: 'Gửi Follow-up cá nhân cho 15 MQLs (Campaign "LLM Focus")', 
			status: 'bg-orange-500',
			assignee: 'Jane Smith',
			dueDate: '2025-11-16'
		},
		{ 
			id: 3,
			text: 'Review Source: Events Q3 (Tỷ lệ chuyển đổi thấp)', 
			status: 'bg-blue-500',
			assignee: 'Mike Johnson',
			dueDate: '2025-11-20'
		},
		{ 
			id: 4,
			text: 'Liên hệ lại: Nhan Ngo (Cần xác nhận nhu cầu)', 
			status: 'bg-orange-500',
			assignee: 'Sarah Lee',
			dueDate: '2025-11-18'
		}
	]
})

// Computed - Funnel chart data
const funnelChartData = computed(() => {
	const labels = ['Đã Gửi', 'Mở Email', 'Click Link', 'MQL', 'SQL']
	const colors = ['#e2e8f0', '#94a3b8', '#fbbf24', '#10b981', '#3b82f6']
	const values = [
		funnelData.value.sent,
		funnelData.value.opened,
		funnelData.value.clicked,
		funnelData.value.mql,
		funnelData.value.sql
	]
	
	return labels.map((label, index) => ({
		name: label,
		value: values[index],
		color: colors[index],
		totalSent: funnelData.value.sent || 1
	}))
})

// Computed - Source chart data
const sourceChartData = computed(() => {
	const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
	
	return sourceData.value.map((item, index) => ({
		name: item.name,
		value: item.value,
		color: colors[index % colors.length]
	}))
})

// Computed - Campaign chart data
const campaignChartData = computed(() => {
	return campaignPerformance.value.map(item => ({
		name: item.name,
		value: item.ctr
	}))
})

// Methods
const handleTimeRangeChange = async () => {
	try {
		await dashboardStore.refreshMarketingDashboard(selectedTimeRange.value)
		toast.success(__('Dữ liệu đã được cập nhật'))
	} catch (error) {
		console.error('Error changing time range:', error)
		toast.error(__('Không thể cập nhật dữ liệu'))
	}
}

const refreshData = async () => {
	try {
		const result = await dashboardStore.refreshMarketingDashboard(selectedTimeRange.value)
		if (result.success) {
			toast.success(__('Dữ liệu đã được làm mới'))
		} else {
			toast.error(__('Không thể làm mới một số dữ liệu'))
		}
	} catch (error) {
		console.error('Error refreshing data:', error)
		toast.error(__('Lỗi khi làm mới dữ liệu'))
	}
}

const handleTaskClick = (task) => {
	console.log('Task clicked:', task)
	// Handle task click - open modal, navigate, etc.
}

// Lifecycle
onMounted(async () => {
	try {
		await dashboardStore.refreshMarketingDashboard(selectedTimeRange.value)
	} catch (error) {
		console.error('Error loading dashboard:', error)
		toast.error(__('Không thể tải dữ liệu dashboard'))
	}
})
</script>

<style scoped>
.dashboard-page {
	font-family: 'Inter', system-ui, -apple-system, sans-serif;
}
</style>