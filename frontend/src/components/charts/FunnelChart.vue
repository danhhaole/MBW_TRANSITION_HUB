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
		default: 'Funnel Chart'
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

const calculatePercentage = (currentCount, totalCount) => {
	if (totalCount === 0) return '0.0'
	return ((currentCount / totalCount) * 100).toFixed(1)
}

const initChart = () => {
	if (!chartRef.value || !props.data.length) return

	chartInstance = echarts.init(chartRef.value)

	const labels = props.data.map(item => item.name)
	const totalSent = props.data[0]?.totalSent || props.data[0]?.value || 100

	const option = {
		tooltip: {
			trigger: 'axis',
			axisPointer: { type: 'shadow' },
			formatter: (params) => {
				const param = params[0]
				const percentage = calculatePercentage(param.value, totalSent)
				return `${param.name}<br/>${param.value} hồ sơ (${percentage}%)`
			}
		},
		grid: {
			left: '15%',
			right: '15%',
			top: '5%',
			bottom: '5%'
		},
		xAxis: {
			type: 'value',
			max: totalSent,
			show: false
		},
		yAxis: {
			type: 'category',
			data: labels,
			inverse: true,
			axisLine: { show: false },
			axisTick: { show: false },
			axisLabel: { fontSize: 12, color: '#475569' }
		},
		series: [{
			type: 'bar',
			data: props.data.map(item => ({
				value: item.value,
				itemStyle: { 
					color: item.color || '#3b82f6', 
					borderRadius: [0, 4, 4, 0] 
				}
			})),
			barWidth: '65%',
			label: {
				show: true,
				position: 'right',
				formatter: '{c}',
				fontSize: 11,
				color: '#64748b'
			}
		}]
	}

	chartInstance.setOption(option)
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