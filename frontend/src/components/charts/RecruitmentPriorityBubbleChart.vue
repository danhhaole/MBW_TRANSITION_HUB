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

    // 1. TRANSFORM DATA: Chuyển dữ liệu Raw từ API sang format ECharts
    let chartData = []
    
    if (props.data && props.data.length > 0) {
        chartData = props.data.map(item => {
            // Map Y (1->Low/0, 2->Medium/1, 3->High/2)
            const yIndex = (item.y || 1) - 1
            const readinessLevels = ['Low', 'Medium', 'High']
            const readinessLabel = readinessLevels[yIndex] || 'Unknown'

            // Map Color
            const colorMap = {
                'Low': '#9CA3AF',    // Gray-400
                'Medium': '#F59E0B', // Amber-500
                'High': '#10B981'    // Emerald-500
            }

            return {
                name: item.talent_id, // Hiển thị ID hoặc Tên
                // ECharts Value: [X, Y, Size]
                value: [
                    item.x,       // Timeline (Days)
                    yIndex,       // Y Index (0, 1, 2)
                    item.size     // Bubble Size (Score)
                ],
                readinessLabel: readinessLabel,
                timelineLabel: `${item.x} days`,
                color: colorMap[readinessLabel] || '#3B82F6',
                
                // Lưu lại toàn bộ dữ liệu gốc để hiển thị tooltip
                raw: item 
            }
        })
    } else {
        // Dữ liệu giả khi không có data
        chartData = [{ 
            name: 'No Data', 
            value: [0, 0, 0], 
            readinessLabel: 'Low', 
            timelineLabel: 'Immediate', 
            color: '#E5E7EB',
            raw: {} 
        }]
    }

    const option = {
        tooltip: {
            trigger: 'item',
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            borderColor: '#E5E7EB',
            textStyle: { color: '#374151' },
            // Custom Tooltip hiển thị chi tiết chỉ số tương tác
            formatter: (params) => {
                if (!params.data.raw || !params.data.raw.talent_id) return 'No data'
                const d = params.data.raw
                return `
                    <div class="font-bold text-gray-900 mb-1">${d.talent_id}</div>
                    <div class="text-xs text-gray-500 mb-2">Channel: <span class="font-medium">${d.top_channel}</span></div>
                    <div class="grid grid-cols-2 gap-x-4 gap-y-1 text-xs">
                        <div>Readiness: <span style="color:${params.data.color}; font-weight:bold">${params.data.readinessLabel}</span></div>
                        <div>Timeline: <b>${d.x} days</b></div>
                        <div>Score: <b>${d.size}</b></div>
                        <div>Conversion: <b>${d.conversion}</b></div>
                    </div>
                    <div class="mt-2 pt-2 border-t border-gray-100 flex justify-between text-xs text-gray-400">
                        <span>👆 ${d.click}</span>
                        <span>👀 ${d.open}</span>
                        <span>↩️ ${d.reply}</span>
                        <span>👁️ ${d.visit}</span>
                    </div>
                `
            }
        },
        grid: {
            left: '60px',
            right: '4%',
            bottom: '40px',
            top: '30px',
            containLabel: true
        },
        xAxis: {
            name: 'Timeline (Days)',
            nameLocation: 'middle',
            nameGap: 30,
            type: 'value',
            min: 0,
            max: 100, // Có thể điều chỉnh max tùy dữ liệu
            splitLine: { lineStyle: { type: 'dashed' } }
        },
        yAxis: {
            name: 'Readiness',
            type: 'category',
            data: ['Low', 'Medium', 'High'],
            splitLine: { show: true, lineStyle: { type: 'dashed' } },
            axisLine: { show: false },
            axisTick: { show: false }
        },
        series: [
            {
                type: 'scatter',
                symbolSize: (data) => {
                    // Scale kích thước bubble: Score càng lớn bubble càng to
                    // Giới hạn min=10, max=50 để không quá bé hoặc quá to
                    const size = Math.sqrt(data[2]) * 4
                    return Math.min(Math.max(size, 8), 60)
                },
                data: chartData.map(item => ({
                    value: item.value,
                    name: item.name,
                    readinessLabel: item.readinessLabel,
                    timelineLabel: item.timelineLabel,
                    itemStyle: {
                        color: item.color,
                        opacity: 0.6,
                        shadowBlur: 2,
                        shadowColor: 'rgba(0,0,0,0.1)'
                    },
                    raw: item.raw // Truyền raw data xuống series item
                })),
                emphasis: {
                    focus: 'series',
                    itemStyle: {
                        opacity: 1,
                        shadowBlur: 10,
                        shadowColor: 'rgba(0,0,0,0.2)'
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
        initChart() // Re-render khi data thay đổi
    }
}, { deep: true })

onUnmounted(() => {
    if (chartInstance) {
        chartInstance.dispose()
    }
    window.removeEventListener('resize', resizeChart)
})
</script>
