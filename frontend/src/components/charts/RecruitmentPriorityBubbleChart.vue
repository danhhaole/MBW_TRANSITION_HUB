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
		default: 'Recruitment Priority Matrix'
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
			formatter: (params) => {
				return `${params.data.name}<br/>
						Readiness: ${params.data.readinessLabel}<br/>
						Timeline: ${params.data.timelineLabel}<br/>
						Talents: ${params.data.value[2]}`
			}
		},
		grid: {
			left: '100px',
			right: '4%',
			bottom: '60px',
			top: '10%',
			containLabel: true
		},
		xAxis: {
			name: 'Engagement Timeline (Days)',
			nameLocation: 'middle',
			nameGap: 35,
			nameTextStyle: {
				color: '#4B5563',
				fontSize: 13,
				fontWeight: 'bold'
			},
			type: 'value',
			min: 0,
			max: 90,
			axisLabel: {
				color: '#6B7280',
				fontSize: 12,
				formatter: '{value}d'
			},
			axisLine: {
				lineStyle: {
					color: '#E5E7EB'
				}
			},
			splitLine: {
				lineStyle: {
					color: '#F3F4F6'
				}
			}
		},
		yAxis: {
			name: 'Recruitment Readiness',
			nameLocation: 'middle',
			nameGap: 70,
			nameTextStyle: {
				color: '#4B5563',
				fontSize: 13,
				fontWeight: 'bold'
			},
			type: 'category',
			data: ['Low', 'Medium', 'High'],
			axisLabel: {
				color: '#6B7280',
				fontSize: 12
			},
			axisLine: {
				lineStyle: {
					color: '#E5E7EB'
				}
			},
			splitLine: {
				show: true,
				lineStyle: {
					color: '#F3F4F6'
				}
			}
		},
		series: [
			{
				type: 'scatter',
				symbolSize: (data) => {
					return Math.sqrt(data[2]) * 8 // Size based on talent count
				},
				data: props.data.map(item => ({
					value: item.value,
					name: item.name,
					readinessLabel: item.readinessLabel,
					timelineLabel: item.timelineLabel,
					itemStyle: {
						color: item.color || '#3B82F6',
						opacity: 0.7
					}
				})),
				label: {
					show: true,
					formatter: '{@[2]}',
					position: 'inside',
					color: '#fff',
					fontSize: 11,
					fontWeight: 'bold'
				},
				emphasis: {
					itemStyle: {
						opacity: 1,
						shadowBlur: 10,
						shadowColor: 'rgba(0, 0, 0, 0.3)'
					}
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
