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
		default: 'Source Distribution'
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

	console.log('SourcePieChart - initChart called with data:', props.data)

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

	const totalValue = props.data.reduce((sum, item) => sum + item.value, 0)

	const option = {
		tooltip: {
			trigger: 'item',
			formatter: (params) => {
				const percentage = ((params.value / totalValue) * 100).toFixed(1)
				return `${params.name}<br/>${params.value} hồ sơ (${percentage}%)`
			}
		},
		legend: {
			orient: 'horizontal',
			bottom: '0',
			left: 'center',
			itemGap: 12,
			textStyle: { fontSize: 11, color: '#475569' }
		},
		series: [{
			type: 'pie',
			radius: ['45%', '75%'],
			center: ['50%', '45%'],
			avoidLabelOverlap: false,
			itemStyle: {
				borderRadius: 6,
				borderColor: '#fff',
				borderWidth: 2
			},
			label: { show: false },
			emphasis: {
				label: {
					show: true,
					fontSize: 14,
					fontWeight: 'bold'
				}
			},
			data: props.data.map(item => ({
				name: item.name,
				value: item.value,
				itemStyle: { color: item.color || '#3b82f6' }
			}))
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