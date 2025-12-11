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
		default: 'Skill Deep Dive',
	},
	data: {
		type: Array,
		default: () => [],
	},
	chartHeight: {
		type: String,
		default: '400px',
	},
})

const chartRef = ref(null)
let chartInstance = null

const initChart = () => {
	if (!chartRef.value) return

	chartInstance = echarts.init(chartRef.value)

	// Handle empty data case
	const hasData = props.data && props.data.length > 0
	const chartData = hasData
		? props.data
		: [
				{ name: 'Skill 1', value: 0 },
				{ name: 'Skill 2', value: 0 },
				{ name: 'Skill 3', value: 0 },
				{ name: 'Skill 4', value: 0 },
				{ name: 'Skill 5', value: 0 },
			]

	const option = {
		tooltip: {
			trigger: 'item', // Quay lại dùng item để hover vào vùng màu xanh là bắt được sự kiện
			backgroundColor: 'rgba(255, 255, 255, 0.95)', // Thêm nền trắng cho dễ đọc
			borderColor: '#E5E7EB',
			borderWidth: 1,
			padding: [10, 15],
			textStyle: {
				color: '#1F2937', // Màu chữ đậm
			},
			extraCssText: 'box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border-radius: 8px;',
			formatter: function (params) {
				// params.data.value sẽ là mảng [100, 100, 100]
				// Chúng ta sẽ lấy dữ liệu gốc từ chartData để hiển thị list

				if (!hasData) return 'No data'

				let html = `<div style="margin-bottom: 8px; font-weight: 600; color: #111827; border-bottom: 1px solid #E5E7EB; padding-bottom: 4px;">
                        Skill Overview
                    </div>`

				// Duyệt qua từng skill trong dữ liệu gốc để tạo danh sách
				chartData.forEach((skill, index) => {
					// Lấy màu (ví dụ: điểm cao thì xanh đậm, thấp thì nhạt hoặc dùng 1 màu)
					const dotColor = '#3B82F6'

					html += `
                <div style="display: flex; align-items: center; justify-content: space-between; min-width: 160px; margin-top: 6px; font-size: 13px;">
                    <span style="display: flex; align-items: center;">
                        <span style="display:inline-block; margin-right:6px; border-radius:50%; width:8px; height:8px; background-color:${dotColor};"></span>
                        <span style="color: #4B5563">${skill.name}</span>
                    </span>
                    <span style="font-weight: 600; color: #111827; margin-left: 12px;">
                        ${skill.value}% <span style="font-weight: normal; color: #9CA3AF; font-size: 11px;">(${skill.count || 0})</span>
                    </span>
                </div>
            `
				})

				return html
			},
		},
		radar: {
			indicator: chartData.map((item) => ({
				name: item.name,
				max: 100,
			})),
			splitNumber: 4,
			name: {
				textStyle: {
					color: '#4B5563',
					fontSize: 12,
				},
			},
			splitArea: {
				areaStyle: {
					color: ['rgba(59, 130, 246, 0.05)', 'rgba(59, 130, 246, 0.1)'],
				},
			},
			axisLine: {
				lineStyle: {
					color: '#E5E7EB',
				},
			},
			splitLine: {
				lineStyle: {
					color: '#E5E7EB',
				},
			},
		},
		series: [
			{
				type: 'radar',
				data: [
					{
						value: chartData.map((item) => item.value),
						name: 'Skill Level',
						areaStyle: {
							color: hasData
								? 'rgba(59, 130, 246, 0.2)'
								: 'rgba(229, 231, 235, 0.2)',
						},
						lineStyle: {
							color: hasData ? '#3B82F6' : '#E5E7EB',
							width: 2,
						},
						itemStyle: {
							color: hasData ? '#3B82F6' : '#E5E7EB',
						},
					},
				],
			},
		],
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

watch(
	() => props.data,
	() => {
		if (chartInstance) {
			initChart()
		}
	},
	{ deep: true },
)

onUnmounted(() => {
	if (chartInstance) {
		chartInstance.dispose()
	}
	window.removeEventListener('resize', resizeChart)
})
</script>
