<template>
  <div class="ats-config">
    <v-row>
      <v-col cols="12">
        <v-select
          v-model="data.atsSystem"
          :items="atsSystems"
          label="Hệ thống ATS"
          variant="outlined"
          density="compact"
        />
      </v-col>
    </v-row>
    
    <v-row>
      <v-col cols="12">
        <v-text-field
          v-model="data.jobPosition"
          label="Vị trí tuyển dụng"
          placeholder="Senior Java Developer"
          variant="outlined"
          density="compact"
        />
      </v-col>
    </v-row>
    
    <v-row>
      <v-col cols="12" md="6">
        <v-select
          v-model="data.status"
          :items="statuses"
          label="Trạng thái ứng viên"
          variant="outlined"
          density="compact"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="data.syncInterval"
          label="Tần suất đồng bộ (phút)"
          type="number"
          placeholder="60"
          variant="outlined"
          density="compact"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

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

// Watch for changes
watch(data, (newData) => {
  emit('update:modelValue', newData)
}, { deep: true })
</script> 