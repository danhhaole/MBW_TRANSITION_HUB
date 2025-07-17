<template>
  <Dialog
    v-model="dialog"
    :options="{
      title: isEdit ? 'Chỉnh sửa nguồn dữ liệu' : 'Thêm nguồn dữ liệu mới',
      size: 'xl'
    }"
  >
    <template #body>
      <div class="p-6">
        <!-- Header -->
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2M4 13h2m0 0V9a2 2 0 012-2h8a2 2 0 012 2v4M6 13h12"></path>
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-900">
              {{ isEdit ? 'Chỉnh sửa nguồn dữ liệu' : 'Thêm nguồn dữ liệu mới' }}
            </h3>
            <p class="text-sm text-gray-500">
              {{ isEdit ? 'Cập nhật thông tin nguồn dữ liệu' : 'Tạo nguồn dữ liệu mới cho hệ thống' }}
            </p>
          </div>
        </div>

        <!-- Loading Form Fields -->
        <div v-if="loadingFields" class="flex justify-center items-center py-8">
          <div class="flex items-center space-x-2 text-gray-600">
            <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>Đang tải form...</span>
          </div>
        </div>

        <!-- Form using FieldLayout -->
        <div v-else-if="fieldTabs && fieldTabs.length > 0" class="space-y-4">
          <FieldLayout
            :tabs="fieldTabs"
            :data="formData"
            doctype="CandidateDataSource"
            :preview="false"
          />
        </div>

        <!-- Fallback Form if FieldLayout fails -->
        <div v-else class="space-y-4">
          <!-- Source Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Tên nguồn <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formData.source_name"
              type="text"
              placeholder="Nhập tên nguồn dữ liệu"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          <!-- Source Type -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Loại nguồn <span class="text-red-500">*</span>
            </label>
            <select
              v-model="formData.source_type"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            >
              <option value="">-- Chọn loại nguồn --</option>
              <option value="ATS">ATS</option>
              <option value="JobBoard">Job Board</option>
              <option value="SocialNetwork">Social Network</option>
              <option value="Manual">Manual</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <!-- API Base URL -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">API Base URL</label>
            <input
              v-model="formData.api_base_url"
              type="url"
              placeholder="https://api.example.com"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <!-- Auth Method -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Phương thức xác thực <span class="text-red-500">*</span>
            </label>
            <select
              v-model="formData.auth_method"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            >
              <option value="">-- Chọn phương thức --</option>
              <option value="API Key">API Key</option>
              <option value="OAuth2">OAuth2</option>
              <option value="Basic">Basic</option>
            </select>
          </div>

          <!-- Status -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Trạng thái</label>
            <select
              v-model="formData.status"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="Active">Active</option>
              <option value="Inactive">Inactive</option>
            </select>
          </div>

          <!-- Notes -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Ghi chú</label>
            <textarea
              v-model="formData.notes"
              rows="3"
              placeholder="Ghi chú về nguồn dữ liệu..."
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            ></textarea>
          </div>

          <!-- Active Status -->
          <div class="flex items-center space-x-2">
            <input
              v-model="formData.is_active"
              type="checkbox"
              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
            />
            <label class="text-sm font-medium text-gray-700">Kích hoạt nguồn dữ liệu</label>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mt-4 bg-red-50 border border-red-200 rounded-lg p-3">
          <div class="flex">
            <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
            <div class="ml-3">
              <p class="text-sm text-red-800">{{ error }}</p>
            </div>
          </div>
        </div>

        <!-- Success Message -->
        <div v-if="success" class="mt-4 bg-green-50 border border-green-200 rounded-lg p-3">
          <div class="flex">
            <svg class="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <div class="ml-3">
              <p class="text-sm text-green-800">{{ __('Thao tác thành công!') }}</p>
            </div>
          </div>
        </div>

        <!-- Buttons -->
        <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200 mt-6">
          <button
            type="button"
            @click="handleCancel"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            {{ __('Hủy') }}
          </button>
          <button
            type="button"
            @click="handleSubmit"
            :disabled="loading"
            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <span v-if="loading" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></span>
            <span>{{ isEdit ? __('Cập nhật') : __('Tạo mới') }}</span>
          </button>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted, reactive } from 'vue'
import { Dialog } from 'frappe-ui'
import FieldLayout from '@/components/FieldLayout/FieldLayout.vue'
import { candidateDataSourceService } from '@/services/candidateDataSourceService.js'

// Translation helper function
const __ = (text) => text

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  dataSource: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'success', 'cancel'])

// Refs
const loading = ref(false)
const loadingFields = ref(false)
const error = ref(null)
const success = ref(false)
const fieldTabs = ref([])

// Form data
const formData = reactive({
  source_name: '',
  source_type: '',
  api_base_url: '',
  auth_method: '',
  client_id: '',
  client_secret: '',
  api_key: '',
  api_secret: '',
  access_token: '',
  refresh_token: '',
  token_expires_at: '',
  doctype_to_sync: '',
  sync_direction: '',
  status: 'Active',
  last_sync_at: '',
  sync_frequency_minutes: 60,
  last_error: '',
  notes: '',
  created_by: '',
  is_active: true
})

