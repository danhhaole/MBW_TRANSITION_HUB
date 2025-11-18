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
		default: 'Salary Alignment'
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
			formatter: '{b}: {c} talents ({d}%)'
		},
		legend: {
			orient: 'vertical',
			right: '5%',
			bottom: '10%',
			textStyle: {
				color: '#4B5563',
				fontSize: 12
			},
			itemWidth: 12,
			itemHeight: 12,
			itemGap: 12
		},
		series: [
			{
				type: 'pie',
				radius: ['40%', '65%'],
				center: ['45%', '50%'],
				avoidLabelOverlap: true,
				itemStyle: {
					borderRadius: 8,
					borderColor: '#fff',
					borderWidth: 2
				},
				label: {
					show: true,
					position: 'outside',
					formatter: '{d}%',
					fontSize: 11,
					fontWeight: 'bold',
					color: '#374151',
					distanceToLabelLine: 8,
					minMargin: 5
				},
				emphasis: {
					label: {
						show: true,
						fontSize: 13,
						fontWeight: 'bold'
					},
					itemStyle: {
						shadowBlur: 10,
						shadowOffsetX: 0,
						shadowColor: 'rgba(0, 0, 0, 0.3)'
					}
				},
				labelLine: {
					show: true,
					length: 25,
					length2: 20,
					lineStyle: {
						width: 1.5
					},
					smooth: true
				},
				data: props.data.map(item => ({
					value: item.value,
					name: item.name,
					itemStyle: {
						color: item.color
					}
				}))
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
