<template>
  <Dialog
    :model-value="props.modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    :options="{
      title: isEdit ? __('Edit Candidate') : __('Add New Candidate'),
      size: 'lg'
    }"
  >
    <template #body>
      <div class="p-6">
        <!-- Loading State -->
        <div v-if="loading" class="space-y-4">
          <div class="animate-pulse">
            <div class="h-4 bg-gray-300 rounded mb-2"></div>
            <div class="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
            <div class="h-4 bg-gray-300 rounded mb-2"></div>
            <div class="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>

        <!-- Form Content -->
        <form v-else @submit.prevent="submitForm" class="space-y-6">
          <!-- Basic Information -->
          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"/>
              </svg>
              Thông tin cơ bản
            </h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Tên đầy đủ <span class="text-red-500">*</span>
                </label>
                <FormControl
                  type="text"
                  v-model="formData.full_name"
                  placeholder="Nhập tên đầy đủ"
                  :error="validationErrors?.full_name"
                  required
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Email <span class="text-red-500">*</span>
                </label>
                <FormControl
                  type="email"
                  v-model="formData.email"
                  placeholder="Nhập địa chỉ email"
                  :error="validationErrors?.email"
                  required
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Số điện thoại
                </label>
                <FormControl
                  type="tel"
                  v-model="formData.phone"
                  placeholder="Nhập số điện thoại"
                  :error="validationErrors?.phone"
                />
              </div>
              
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Chức danh/Vị trí
                </label>
                <FormControl
                  type="text"
                  v-model="formData.headline"
                  placeholder="VD: Senior Software Engineer"
                />
              </div>
            </div>
          </div>

          <!-- Professional Information -->
          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z" clip-rule="evenodd"/>
              </svg>
              Thông tin nghề nghiệp
            </h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Nguồn
                </label>
                <FormControl
                  type="select"
                  v-model="formData.source"
                  :options="sourceOptions"
                  placeholder="Chọn nguồn"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Trạng thái
                </label>
                <FormControl
                  type="select"
                  v-model="formData.status"
                  :options="statusOptions"
                  placeholder="Chọn trạng thái"
                />
              </div>
              
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Kỹ năng
                </label>
                <div class="space-y-2">
                  <div class="flex flex-wrap gap-2">
                    <span
                      v-for="(skill, index) in formData.skills"
                      :key="index"
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                    >
                      {{ skill }}
                      <button
                        type="button"
                        @click="removeSkill(index)"
                        class="ml-1 h-4 w-4 rounded-full inline-flex items-center justify-center hover:bg-blue-200"
                      >
                        <svg class="h-2 w-2" fill="currentColor" viewBox="0 0 8 8">
                          <path d="M0 0L8 8M8 0L0 8" stroke="currentColor" stroke-width="1"/>
                        </svg>
                      </button>
                    </span>
                  </div>
                  <div class="flex gap-2">
                    <FormControl
                      type="text"
                      v-model="newSkill"
                      placeholder="Nhập kỹ năng và nhấn Enter"
                      @keyup.enter.stop="addSkill"
                      @keydown.enter.prevent
                      class="flex-1"
                    />
                    <Button
                      type="button"
                      variant="outline"
                      @click="addSkill"
                      :disabled="!newSkill.trim()"
                      class="px-3"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                      </svg>
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Additional Information -->
          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
              </svg>
              Thông tin bổ sung
            </h3>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  URL CV
                </label>
                <FormControl
                  type="url"
                  v-model="formData.cv_original_url"
                  placeholder="https://example.com/cv.pdf"
                  :error="validationErrors?.cv_original_url"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Tóm tắt AI
                </label>
                <FormControl
                  type="textarea"
                  v-model="formData.ai_summary"
                  placeholder="Tóm tắt thông tin ứng viên bằng AI..."
                  :rows="4"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Cài đặt email
                </label>
                <div class="flex items-center">
                  <FormControl
                    type="checkbox"
                    v-model="formData.email_opt_out"
                    class="mr-2"
                  />
                  <label class="text-sm text-gray-700">
                    Từ chối email marketing
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Form Actions -->
          <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
            <Button
              variant="outline"
              @click="cancelEdit"
              :disabled="saving"
            >
              Hủy
            </Button>
            <Button
              type="submit"
              variant="solid"
              :loading="saving"
              :disabled="!isFormValid"
            >
              {{ isEdit ? 'Cập nhật' : 'Tạo mới' }}
            </Button>
          </div>
        </form>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { Dialog, Button, FormControl } from 'frappe-ui'
import { validateCandidateForm, processSkills, skillsToString } from '../../services/candidateService'

