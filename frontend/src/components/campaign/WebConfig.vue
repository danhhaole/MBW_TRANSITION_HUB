<template>
  <div class="web-config space-y-4">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">
        Từ khóa tìm kiếm
      </label>
      <FormControl
        v-model="data.keywords"
        type="text"
        placeholder="Senior Golang Developer Hanoi"
      />
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">
        Nguồn thu thập
      </label>
      <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
        <label
          v-for="source in webSources"
          :key="source.value"
          class="flex items-center space-x-2 cursor-pointer"
        >
          <input
            type="checkbox"
            :value="source.value"
            v-model="data.sources"
            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
          <span class="text-sm text-gray-700">{{ source.text }}</span>
        </label>
      </div>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Số lượng tối đa
        </label>
        <FormControl
          v-model="data.maxResults"
          type="number"
          placeholder="100"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Khoảng thời gian
        </label>
        <FormControl
          v-model="data.timeRange"
          type="select"
          :options="timeRangeOptions"
          placeholder="Chọn khoảng thời gian"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { FormControl } from 'frappe-ui'

// Props & Emits
const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue'])

// Data
const data = ref({
  keywords: '',
  sources: [],
  maxResults: 100,
  timeRange: '',
  ...props.modelValue
})

// Options
const webSources = [
  { text: 'LinkedIn', value: 'linkedin' },
  { text: 'TopCV', value: 'topcv' },
  { text: 'VietnamWorks', value: 'vietnamworks' },
  { text: 'CareerBuilder', value: 'careerbuilder' },
  { text: 'Indeed', value: 'indeed' },
  { text: 'GitHub', value: 'github' }
]

const timeRanges = [
  { title: 'Tuần qua', value: '7d' },
  { title: 'Tháng qua', value: '30d' },
  { title: '3 tháng qua', value: '90d' },
  { title: '6 tháng qua', value: '180d' },
  { title: 'Năm qua', value: '365d' }
]

// Computed options for select components
const timeRangeOptions = computed(() => {
  return timeRanges.map(range => ({
    label: range.title,
    value: range.value
  }))
})

// Watch for changes
watch(data, (newData) => {
  emit('update:modelValue', newData)
}, { deep: true })
</script> 