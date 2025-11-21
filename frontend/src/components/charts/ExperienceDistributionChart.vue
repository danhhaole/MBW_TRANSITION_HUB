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
		default: 'Experience Distribution'
	},
	data: {
		type: Array,
		default: () => []
	},
	chartHeight: {
		type: String,
		default: '400px'
	}
})

const chartRef = ref(null)
let chartInstance = null

const initChart = () => {
	if (!chartRef.value) return

	chartInstance = echarts.init(chartRef.value)

	// Handle empty data case
	const hasData = props.data && props.data.length > 0
	const chartData = hasData ? props.data : [
		{ name: '0-2 years', value: 0 },
		{ name: '3-5 years', value: 0 },
		{ name: '6-10 years', value: 0 },
		{ name: '11+ years', value: 0 }
	]

	const option = {
		tooltip: {
			trigger: 'axis',
			axisPointer: {
				type: 'shadow'
			},
			formatter: '{b}: {c} talents'
		},
		grid: {
			left: '80px',
			right: '4%',
			bottom: '3%',
			top: '10%',
			containLabel: true
		},
		xAxis: {
			type: 'category',
			data: chartData.map(item => item.name),
			axisLabel: {
				color: '#6B7280',
				fontSize: 12
			},
			axisLine: {
				lineStyle: {
					color: '#E5E7EB'
				}
			}
		},
		yAxis: {
			type: 'value',
			name: 'Number of Talents',
			nameTextStyle: {
				color: '#6B7280',
				fontSize: 12
			},
			axisLabel: {
				color: '#6B7280',
				fontSize: 12
			},
			splitLine: {
				lineStyle: {
					color: '#F3F4F6'
				}
			}
		},
		series: [
			{
				data: chartData.map(item => ({
					value: item.value,
					itemStyle: {
						color: hasData ? new echarts.graphic.LinearGradient(0, 0, 0, 1, [
							{ offset: 0, color: '#3B82F6' },
							{ offset: 1, color: '#60A5FA' }
						]) : '#E5E7EB'
					}
				})),
				type: 'bar',
				barWidth: '60%',
				label: {
					show: true,
					position: 'top',
					color: '#374151',
					fontSize: 12,
					fontWeight: 'bold'
				}
			}
		]
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