// Translation helper function
const __ = (text) => text

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  candidate: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  },
  saving: {
    type: Boolean,
    default: false
  },
  filterOptions: {
    type: Object,
    default: () => ({
      status: [],
      source: [],
      skills: []
    })
  }
})

// Debug log removed

// Emits
const emit = defineEmits([
  'update:modelValue',
  'save-candidate',
  'cancel'
])

// Refs
const formRef = ref(null)
const validationErrors = ref({})
const newSkill = ref('')

// Helper functions are imported directly

// Form data
const formData = ref({
  full_name: '',
  email: '',
  phone: '',
  headline: '',
  source: 'MANUAL',
  status: 'NEW',
  skills: [],
  cv_original_url: '',
  ai_summary: '',
  email_opt_out: 0
})

// Computed
const isEdit = computed(() => !!props.candidate)

const statusOptions = computed(() => {
  try {
    const baseOptions = [
      { label: 'Mới', value: 'NEW' },
      { label: 'Đã tìm thấy', value: 'SOURCED' },
      { label: 'Đang chăm sóc', value: 'NURTURING' },
      { label: 'Đã tương tác', value: 'ENGAGED' },
      { label: 'Đã lưu trữ', value: 'ARCHIVED' }
    ]
    
    const filterOptions = props.filterOptions || {}
    const statusFromAPI = filterOptions.status || []
    
    if (Array.isArray(statusFromAPI)) {
      return [...baseOptions, ...statusFromAPI]
    }
    
    return baseOptions
  } catch (error) {
    console.error('Error in statusOptions:', error)
    return [
      { label: 'Mới', value: 'NEW' },
      { label: 'Đã tìm thấy', value: 'SOURCED' },
      { label: 'Đang chăm sóc', value: 'NURTURING' },
      { label: 'Đã tương tác', value: 'ENGAGED' },
      { label: 'Đã lưu trữ', value: 'ARCHIVED' }
    ]
  }
})

const sourceOptions = computed(() => {
  try {
    const baseOptions = [
      { label: 'Thủ công', value: 'MANUAL' },
      { label: 'LinkedIn', value: 'LINKEDIN' },
      { label: 'Website', value: 'WEBSITE' },
      { label: 'Giới thiệu', value: 'REFERRAL' },
      { label: 'Job Board', value: 'JOB_BOARD' }
    ]
    
    const filterOptions = props.filterOptions || {}
    const sourceFromAPI = filterOptions.source || []
    
    if (Array.isArray(sourceFromAPI)) {
      return [...baseOptions, ...sourceFromAPI]
    }
    
    return baseOptions
  } catch (error) {
    console.error('Error in sourceOptions:', error)
    return [
      { label: 'Thủ công', value: 'MANUAL' },
      { label: 'LinkedIn', value: 'LINKEDIN' },
      { label: 'Website', value: 'WEBSITE' },
      { label: 'Giới thiệu', value: 'REFERRAL' },
      { label: 'Job Board', value: 'JOB_BOARD' }
    ]
  }
})

const availableSkills = computed(() => {
  try {
    const baseSkills = [
      'JavaScript',
      'Python', 
      'Java',
      'React',
      'Vue.js',
      'Node.js',
      'SQL',
      'HTML/CSS',
      'TypeScript',
      'Angular',
      'AWS',
      'Docker',
      'Kubernetes'
    ]
    
    const filterOptions = props.filterOptions || {}
    const skillsFromAPI = filterOptions.skills || []
    
    if (Array.isArray(skillsFromAPI)) {
      // Convert API skills to strings if they're objects
      const apiSkillsStrings = skillsFromAPI.map(skill => 
        typeof skill === 'string' ? skill : (skill.label || skill.value || skill)
      )
      return [...baseSkills, ...apiSkillsStrings].filter((skill, index, arr) => 
        arr.indexOf(skill) === index // Remove duplicates
      )
    }
    
    return baseSkills
  } catch (error) {
    console.error('Error in availableSkills:', error)
    return [
      'JavaScript',
      'Python',
      'Java',
      'React',
      'Vue.js',
      'Node.js',
      'SQL',
      'HTML/CSS'
    ]
  }
})

const isFormValid = computed(() => {
  const hasName = !!formData.value.full_name?.trim()
  const hasEmail = !!formData.value.email?.trim()
  const hasNoErrors = Object.keys(validationErrors.value || {}).length === 0
  
  const result = hasName && hasEmail && hasNoErrors
  console.log('isFormValid check:', { hasName, hasEmail, hasNoErrors, result })
  
  return result
})

