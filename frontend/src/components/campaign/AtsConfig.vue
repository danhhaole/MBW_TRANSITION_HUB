<template>
  <div class="ats-config space-y-4">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">
        Hệ thống ATS
      </label>
      <FormControl
        v-model="data.atsSystem"
        type="select"
        :options="atsSystemOptions"
        placeholder="Chọn hệ thống ATS"
      />
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">
        Vị trí tuyển dụng
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
          Trạng thái ứng viên
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
          Tần suất đồng bộ (phút)
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
  }
})

const emit = defineEmits(['update:modelValue'])

// Data
const data = ref({
  atsSystem: '',
  jobPosition: '',
  status: '',
  syncInterval: 60,
  ...props.modelValue
})

// Options
const atsSystems = [
  'Greenhouse',
  'Lever',
  'Workday',
  'BambooHR',
  'JazzHR',
  'SmartRecruiters'
]

const statuses = [
  'Applied',
  'Screening',
  'Interview',
  'Offer',
  'Rejected',
  'Withdrawn'
]

// Computed options for select components
const atsSystemOptions = computed(() => {
  return atsSystems.map(system => ({
    label: system,
    value: system
  }))
})

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