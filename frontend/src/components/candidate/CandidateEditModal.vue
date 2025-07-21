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
              {{ __('Basic Information') }}
            </h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Full Name') }} <span class="text-red-500">*</span>
                </label>
                <FormControl
                  type="text"
                  v-model="formData.full_name"
                  :placeholder="__('Enter full name')"
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
                  :placeholder="__('Enter email address')"
                  :error="validationErrors?.email"
                  required
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Phone Number') }}
                </label>
                <FormControl
                  type="tel"
                  v-model="formData.phone"
                  :placeholder="__('Enter phone number')"
                  :error="validationErrors?.phone"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Headline') }}
                </label>
                <FormControl
                  type="text"
                  v-model="formData.headline"
                  :placeholder="__('Enter current position/title')"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Avatar URL') }}
                </label>
                <FormControl
                  type="url"
                  v-model="formData.avatar"
                  :placeholder="__('Enter avatar URL')"
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
              {{ __('Professional Information') }}
            </h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Source') }}
                </label>
                <FormControl
                  type="select"
                  v-model="formData.source"
                  :options="sourceOptions"
                  :placeholder="__('Select source')"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Status') }}
                </label>
                <FormControl
                  type="select"
                  v-model="formData.status"
                  :options="statusOptions"
                  :placeholder="__('Select status')"
                />
              </div>
              
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Skills') }}
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
                      :placeholder="__('Enter skill and press Enter')"
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
              {{ __('Additional Information') }}
            </h3>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('AI Summary') }}
                </label>
                <FormControl
                  type="textarea"
                  v-model="formData.ai_summary"
                  :placeholder="__('Enter AI-generated summary')"
                  :rows="4"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Email Settings') }}
                </label>
                <div class="flex items-center">
                  <FormControl
                    type="checkbox"
                    v-model="formData.email_opt_out"
                    class="mr-2"
                  />
                  <label class="text-sm text-gray-700">
                    {{ __('Opt out from marketing emails') }}
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
              {{ __('Cancel') }}
            </Button>
            <Button
              type="submit"
              variant="solid"
              :loading="saving"
              :disabled="!isFormValid"
            >
              {{ isEdit ? __('Update') : __('Create') }}
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
  avatar: '',
  source: 'Manual',
  status: 'NEW',
  skills: [],
  ai_summary: '',
  email_opt_out: false
})

// Computed
const isEdit = computed(() => !!props.candidate)

const statusOptions = computed(() => {
  try {
    const baseOptions = [
      { label: 'NEW', value: 'NEW' },
      { label: 'SOURCED', value: 'SOURCED' },
      { label: 'NURTURING', value: 'NURTURING' },
      { label: 'ENGAGED', value: 'ENGAGED' },
      { label: 'ARCHIVED', value: 'ARCHIVED' }
    ]
    
    const filterOptions = props.filterOptions || {}
    const statusFromAPI = filterOptions.status || []
    
    if (Array.isArray(statusFromAPI)) {
      return [...statusFromAPI]
    }
    
    return baseOptions
  } catch (error) {
    console.error('Error in statusOptions:', error)
    return [
      { label: 'NEW', value: 'NEW' },
      { label: 'SOURCED', value: 'SOURCED' },
      { label: 'NURTURING', value: 'NURTURING' },
      { label: 'ENGAGED', value: 'ENGAGED' },
      { label: 'ARCHIVED', value: 'ARCHIVED' }
    ]
  }
})

const sourceOptions = computed(() => {
  try {
    const baseOptions = [
      { label: 'Thủ công', value: 'Manual' },
      { label: 'LinkedIn', value: 'LinkedIn' },
      { label: 'Website', value: 'Website' },
      { label: 'Giới thiệu', value: 'Referral' },
      { label: 'Job Board', value: 'Job Board' },
      { label: 'ATS Import', value: 'ATS Import' },
      { label: 'Email', value: 'Email' }
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
      { label: 'Thủ công', value: 'Manual' },
      { label: 'LinkedIn', value: 'LinkedIn' },
      { label: 'Website', value: 'Website' },
      { label: 'Giới thiệu', value: 'Referral' },
      { label: 'Job Board', value: 'Job Board' }
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
      avatar: '',
      source: 'Manual',
      status: 'NEW',
      skills: [],
      ai_summary: '',
      email_opt_out: false
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
        avatar: props.candidate.avatar || '',
        source: props.candidate.source || 'Manual',
        status: props.candidate.status || 'NEW',
        skills: processSkills(props.candidate.skills) || [],
        ai_summary: props.candidate.ai_summary || '',
        email_opt_out: !!props.candidate.email_opt_out
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