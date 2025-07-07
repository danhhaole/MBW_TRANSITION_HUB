<template>
  <div class="pool-config">
    <v-row>
      <v-col cols="12">
        <v-select
          v-model="data.selectedSegment"
          :items="segments"
          label="Chọn phân khúc nhân tài *"
          placeholder="Chọn phân khúc có sẵn..."
          variant="outlined"
          density="compact"
          :loading="loadingSegments"
          item-title="title"
          item-value="name"
          required
        />
      </v-col>
    </v-row>
    
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="data.skills"
          label="Kỹ năng (bổ sung)"
          placeholder="React, NodeJS, Python..."
          variant="outlined"
          density="compact"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="data.experience"
          label="Số năm kinh nghiệm (bổ sung)"
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
          label="Địa điểm (bổ sung)"
          variant="outlined"
          density="compact"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-select
          v-model="data.level"
          :items="levels"
          label="Cấp độ (bổ sung)"
          variant="outlined"
          density="compact"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { talentSegmentService } from '@/services/universalService'

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
  selectedSegment: '',
  skills: '',
  experience: '',
  location: '',
  level: '',
  ...props.modelValue
})

const segments = ref([])
const loadingSegments = ref(false)

// Load talent segments
const loadTalentSegments = async () => {
  loadingSegments.value = true
  try {
    const result = await talentSegmentService.getList({
      fields: ['name', 'title', 'description', 'candidate_count'],
      page_length: 100
    })
    if (result.success) {
      segments.value = result.data
    }
  } catch (error) {
    console.error('Error loading talent segments:', error)
  } finally {
    loadingSegments.value = false
  }
}

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

// Lifecycle
onMounted(() => {
  loadTalentSegments()
})
</script> 