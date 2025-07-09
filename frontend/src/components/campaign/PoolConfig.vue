<template>
  <div class="pool-config space-y-4">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">
        Chọn phân khúc nhân tài <span class="text-red-500">*</span>
      </label>
      <Autocomplete
        v-model="data.selectedSegment"
        :options="segmentOptions"
        placeholder="Chọn phân khúc có sẵn..."
        @change="handleSegmentChange"
      />
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Kỹ năng (bổ sung)
        </label>
        <FormControl
          v-model="data.skills"
          type="text"
          placeholder="React, NodeJS, Python..."
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Số năm kinh nghiệm (bổ sung)
        </label>
        <FormControl
          v-model="data.experience"
          type="number"
          placeholder="3+"
        />
      </div>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Địa điểm (bổ sung)
        </label>
        <FormControl
          v-model="data.location"
          type="select"
          :options="locationOptions"
          placeholder="Chọn địa điểm"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Cấp độ (bổ sung)
        </label>
        <FormControl
          v-model="data.level"
          type="select"
          :options="levelOptions"
          placeholder="Chọn cấp độ"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { FormControl, Autocomplete } from 'frappe-ui'
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

// Computed options for select components
const segmentOptions = computed(() => {
  return segments.value.map(segment => ({
    label: segment.title,
    value: segment.name,
    description: segment.description
  }))
})

const locationOptions = computed(() => {
  return locations.map(location => ({
    label: location,
    value: location
  }))
})

const levelOptions = computed(() => {
  return levels.map(level => ({
    label: level,
    value: level
  }))
})

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

// Handle segment change
const handleSegmentChange = (value) => {
  data.value.selectedSegment = value
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