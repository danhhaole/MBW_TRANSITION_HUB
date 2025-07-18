<template>
  <div class="ats-config space-y-4">
    <!-- Display selected data source info -->
    <div v-if="selectedDataSource" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
      <h4 class="text-sm font-medium text-blue-900 mb-1">Nguồn đã chọn</h4>
      <div class="text-sm text-blue-700">
        <div class="font-medium">{{ selectedDataSource.source_name }}</div>
        <div class="text-xs">{{ selectedDataSource.source_type }} • {{ selectedDataSource.description || 'Không có mô tả' }}</div>
      </div>
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">
        {{ __('Job Position') }}
      </label>
      <FormControl
        v-model="data.jobPosition"
        type="text"
        placeholder="Senior Java Developer"
      />
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Candidate Status') }}
        </label>
        <FormControl
          v-model="data.status"
          type="select"
          :options="statusOptions"
          placeholder="Chọn trạng thái"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Sync Frequency (minutes)') }}
        </label>
        <FormControl
          v-model="data.syncInterval"
          type="number"
          placeholder="60"
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
  },
  selectedDataSource: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue'])

// Data
const data = ref({
  jobPosition: '',
  status: '',
  syncInterval: 60,
  ...props.modelValue
})

// Options
const statuses = [
  'Applied',
  'Screening',
  'Interview',
  'Offer',
  'Rejected',
  'Withdrawn'
]

// Computed options for select components
const statusOptions = computed(() => {
  return statuses.map(status => ({
    label: status,
    value: status
  }))
})

// Watch for changes
watch(data, (newData) => {
  emit('update:modelValue', newData)
}, { deep: true })
</script> 