// Computed
const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const isEdit = computed(() => !!props.dataSource)

// Methods
const resetForm = () => {
  Object.assign(formData, {
    source_name: '',
    source_type: '',
    api_base_url: '',
    auth_method: '',
    client_id: '',
    client_secret: '',
    api_key: '',
    api_secret: '',
    access_token: '',
    refresh_token: '',
    token_expires_at: '',
    doctype_to_sync: '',
    sync_direction: '',
    status: 'Active',
    last_sync_at: '',
    sync_frequency_minutes: 60,
    last_error: '',
    notes: '',
    created_by: '',
    is_active: true
  })
}

const setFormData = (dataSource) => {
  if (dataSource) {
    Object.keys(formData).forEach(key => {
      if (dataSource[key] !== undefined) {
        formData[key] = dataSource[key]
      }
    })
  }
}

const loadFieldLayout = async () => {
  loadingFields.value = true
  try {
    const response = await candidateDataSourceService.getFormData(props.dataSource?.name || null)
    
    if (response.success && response.data && response.data.fieldLayout) {
      fieldTabs.value = response.data.fieldLayout
    } else {
      // Fallback: create simple field layout
      fieldTabs.value = [
        {
          label: '',
          name: 'main_tab',
          sections: [
            {
              label: 'Thông tin cơ bản',
              name: 'basic_info',
              columns: [
                {
                  label: '',
                  name: 'col1',
                  fields: [
                    {
                      fieldname: 'source_name',
                      fieldtype: 'Data',
                      label: 'Tên nguồn',
                      reqd: 1,
                      visible: true
                    },
                    {
                      fieldname: 'source_type',
                      fieldtype: 'Select',
                      label: 'Loại nguồn',
                      options: 'ATS\nJobBoard\nSocialNetwork\nManual\nOther',
                      reqd: 1,
                      visible: true
                    },
                    {
                      fieldname: 'api_base_url',
                      fieldtype: 'Small Text',
                      label: 'API Base URL',
                      visible: true
                    },
                    {
                      fieldname: 'auth_method',
                      fieldtype: 'Select',
                      label: 'Phương thức xác thực',
                      options: 'API Key\nOAuth2\nBasic',
                      reqd: 1,
                      visible: true
                    },
                    {
                      fieldname: 'status',
                      fieldtype: 'Select',
                      label: 'Trạng thái',
                      options: 'Active\nInactive',
                      visible: true
                    },
                    {
                      fieldname: 'notes',
                      fieldtype: 'Small Text',
                      label: 'Ghi chú',
                      visible: true
                    },
                    {
                      fieldname: 'is_active',
                      fieldtype: 'Check',
                      label: 'Kích hoạt',
                      visible: true
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  } catch (err) {
    console.error('Error loading field layout:', err)
    // Use fallback layout in case of error
    fieldTabs.value = []
  } finally {
    loadingFields.value = false
  }
}

const validateForm = () => {
  const errors = []

  if (!formData.source_name?.trim()) {
    errors.push('Tên nguồn là bắt buộc')
  }

  if (!formData.source_type) {
    errors.push('Loại nguồn là bắt buộc')
  }

  if (!formData.auth_method) {
    errors.push('Phương thức xác thực là bắt buộc')
  }

  if (formData.api_base_url && formData.api_base_url.trim()) {
    try {
      new URL(formData.api_base_url)
    } catch {
      errors.push('Định dạng API Base URL không hợp lệ')
    }
  }

  return errors
}

const handleSubmit = async () => {
  error.value = null
  success.value = false

  const validationErrors = validateForm()
  if (validationErrors.length > 0) {
    error.value = validationErrors.join(', ')
    return
  }

  loading.value = true

  try {
    let result
    if (isEdit.value) {
      result = await candidateDataSourceService.update(props.dataSource.name, formData)
    } else {
      result = await candidateDataSourceService.create(formData)
    }

    if (result.success) {
      success.value = true
      emit('success', {
        action: isEdit.value ? 'update' : 'create',
        data: result.data
      })
      
      // Close dialog after success
      setTimeout(() => {
        dialog.value = false
      }, 1000)
    } else {
      error.value = result.error || 'Có lỗi xảy ra'
    }
  } catch (err) {
    error.value = 'Có lỗi xảy ra: ' + err.message
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  error.value = null
  success.value = false
  emit('cancel')
  dialog.value = false
}

// Watch for dataSource changes (edit mode)
watch(() => props.dataSource, (newDataSource) => {
  if (newDataSource) {
    setFormData(newDataSource)
  } else {
    resetForm()
  }
}, { immediate: true })

// Watch dialog open/close
watch(dialog, (isOpen) => {
  if (isOpen) {
    error.value = null
    success.value = false
    loadFieldLayout()
    
    if (props.dataSource) {
      setFormData(props.dataSource)
    } else {
      resetForm()
    }
  }
})

// Expose methods for parent component
defineExpose({
  resetForm,
  validateForm
})
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style> 