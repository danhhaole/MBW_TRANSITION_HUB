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
		default: 'Skill Deep Dive'
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

	const option = {
		tooltip: {
			trigger: 'item',
			formatter: '{b}: {c}%'
		},
		radar: {
			indicator: props.data.map(item => ({
				name: item.name,
				max: 100
			})),
			splitNumber: 4,
			name: {
				textStyle: {
					color: '#4B5563',
					fontSize: 12
				}
			},
			splitArea: {
				areaStyle: {
					color: ['rgba(59, 130, 246, 0.05)', 'rgba(59, 130, 246, 0.1)']
				}
			},
			axisLine: {
				lineStyle: {
					color: '#E5E7EB'
				}
			},
			splitLine: {
				lineStyle: {
					color: '#E5E7EB'
				}
			}
		},
		series: [
			{
				type: 'radar',
				data: [
					{
						value: props.data.map(item => item.value),
						name: 'Skill Level',
						areaStyle: {
							color: 'rgba(59, 130, 246, 0.2)'
						},
						lineStyle: {
							color: '#3B82F6',
							width: 2
						},
						itemStyle: {
							color: '#3B82F6'
						}
					}
				]
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
