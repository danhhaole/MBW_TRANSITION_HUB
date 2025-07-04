<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="700px"
    persistent
    scrollable
  >
    <v-card class="candidate-edit-modal">
      <!-- Header -->
      <v-card-title class="d-flex align-center justify-space-between pa-6 bg-primary">
        <div class="d-flex align-center">
          <v-icon class="mr-3" color="white" size="32">mdi-account-edit</v-icon>
          <div>
            <h2 class="text-h5 text-white font-weight-medium">
              {{ isEdit ? 'Chỉnh sửa ứng viên' : 'Thêm ứng viên mới' }}
            </h2>
            <div class="text-body-2 text-blue-lighten-3">
              {{ isEdit ? candidate?.full_name : 'Tạo hồ sơ ứng viên mới' }}
            </div>
          </div>
        </div>
        
        <v-btn
          icon="mdi-close"
          variant="text"
          color="white"
          @click="cancelEdit"
        />
      </v-card-title>

      <!-- Loading State -->
      <div v-if="loading" class="pa-6">
        <v-skeleton-loader type="text, text, text, text, divider, chip, chip" />
      </div>

      <!-- Form Content -->
      <v-form v-else ref="formRef" @submit.prevent="submitForm">
        <v-card-text class="pa-6">
          <!-- Basic Information -->
          <div class="mb-6">
            <h3 class="text-h6 font-weight-medium mb-4 d-flex align-center">
              <v-icon class="mr-2" color="primary">mdi-account-details</v-icon>
              Thông tin cơ bản
            </h3>
            
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="formData.full_name"
                  label="Tên đầy đủ *"
                  variant="outlined"
                  :rules="[rules.required]"
                  :error-messages="validationErrors.full_name"
                  required
                />
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.email"
                  label="Email *"
                  type="email"
                  variant="outlined"
                  :rules="[rules.required, rules.email]"
                  :error-messages="validationErrors.email"
                  required
                />
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.phone"
                  label="Số điện thoại"
                  variant="outlined"
                  :rules="[rules.phone]"
                  :error-messages="validationErrors.phone"
                />
              </v-col>
              
              <v-col cols="12">
                <v-text-field
                  v-model="formData.headline"
                  label="Chức danh/Vị trí"
                  variant="outlined"
                  placeholder="VD: Senior Software Engineer"
                />
              </v-col>
            </v-row>
          </div>

          <!-- Professional Information -->
          <div class="mb-6">
            <h3 class="text-h6 font-weight-medium mb-4 d-flex align-center">
              <v-icon class="mr-2" color="primary">mdi-briefcase</v-icon>
              Thông tin nghề nghiệp
            </h3>
            
            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.source"
                  label="Nguồn"
                  variant="outlined"
                  :items="sourceOptions"
                  item-title="label"
                  item-value="value"
                />
              </v-col>
              
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.status"
                  label="Trạng thái"
                  variant="outlined"
                  :items="statusOptions"
                  item-title="label"
                  item-value="value"
                />
              </v-col>
              
              <v-col cols="12">
                <v-combobox
                  v-model="formData.skills"
                  label="Kỹ năng"
                  variant="outlined"
                  chips
                  multiple
                  closable-chips
                  :items="availableSkills"
                  item-title="label"
                  item-value="value"
                  placeholder="Nhập kỹ năng và nhấn Enter"
                  hint="Nhập kỹ năng và nhấn Enter để thêm"
                />
              </v-col>
            </v-row>
          </div>

          <!-- Additional Information -->
          <div class="mb-6">
            <h3 class="text-h6 font-weight-medium mb-4 d-flex align-center">
              <v-icon class="mr-2" color="primary">mdi-information</v-icon>
              Thông tin bổ sung
            </h3>
            
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="formData.cv_original_url"
                  label="URL CV"
                  variant="outlined"
                  placeholder="https://example.com/cv.pdf"
                  :rules="[rules.url]"
                />
              </v-col>
              
              <v-col cols="12">
                <v-textarea
                  v-model="formData.ai_summary"
                  label="Tóm tắt AI"
                  variant="outlined"
                  rows="3"
                  placeholder="Mô tả ngắn gọn về ứng viên..."
                />
              </v-col>
            </v-row>
          </div>

          <!-- Settings -->
          <div class="mb-6">
            <h3 class="text-h6 font-weight-medium mb-4 d-flex align-center">
              <v-icon class="mr-2" color="primary">mdi-cog</v-icon>
              Cài đặt
            </h3>
            
            <v-row>
              <v-col cols="12">
                <v-switch
                  v-model="formData.email_opt_out"
                  label="Từ chối email marketing"
                  color="error"
                  inset
                  :true-value="1"
                  :false-value="0"
                />
              </v-col>
            </v-row>
          </div>
        </v-card-text>

        <!-- Actions -->
        <v-card-actions class="px-6 py-4 bg-grey-lighten-5">
          <v-spacer />
          <v-btn
            variant="outlined"
            @click="cancelEdit"
            :disabled="saving"
          >
            Hủy
          </v-btn>
          <v-btn
            type="submit"
            color="primary"
            variant="flat"
            :loading="saving"
            :disabled="!isFormValid"
          >
            {{ isEdit ? 'Cập nhật' : 'Tạo mới' }}
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { validateCandidateForm, processSkills } from '@/utils/candidateHelpers'

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
      statuses: [],
      sources: [],
      skills: []
    })
  }
})

