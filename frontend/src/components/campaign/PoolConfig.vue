<template>
  <div class="pool-config space-y-4">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">
        {{ __('Select a talent pool') }}
      </label>
      <Autocomplete
        v-model="data.selectedSegment"
        :options="segmentOptions"
        :placeholder="__('Select a talent pool')"
        @change="handleSegmentChange"
      />
    </div>
    
    <!-- <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Skills (optional)') }}
        </label>
        <FormControl
          v-model="data.skills"
          type="text"
          :placeholder="__('React, NodeJS, Python...')"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Years of experience (optional)') }}
        </label>
        <FormControl
          v-model="data.experience"
          type="number"
          :placeholder="__('3+')"
        />
      </div>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Location (optional)') }}
        </label>
        <FormControl
          v-model="data.location"
          type="select"
          :options="locationOptions"
          :placeholder="__('Select a location')"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Level (optional)') }}
        </label>
        <FormControl
          v-model="data.level"
          type="select"
          :options="levelOptions"
          :placeholder="__('Select a level')"
        />
      </div>
    </div> -->
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { FormControl, Autocomplete, call } from 'frappe-ui'
import { useTalentSegmentStore } from '@/stores/talentSegment'

const talentSegmentStore = useTalentSegmentStore()

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
const isUpdatingFromParent = ref(false)

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
    const result = await call('frappe.client.get_list', {
      doctype: 'Mira Segment',
      fields: ['name', 'title', 'description', 'candidate_count'],
      limit_page_length: 100
    })
    if (result && result.length) {
      segments.value = result
    }
  } catch (error) {
    console.error('Error loading talent segments:', error)
  } finally {
    loadingSegments.value = false
  }
}

// Handle segment change
const handleSegmentChange = (value) => {
  console.log("Segment changed:", value)
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
  // Skip if updating from parent to prevent infinite loop
  if (isUpdatingFromParent.value) {
    return
  }
  
  // Find selected segment and get candidate count
  let candidateCount = 0
  if (newData.selectedSegment) {
    const segmentValue = newData.selectedSegment.value || newData.selectedSegment
    const selectedSeg = segments.value.find(s => s.name === segmentValue)
    if (selectedSeg) {
      candidateCount = selectedSeg.candidate_count || 0
      console.log("Selected segment candidate count:", candidateCount)
    }
  }
  
  console.log("newData", {
    ...newData,
    selectedSegment: newData.selectedSegment.value || newData.selectedSegment,
    candidateCount: candidateCount
  })
  
  emit('update:modelValue', {
    ...newData,
    selectedSegment: newData.selectedSegment.value || newData.selectedSegment,
    candidateCount: candidateCount
  })
}, { deep: true })

// Watch for modelValue changes from parent (e.g., clear segment)
watch(() => props.modelValue, (newValue) => {
  isUpdatingFromParent.value = true
  
  // Reset data when parent clears
  if (!newValue || Object.keys(newValue).length === 0) {
    data.value = {
      selectedSegment: '',
      skills: '',
      experience: '',
      location: '',
      level: ''
    }
  } else {
    // Update data from parent
    data.value = {
      selectedSegment: '',
      skills: '',
      experience: '',
      location: '',
      level: '',
      ...newValue
    }
  }
  
  // Reset flag after Vue's next tick
  setTimeout(() => {
    isUpdatingFromParent.value = false
  }, 0)
}, { deep: true })

// Lifecycle
onMounted(() => {
  loadTalentSegments()
})
</script> 