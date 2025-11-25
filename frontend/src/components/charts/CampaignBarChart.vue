<template>
	<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
		<h3 class="text-lg font-semibold text-gray-900 mb-4">{{ title }}</h3>
		<div ref="chartRef" :style="{ width: '100%', height: chartHeight }"></div>
	</div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
	title: {
		type: String,
		default: 'Campaign Performance'
	},
	data: {
		type: Array,
		default: () => []
	},
	chartHeight: {
		type: String,
		default: '320px'
	}
})

const chartRef = ref(null)
let chartInstance = null

const initChart = () => {
	if (!chartRef.value) return

	// Khởi tạo chart instance nếu chưa có
	if (!chartInstance) {
		chartInstance = echarts.init(chartRef.value)
	}

	console.log('CampaignBarChart - initChart called with data:', props.data)

	// Nếu không có data, hiển thị chart trống
	if (!props.data.length) {
		chartInstance.setOption({
			title: {
				text: 'No data available',
				left: 'center',
				top: 'center',
				textStyle: {
					color: '#9CA3AF',
					fontSize: 14
				}
			}
		}, true) // true để clear previous options
		return
	}

	const option = {
		tooltip: {
			trigger: 'axis',
			axisPointer: { type: 'shadow' },
			formatter: (params) => {
				const param = params[0]
				return `${param.name}<br/>Talents: ${param.value}`
			}
		},
		grid: {
			left: '8%',
			right: '8%',
			bottom: '20%',
			top: '10%'
		},
		xAxis: {
			type: 'category',
			data: props.data.map(item => item.name),
			axisLine: { lineStyle: { color: '#e2e8f0' } },
			axisTick: { show: false },
			axisLabel: {
				interval: 0,
				rotate: 25,
				fontSize: 10,
				color: '#64748b'
			}
		},
		yAxis: {
			type: 'value',
			axisLine: { show: false },
			axisTick: { show: false },
			splitLine: { lineStyle: { color: '#f1f5f9' } },
			axisLabel: { fontSize: 11, color: '#64748b' }
		},
		series: [{
			type: 'bar',
			data: props.data.map(item => ({
				value: item.value,
				itemStyle: {
					color: item.color || '#3b82f6',
					borderRadius: [4, 4, 0, 0]
				}
			})),
			barWidth: '50%',
			label: {
				show: true,
				position: 'top',
				formatter: '{c}',
				fontSize: 10,
				color: '#475569'
			}
		}]
	}

	chartInstance.setOption(option, true) // true để hoàn toàn thay thế options cũ
}

const resizeChart = () => {
	if (chartInstance) {
		chartInstance.resize()
	}
}

onMounted(() => {
	initChart()
	window.addEventListener('resize', resizeChart)
})

watch(() => props.data, () => {
	if (chartInstance) {
		initChart()
	}
}, { deep: true })

onUnmounted(() => {
	if (chartInstance) {
		chartInstance.dispose()
	}
	window.removeEventListener('resize', resizeChart)
})
</script>