// Emits
const emit = defineEmits([
  'update:modelValue',
  'save-candidate',
  'cancel'
])

// Refs
const formRef = ref(null)
const validationErrors = ref({})

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

const statusOptions = computed(() => [
  { label: 'Mới', value: 'NEW' },
  { label: 'Đã tìm thấy', value: 'SOURCED' },
  { label: 'Đang chăm sóc', value: 'NURTURING' },
  { label: 'Đã tương tác', value: 'ENGAGED' },
  { label: 'Đã lưu trữ', value: 'ARCHIVED' },
  ...props.filterOptions.statuses
])

const sourceOptions = computed(() => [
  { label: 'Thủ công', value: 'MANUAL' },
  { label: 'LinkedIn', value: 'LINKEDIN' },
  { label: 'Website', value: 'WEBSITE' },
  { label: 'Giới thiệu', value: 'REFERRAL' },
  { label: 'Job Board', value: 'JOB_BOARD' },
  ...props.filterOptions.sources
])

const availableSkills = computed(() => [
  // Common skills
  { label: 'JavaScript', value: 'JavaScript' },
  { label: 'Python', value: 'Python' },
  { label: 'Java', value: 'Java' },
  { label: 'React', value: 'React' },
  { label: 'Vue.js', value: 'Vue.js' },
  { label: 'Node.js', value: 'Node.js' },
  { label: 'SQL', value: 'SQL' },
  { label: 'HTML/CSS', value: 'HTML/CSS' },
  ...props.filterOptions.skills
])

const isFormValid = computed(() => {
  return formData.value.full_name?.trim() && 
         formData.value.email?.trim() &&
         Object.keys(validationErrors.value).length === 0
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
  
  if (formRef.value) {
    formRef.value.resetValidation()
  }
}

const loadCandidateData = () => {
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
}

const validateForm = () => {
  validationErrors.value = {}
  
  const validation = validateCandidateForm(formData.value)
  if (!validation.isValid) {
    validationErrors.value = validation.errors
    return false
  }
  
  return true
}

const submitForm = async () => {
  if (!validateForm()) {
    return
  }
  
  try {
    // Validate form using v-form
    const { valid } = await formRef.value.validate()
    if (!valid) {
      return
    }
    
    // Prepare data for submission
    const submitData = {
      ...formData.value,
      skills: processSkills(formData.value.skills)
    }
    
    emit('save-candidate', submitData)
  } catch (error) {
    console.error('Form submission error:', error)
  }
}

const cancelEdit = () => {
  resetForm()
  emit('cancel')
  emit('update:modelValue', false)
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
:deep(.v-field) {
  border-radius: 8px;
}

:deep(.v-field--focused) {
  box-shadow: 0 0 0 2px rgba(var(--v-theme-primary), 0.2);
}

:deep(.v-messages) {
  min-height: 0;
}

:deep(.v-input--error .v-field) {
  border-color: rgb(var(--v-theme-error));
}

/* Switch styling */
:deep(.v-switch .v-selection-control__input) {
  border-radius: 12px;
}

/* Chips styling */
:deep(.v-chip) {
  border-radius: 6px;
}

/* Textarea styling */
:deep(.v-textarea .v-field) {
  min-height: 80px;
}
</style> 