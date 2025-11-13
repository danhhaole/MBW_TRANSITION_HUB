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
						v-model="timeRange"
						class="text-sm px-3 py-1.5 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent bg-white"
					>
						<option value="30d">{{ __('30 ngày') }}</option>
						<option value="90d">{{ __('90 ngày') }}</option>
						<option value="ytd">{{ __('Năm nay') }}</option>
						<option value="q4">{{ __('Quý 4/2025') }}</option>
					</select>
				</div>
				<Button variant="ghost" size="sm" :loading="refreshLoading" @click="refreshData">
					<template #prefix>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
						</svg>
					</template>
					{{ __('Làm mới') }}
				</Button>
			</div>

			<!-- KPI Cards -->
			<div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-6">
				<StatCard
					:label="__('Tổng Hồ sơ')"
					:value="FIXED_TOTAL_POOL"
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
					:value="`+${currentData.kpi.growth}`"
					icon-bg-class="bg-emerald-50"
					icon-bg-hover-class="bg-emerald-100"
					icon-color-class="text-emerald-600"
				>
					<template #icon>
						<svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
						</svg>
					</template>
				</StatCard>

				<StatCard
					:label="__('Talent Nóng (MQL)')"
					:value="currentData.kpi.hot"
					value-format="number"
					icon-bg-class="bg-orange-50"
					icon-bg-hover-class="bg-orange-100"
					icon-color-class="text-orange-600"
				>
					<template #icon>
						<svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
						</svg>
					</template>
				</StatCard>

				<StatCard
					:label="__('Chuyển đổi (SQL)')"
					:value="currentData.kpi.converted"
					value-format="number"
					icon-bg-class="bg-green-50"
					icon-bg-hover-class="bg-green-100"
					icon-color-class="text-green-600"
				>
					<template #icon>
						<svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
					</template>
				</StatCard>

				<!-- <StatCard
					:label="__('Chi phí/Talent')"
					:value="currentData.kpi.cpl"
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
				</StatCard> -->
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
					:data="conversionTable"
					row-key="channel"
				>
					<template #cell-rate="{ value }">
						<span :class="value >= 5 ? 'text-green-600 font-semibold' : 'text-gray-700 font-semibold'">
							{{ value }}%
						</span>
					</template>
				</DataTable>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Button, Breadcrumbs } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import FunnelChart from '@/components/charts/FunnelChart.vue'
import SourcePieChart from '@/components/charts/SourcePieChart.vue'
import CampaignBarChart from '@/components/charts/CampaignBarChart.vue'
import StatCard from '@/components/shared/StatCard.vue'
import TaskList from '@/components/shared/TaskList.vue'
import DataTable from '@/components/shared/DataTableInChart.vue'

// Data
const timeRange = ref('90d')
const refreshLoading = ref(false)
const FIXED_TOTAL_POOL = 20
const CAMPAIGN_NAMES = ['LLM Focus Q4', 'React Devs Q1', 'Senior Arch.', 'New Grads Sep', 'Data Eng. Q3']

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

// Conversion table data
const conversionTable = [
	{ channel: 'Referral', total: 150, hired: 12, rate: 8.0 },
	{ channel: 'LinkedIn Campaign', total: 450, hired: 15, rate: 3.3 },
	{ channel: 'Career Page Organic', total: 700, hired: 20, rate: 2.8 }
]

// Data by time range
const dataByTime = {
	'30d': {
		kpi: { growth: 0, hot: 0, converted: 0, cpl: 6.2 },
		funnel: { counts: [200, 110, 35, 12, 5], totalSent: 200 },
		source: { counts: [350, 200, 100, 50, 50] },
		campaign: { clicks: [15, 10, 5, 20, 8], sents: [90, 80, 70, 250, 60] }
	},
	'90d': {
		kpi: { growth: 0, hot: 0, converted: 0, cpl: 5.5 },
		funnel: { counts: [500, 250, 80, 30, 15], totalSent: 500 },
		source: { counts: [1000, 750, 400, 350, 350] },
		campaign: { clicks: [45, 32, 18, 60, 25], sents: [243, 225, 178, 800, 190] }
	},
	'ytd': {
		kpi: { growth: 0, hot: 0, converted: 0, cpl: 5.0 },
		funnel: { counts: [1500, 750, 250, 100, 45], totalSent: 1500 },
		source: { counts: [1200, 800, 500, 200, 150] },
		campaign: { clicks: [100, 80, 50, 150, 60], sents: [500, 450, 350, 1800, 400] }
	},
	'q4': {
		kpi: { growth: 0, hot: 0, converted: 0, cpl: 5.8 },
		funnel: { counts: [350, 180, 60, 20, 10], totalSent: 350 },
		source: { counts: [700, 400, 200, 150, 100] },
		campaign: { clicks: [30, 20, 10, 40, 15], sents: [180, 150, 120, 500, 130] }
	}
}

// Computed
const currentData = computed(() => dataByTime[timeRange.value])

// Task list data
const taskListData = computed(() => [
	{ 
		id: 1,
		text: 'Chuyển giao cho Recruiter: Tung Nguyen (Đã mở 5 lần)', 
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
])

// Chart data transformers
const funnelChartData = computed(() => {
	const labels = ['Đã Gửi', 'Mở Email', 'Click Link', 'MQL', 'SQL']
	const colors = ['#e2e8f0', '#94a3b8', '#fbbf24', '#10b981', '#3b82f6']
	
	return labels.map((label, index) => ({
		name: label,
		value: currentData.value.funnel.counts[index],
		color: colors[index],
		totalSent: currentData.value.funnel.totalSent
	}))
})

const sourceChartData = computed(() => {
	const labels = ['LinkedIn', 'Career Page', 'Events', 'Referrals', 'Job Boards']
	const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
	
	return labels.map((label, index) => ({
		name: label,
		value: currentData.value.source.counts[index],
		color: colors[index]
	}))
})

const campaignChartData = computed(() => {
	const data = currentData.value.campaign
	const ctrValues = calculateCTR(data.clicks, data.sents)
	
	return CAMPAIGN_NAMES.map((name, index) => ({
		name: name,
		value: ctrValues[index]
	}))
})

// Methods
const calculateCTR = (clicks, sents) => {
	return clicks.map((clickCount, index) => {
		const sentCount = sents[index]
		if (sentCount === 0) return 0
		return parseFloat(((clickCount / sentCount) * 100).toFixed(2))
	})
}

const handleTaskClick = (task) => {
	console.log('Task clicked:', task)
	// Handle task click - open modal, navigate, etc.
}

// Refresh Data
const refreshData = async () => {
	refreshLoading.value = true
	try {
		await new Promise(resolve => setTimeout(resolve, 800))
		// In real app, fetch data from API here
	} catch (error) {
		console.error('Error refreshing data:', error)
	} finally {
		refreshLoading.value = false
	}
}
</script>

<style scoped>
.dashboard-page {
	font-family: 'Inter', system-ui, -apple-system, sans-serif;
}
</style>