// Validation rules
const rules = {
  required: (value) => !!value?.trim() || 'Trường này là bắt buộc',
  email: (value) => {
    if (!value) return true
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return pattern.test(value) || 'Email không hợp lệ'
  },
  phone: (value) => {
    if (!value) return true
    const pattern = /^[+\d\s\-()]+$/
    return pattern.test(value) || 'Số điện thoại không hợp lệ'
  },
  url: (value) => {
    if (!value) return true
    try {
      new URL(value)
      return true
    } catch {
      return 'URL không hợp lệ'
    }
  }
}

// Methods
const resetForm = () => {
  try {
    formData.value = {
      full_name: '',
      email: '',
      phone: '',
      headline: '',
      source: 'MANUAL',
      status: 'NEW',
      skills: [],
      cv_original_url: '',
      ai_summary: '',
      email_opt_out: 0
    }
    validationErrors.value = {}
  } catch (error) {
    console.error('Error in resetForm:', error)
  }
}

const loadCandidateData = () => {
  try {
    if (props.candidate) {
      formData.value = {
        full_name: props.candidate.full_name || '',
        email: props.candidate.email || '',
        phone: props.candidate.phone || '',
        headline: props.candidate.headline || '',
        source: props.candidate.source || 'MANUAL',
        status: props.candidate.status || 'NEW',
        skills: processSkills(props.candidate.skills) || [],
        cv_original_url: props.candidate.cv_original_url || '',
        ai_summary: props.candidate.ai_summary || '',
        email_opt_out: props.candidate.email_opt_out || 0
      }
    } else {
      resetForm()
    }
  } catch (error) {
    console.error('Error in loadCandidateData:', error)
    resetForm()
  }
}

const validateForm = () => {
  try {
    validationErrors.value = {}
    
    // Chỉ check basic validation
    if (!formData.value.full_name?.trim()) {
      validationErrors.value.full_name = 'Tên đầy đủ là bắt buộc'
      return false
    }
    
    if (!formData.value.email?.trim()) {
      validationErrors.value.email = 'Email là bắt buộc'
      return false
    }
    
    // Check email format
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailPattern.test(formData.value.email)) {
      validationErrors.value.email = 'Email không hợp lệ'
      return false
    }
    
    return true
  } catch (error) {
    console.error('Error in validateForm:', error)
    validationErrors.value = {}
    return true // Allow form to proceed if validation fails
  }
}

// Prevent double submit
let isSubmitting = false

const submitForm = async () => {
  console.log('=== SUBMIT FORM CALLED ===')
  
  // Prevent double submit
  if (isSubmitting) {
    console.log('Already submitting, ignoring duplicate call')
    return
  }
  
  console.log('formData:', formData.value)
  
  const isValid = validateForm()
  console.log('validateForm result:', isValid)
  console.log('validationErrors:', validationErrors.value)
  
  if (!isValid) {
    console.log('Form validation failed, stopping submit')
    return
  }
  
  console.log('Form validation passed, proceeding...')
  
  try {
    isSubmitting = true
    
    // Prepare data for submission
    const submitData = {
      ...formData.value,
      skills: skillsToString(formData.value.skills)
    }
    
    console.log('Emitting save-candidate with:', submitData)
    emit('save-candidate', submitData)
  } catch (error) {
    console.error('Form submission error:', error)
  } finally {
    // Reset submitting flag after a delay
    setTimeout(() => {
      isSubmitting = false
    }, 1000)
  }
}

const cancelEdit = () => {
  resetForm()
  emit('cancel')
  emit('update:modelValue', false)
}

// Skill management methods
const addSkill = (event) => {
  // Prevent form submission if called from Enter key
  if (event) {
    event.preventDefault()
    event.stopPropagation()
  }
  
  if (newSkill.value && newSkill.value.trim()) {
    const skill = newSkill.value.trim()
    if (!formData.value.skills.includes(skill)) {
      formData.value.skills.push(skill)
    }
    newSkill.value = ''
  }
}

const removeSkill = (index) => {
  formData.value.skills.splice(index, 1)
}

// Watch for modal open/close
watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    nextTick(() => {
      loadCandidateData()
    })
  } else {
    // Small delay to allow modal animation
    setTimeout(resetForm, 300)
  }
})

// Watch for candidate changes
watch(() => props.candidate, () => {
  if (props.modelValue) {
    loadCandidateData()
  }
}, { deep: true })
</script>

<style scoped>
.candidate-edit-modal {
  max-height: 90vh;
}

/* Form styling improvements */
:deep(.form-control) {
  border-radius: 8px;
}

:deep(.form-control:focus-within) {
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

/* Textarea styling */
:deep(.form-control textarea) {
  min-height: 80px;
}
</style> 