<template>
	<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
		<h3 class="text-lg font-semibold text-gray-900 mb-2">{{ title }}</h3>
		<div class="w-full overflow-hidden">
			<div ref="chartRef" :style="{ width: '100%', height: chartHeight }"></div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
	title: {
		type: String,
		default: 'Quality Source Analysis'
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
	const chartData = hasData ? props.data : [{ name: 'No Data', value: 0, totalTalents: 0 }]

	const option = {
		tooltip: {
			trigger: 'axis',
			axisPointer: {
				type: 'shadow'
			},
			formatter: hasData ? (params) => {
				const data = params[0]
				return `${data.name}<br/>
						A-rated talents: ${data.value}%<br/>
						Total talents: ${data.data.totalTalents}`
			} : () => 'No data available'
		},
		grid: {
			left: '25%',
			right: '8%',
			bottom: '8%',
			top: '3%',
			containLabel: true
		},
		xAxis: {
			type: 'value',
			name: 'A-rated Talent Rate (%)',
			nameLocation: 'middle',
			nameGap: 25,
			nameTextStyle: {
				color: '#4B5563',
				fontSize: 13,
				fontWeight: 'bold'
			},
			max: 100,
			axisLabel: {
				color: '#6B7280',
				fontSize: 12,
				formatter: '{value}%'
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
			type: 'category',
			data: chartData.map(item => item.name),
			axisLabel: {
				color: hasData ? '#374151' : '#9CA3AF',
				fontSize: 13,
				fontWeight: 500
			},
			axisLine: {
				lineStyle: {
					color: '#E5E7EB'
				}
			},
			axisTick: {
				show: false
			}
		},
		series: [
			{
				type: 'bar',
				data: chartData.map(item => ({
					value: item.value,
					totalTalents: item.totalTalents,
					itemStyle: {
						color: hasData ? new echarts.graphic.LinearGradient(0, 0, 1, 0, [
							{ offset: 0, color: item.color || '#3B82F6' },
							{ offset: 1, color: item.colorEnd || '#60A5FA' }
						]) : '#E5E7EB',
						borderRadius: [0, 4, 4, 0]
					}
				})),
				barWidth: '60%',
				label: {
					show: hasData,
					position: 'inside',
					formatter: '{c}%',
					color: '#FFFFFF',
					fontSize: 12,
					fontWeight: 'bold'
				},
				emphasis: {
					itemStyle: {
						shadowBlur: 10,
						shadowColor: 'rgba(0, 0, 0, 0.2)'
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
