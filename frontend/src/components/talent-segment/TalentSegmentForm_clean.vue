<template>
  <div class="max-w-2xl mx-auto">
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- Title -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Segment Name') }} <span class="text-red-500">*</span>
        </label>
        <input
          v-model="formData.title"
          type="text"
          :placeholder="__('Enter segment name...')"
          class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          :class="{ 'border-red-500': errors.title }"
          maxlength="100"
          required
        />
        <p v-if="errors.title" class="mt-1 text-sm text-red-600">{{ __(errors.title) }}</p>
        <p class="mt-1 text-sm text-gray-500">{{ __('This name will be displayed in the segment list') }}</p>
      </div>

      <!-- Description -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Description') }}
        </label>
        <textarea
          v-model="formData.description"
          rows="3"
          :placeholder="__('Detailed description of this segment...')"
          class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          :class="{ 'border-red-500': errors.description }"
          maxlength="500"
        />
        <p v-if="errors.description" class="mt-1 text-sm text-red-600">{{ __(errors.description) }}</p>
        <p class="mt-1 text-sm text-gray-500">{{ __('Description will help others understand the purpose of the segment') }}</p>
      </div>

      <!-- Type and Owner in a row -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Type -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Loại phân khúc <span class="text-red-500">*</span>
          </label>
          <select
            v-model="formData.type"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            :class="{ 'border-red-500': errors.type }"
            required
          >
            <option value="">Chọn loại phân khúc</option>
            <option v-for="option in typeOptions" :key="option.value" :value="option.value">
              {{ option.title }}
            </option>
          </select>
          <p v-if="errors.type" class="mt-1 text-sm text-red-600">{{ errors.type }}</p>
        </div>

        <!-- Owner -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Người quản lý
          </label>
          <select
            v-model="formData.owner_id"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            :class="{ 'border-red-500': errors.owner_id }"
          >
            <option value="">Chọn người quản lý</option>
            <option v-for="user in userOptions" :key="user.name" :value="user.name">
              {{ user.full_name }}
            </option>
          </select>
          <p v-if="errors.owner_id" class="mt-1 text-sm text-red-600">{{ errors.owner_id }}</p>
        </div>
      </div>

      <!-- Candidate Count (if editing) -->
      <div v-if="isEditing">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Số lượng ứng viên
        </label>
        <input
          v-model.number="formData.candidate_count"
          type="number"
          min="0"
          placeholder="0"
          class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          :class="{ 'border-red-500': errors.candidate_count }"
        />
        <p v-if="errors.candidate_count" class="mt-1 text-sm text-red-600">{{ errors.candidate_count }}</p>
        <p class="mt-1 text-sm text-gray-500">Số lượng ứng viên hiện tại trong phân khúc</p>
      </div>

      <!-- AI Configuration (only for DYNAMIC type) -->
      <div v-if="formData.type === 'DYNAMIC'" class="border border-gray-200 rounded-lg p-4">
        <div class="flex items-center mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
          <h4 class="text-lg font-medium text-gray-900">Cấu hình AI (Tùy chọn)</h4>
        </div>
        <p class="text-sm text-gray-600 mb-4">
          Cấu hình các tiêu chí để AI tự động phân loại ứng viên
        </p>
        
        <!-- Skills Selection -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Kỹ năng cần thiết
          </label>
          <div class="space-y-2">
            <div class="flex flex-wrap gap-2">
              <span
                v-for="(skill, index) in criteriaForm.skills"
                :key="index"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
              >
                {{ skill }}
                <button
                  type="button"
                  @click="removeSkill(index)"
                  class="ml-1.5 h-4 w-4 rounded-full inline-flex items-center justify-center text-blue-400 hover:bg-blue-200 hover:text-blue-500 focus:outline-none"
                >
                  <svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
                    <path stroke-linecap="round" stroke-width="1.5" d="m1 1 6 6m0-6-6 6" />
                  </svg>
                </button>
              </span>
            </div>
            <input
              v-model="newSkill"
              @keydown.enter.prevent="addSkill"
              type="text"
              placeholder="Nhập kỹ năng và nhấn Enter (VD: Java, Spring, React...)"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
        </div>

        <!-- Experience Years -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Kinh nghiệm làm việc
          </label>
          <div class="grid grid-cols-3 gap-3">
            <select
              v-model="criteriaForm.experienceOperator"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option value=">=">&gt;= Ít nhất</option>
              <option value="=">=== Chính xác</option>
              <option value="<=">&lt;= Tối đa</option>
            </select>
            <div class="col-span-2">
              <input
                v-model.number="criteriaForm.experienceYears"
                type="number"
                min="0"
                max="50"
                placeholder="Số năm kinh nghiệm"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>
          </div>
        </div>

        <!-- Education Level -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Trình độ học vấn
          </label>
          <select
            v-model="criteriaForm.educationLevel"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option value="">Không yêu cầu</option>
            <option value="high_school">Trung học phổ thông</option>
            <option value="diploma">Cao đẳng</option>
            <option value="bachelor">Đại học</option>
            <option value="master">Thạc sĩ</option>
            <option value="phd">Tiến sĩ</option>
          </select>
        </div>

        <!-- Location -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Địa điểm làm việc mong muốn
          </label>
          <div class="space-y-2">
            <div class="flex flex-wrap gap-2">
              <span
                v-for="(location, index) in criteriaForm.locations"
                :key="index"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
              >
                {{ location }}
                <button
                  type="button"
                  @click="removeLocation(index)"
                  class="ml-1.5 h-4 w-4 rounded-full inline-flex items-center justify-center text-green-400 hover:bg-green-200 hover:text-green-500 focus:outline-none"
                >
                  <svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
                    <path stroke-linecap="round" stroke-width="1.5" d="m1 1 6 6m0-6-6 6" />
                  </svg>
                </button>
              </span>
            </div>
            <input
              v-model="newLocation"
              @keydown.enter.prevent="addLocation"
              type="text"
              placeholder="Nhập địa điểm và nhấn Enter (VD: Hà Nội, TP.HCM...)"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
        </div>

        <!-- Salary Range -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Mức lương tối thiểu (triệu VND)
            </label>
            <input
              v-model.number="criteriaForm.salaryMin"
              type="number"
              min="0"
              step="0.5"
              placeholder="VD: 15"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Mức lương tối đa (triệu VND)
            </label>
            <input
              v-model.number="criteriaForm.salaryMax"
              type="number"
              min="0"
              step="0.5"
              placeholder="VD: 30"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
        </div>
      </div>

      <!-- Form Actions -->
      <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
        <Button
          variant="outline"
          theme="gray"
          @click="handleCancel"
          :disabled="loading"
        >
          {{ __('Cancel') }}
        </Button>
        <Button
          variant="solid"
          theme="blue"
          type="submit"
          :loading="loading"
        >
          {{ isEditing ? __('Update') : __('Create') }}
        </Button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { Button } from 'frappe-ui'
