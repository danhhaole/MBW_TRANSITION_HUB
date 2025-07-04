<template>
  <v-form ref="formRef" @submit.prevent="$emit('submit', formData)">
    <v-row>
      <!-- Basic Information -->
      <v-col cols="12">
        <h3 class="text-h6 font-weight-medium mb-4">Thông tin cơ bản</h3>
      </v-col>
      
      <v-col cols="12">
        <v-text-field
          v-model="formData.full_name"
          label="Tên đầy đủ *"
          variant="outlined"
          :rules="[rules.required]"
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
          required
        />
      </v-col>
      
      <v-col cols="12" md="6">
        <v-text-field
          v-model="formData.phone"
          label="Số điện thoại"
          variant="outlined"
          :rules="[rules.phone]"
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

      <!-- Professional Information -->
      <v-col cols="12">
        <h3 class="text-h6 font-weight-medium mb-4">Thông tin nghề nghiệp</h3>
      </v-col>
      
      <v-col cols="12" md="6">
        <v-select
          v-model="formData.source"
          label="Nguồn"
          variant="outlined"
          :items="sourceOptions"
        />
      </v-col>
      
      <v-col cols="12" md="6">
        <v-select
          v-model="formData.status"
          label="Trạng thái"
          variant="outlined"
          :items="statusOptions"
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
          placeholder="Nhập kỹ năng và nhấn Enter"
        />
      </v-col>

      <!-- Additional Information -->
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

      <!-- Settings -->
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

      <!-- Actions -->
      <v-col cols="12" class="d-flex justify-end">
        <v-btn
          variant="outlined"
          @click="$emit('cancel')"
          :disabled="loading"
          class="mr-2"
        >
          Hủy
        </v-btn>
        <v-btn
          type="submit"
          color="primary"
          variant="flat"
          :loading="loading"
        >
          {{ candidate ? 'Cập nhật' : 'Tạo mới' }}
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

// Props
const props = defineProps({
  candidate: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['submit', 'cancel'])

// Refs
const formRef = ref(null)

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

// Options
const statusOptions = [
  { title: 'Mới', value: 'NEW' },
  { title: 'Đã tìm thấy', value: 'SOURCED' },
  { title: 'Đang chăm sóc', value: 'NURTURING' },
  { title: 'Đã tương tác', value: 'ENGAGED' },
  { title: 'Đã lưu trữ', value: 'ARCHIVED' }
]

const sourceOptions = [
  { title: 'Thủ công', value: 'MANUAL' },
  { title: 'LinkedIn', value: 'LINKEDIN' },
  { title: 'Website', value: 'WEBSITE' },
  { title: 'Giới thiệu', value: 'REFERRAL' },
  { title: 'Job Board', value: 'JOB_BOARD' }
]

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

// Watch for candidate changes
watch(() => props.candidate, (newCandidate) => {
  if (newCandidate) {
    formData.value = {
      full_name: newCandidate.full_name || '',
      email: newCandidate.email || '',
      phone: newCandidate.phone || '',
      headline: newCandidate.headline || '',
      source: newCandidate.source || 'MANUAL',
      status: newCandidate.status || 'NEW',
      skills: newCandidate.skills || [],
      cv_original_url: newCandidate.cv_original_url || '',
      ai_summary: newCandidate.ai_summary || '',
      email_opt_out: newCandidate.email_opt_out || 0
    }
  } else {
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
  }
}, { immediate: true })
</script>

<style scoped>
/* Form styling */
:deep(.v-field) {
  border-radius: 8px;
}

:deep(.v-field--focused) {
  box-shadow: 0 0 0 2px rgba(var(--v-theme-primary), 0.2);
}
</style> 