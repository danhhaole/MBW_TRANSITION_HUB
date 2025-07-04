<template>
  <div class="pool-config">
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="data.skills"
          label="Kỹ năng"
          placeholder="React, NodeJS, Python..."
          variant="outlined"
          density="compact"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="data.experience"
          label="Số năm kinh nghiệm"
          placeholder="3+"
          type="number"
          variant="outlined"
          density="compact"
        />
      </v-col>
    </v-row>
    
    <v-row>
      <v-col cols="12" md="6">
        <v-select
          v-model="data.location"
          :items="locations"
          label="Địa điểm"
          variant="outlined"
          density="compact"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-select
          v-model="data.level"
          :items="levels"
          label="Cấp độ"
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
  skills: '',
  experience: '',
  location: '',
  level: '',
  ...props.modelValue
})

// Options
const locations = [
  'Hà Nội',
  'TP. Hồ Chí Minh',
  'Đà Nẵng',
  'Cần Thơ',
  'Hải Phòng'
]

const levels = [
  'Intern',
  'Fresher',
  'Junior',
  'Mid-level',
  'Senior',
  'Lead',
  'Manager'
]

// Watch for changes
watch(data, (newData) => {
  emit('update:modelValue', newData)
}, { deep: true })
</script> 