import { talentSegmentService, userService } from '@/services/universalService'

// Translation helper function


// Props
const props = defineProps({
  segment: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['success', 'cancel'])

// Local state
const loading = ref(false)
const loadingUsers = ref(false)
const userOptions = ref([])
const errors = ref({})

// Form fields for new skills and locations
const newSkill = ref('')
const newLocation = ref('')

const formData = ref({
  title: '',
  description: '',
  type: 'MANUAL',
  owner_id: '',
  candidate_count: 0,
  criteria: '{}'
})

// Criteria form for better UX
const criteriaForm = ref({
  skills: [],
  experienceOperator: '>=',
  experienceYears: null,
  locations: [],
  educationLevel: '',
  salaryMin: null,
  salaryMax: null
})

// Type options
const typeOptions = [
  {
    title: 'Manual',
    value: 'MANUAL'
  },
  {
    title: 'Automatic (AI)',
    value: 'DYNAMIC'
  }
]

// Computed
const isEditing = computed(() => !!props.segment)

// Validation
const validateForm = () => {
  errors.value = {}
  
  if (!formData.value.title || formData.value.title.trim().length < 3) {
    errors.value.title = 'Segment name must be at least 3 characters'
  }
  
  if (formData.value.title && formData.value.title.length > 100) {
    errors.value.title = 'Segment name cannot exceed 100 characters'
  }
  
  if (formData.value.description && formData.value.description.length > 500) {
    errors.value.description = 'Description cannot exceed 500 characters'
  }
  
  if (!formData.value.type) {
    errors.value.type = 'Segment type is required'
  }
  
  if (formData.value.candidate_count < 0) {
    errors.value.candidate_count = 'Number of candidates must be >= 0'
  }
  
  return Object.keys(errors.value).length === 0
}

// Convert form to JSON criteria
const convertFormToCriteria = () => {
  const criteria = {}
  
  if (criteriaForm.value.skills?.length > 0) {
    criteria.skills = criteriaForm.value.skills
  }
  
  if (criteriaForm.value.experienceYears !== null && criteriaForm.value.experienceYears !== '') {
    criteria.experienceYears = `${criteriaForm.value.experienceOperator}${criteriaForm.value.experienceYears}`
  }
  
  if (criteriaForm.value.locations?.length > 0) {
    criteria.locations = criteriaForm.value.locations
  }
  
  if (criteriaForm.value.educationLevel) {
    criteria.educationLevel = criteriaForm.value.educationLevel
  }
  
  if (criteriaForm.value.salaryMin !== null || criteriaForm.value.salaryMax !== null) {
    const salaryRange = {}
    if (criteriaForm.value.salaryMin !== null && criteriaForm.value.salaryMin !== '') {
      salaryRange.min = criteriaForm.value.salaryMin
    }
    if (criteriaForm.value.salaryMax !== null && criteriaForm.value.salaryMax !== '') {
      salaryRange.max = criteriaForm.value.salaryMax
    }
    if (Object.keys(salaryRange).length > 0) {
      criteria.salaryRange = salaryRange
    }
  }
  
  return JSON.stringify(criteria)
}

// Convert JSON criteria to form
const parseCriteriaToForm = (criteriaJson) => {
  try {
    const criteria = JSON.parse(criteriaJson || '{}')
    
    criteriaForm.value = {
      skills: criteria.skills || [],
      experienceOperator: '>=',
      experienceYears: null,
      locations: criteria.locations || [],
      educationLevel: criteria.educationLevel || '',
      salaryMin: criteria.salaryRange?.min || null,
      salaryMax: criteria.salaryRange?.max || null
    }
    
    // Parse experience years
    if (criteria.experienceYears) {
      const expStr = criteria.experienceYears.toString()
      const match = expStr.match(/^([><=]+)(.+)$/)
      if (match) {
        criteriaForm.value.experienceOperator = match[1]
        criteriaForm.value.experienceYears = parseInt(match[2])
      }
    }
  } catch (error) {
    console.error('Error parsing criteria JSON:', error)
    criteriaForm.value = {
      skills: [],
      experienceOperator: '>=',
      experienceYears: null,
      locations: [],
      educationLevel: '',
      salaryMin: null,
      salaryMax: null
    }
  }
}

// Skills management
const addSkill = () => {
  if (newSkill.value.trim() && !criteriaForm.value.skills.includes(newSkill.value.trim())) {
    criteriaForm.value.skills.push(newSkill.value.trim())
    newSkill.value = ''
  }
}

const removeSkill = (index) => {
  criteriaForm.value.skills.splice(index, 1)
}

// Locations management
const addLocation = () => {
  if (newLocation.value.trim() && !criteriaForm.value.locations.includes(newLocation.value.trim())) {
    criteriaForm.value.locations.push(newLocation.value.trim())
    newLocation.value = ''
  }
}

const removeLocation = (index) => {
  criteriaForm.value.locations.splice(index, 1)
}

const resetForm = () => {
  formData.value = {
    title: '',
    description: '',
    type: 'MANUAL',
    owner_id: '',
    candidate_count: 0,
    criteria: '{}'
  }
  
  criteriaForm.value = {
    skills: [],
    experienceOperator: '>=',
    experienceYears: null,
    locations: [],
    educationLevel: '',
    salaryMin: null,
    salaryMax: null
  }
  
  errors.value = {}
}

const loadUserOptions = async () => {
  loadingUsers.value = true
  try {
    const result = await userService.getList({ fields: ['name', 'full_name', 'email'] })
    if (result.success) {
      userOptions.value = result.data
    }
  } catch (error) {
    console.error('Error loading users:', error)
  } finally {
    loadingUsers.value = false
  }
}

// Event handlers
const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }
  
  loading.value = true
  
  try {
    // Convert criteria form to JSON string
    formData.value.criteria = convertFormToCriteria()
    
    let result
    if (isEditing.value) {
      result = await talentSegmentService.update(props.segment.name, formData.value)
    } else {
      result = await talentSegmentService.create(formData.value)
    }
    
    if (result.success) {
      emit('success', result.data)
      resetForm()
    } else {
      throw new Error(result.message || 'Operation failed')
    }
  } catch (error) {
    console.error('Error saving segment:', error)
    // You might want to show an error toast here
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  emit('cancel')
  resetForm()
}

// Initialize form when segment prop changes
watch(() => props.segment, (newSegment) => {
  if (newSegment) {
    formData.value = {
      title: newSegment.title || '',
      description: newSegment.description || '',
      type: newSegment.type || 'MANUAL',
      owner_id: newSegment.owner_id || '',
      candidate_count: newSegment.candidate_count || 0,
      criteria: newSegment.criteria || '{}'
    }
    
    // Parse criteria to form
    parseCriteriaToForm(newSegment.criteria)
  } else {
    resetForm()
  }
}, { immediate: true })

// Load users on mount
onMounted(() => {
  loadUserOptions()
})
</script>

<style scoped>
/* Custom form styles */
.form-control:focus {
  @apply ring-2 ring-blue-500 border-blue-500;
}

.error-input {
  @apply border-red-500 ring-red-500;
}

/* Skill and location chips */
.chip {
  @apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium;
}

.chip-remove {
  @apply ml-1.5 h-4 w-4 rounded-full inline-flex items-center justify-center focus:outline-none;
}
</style>
