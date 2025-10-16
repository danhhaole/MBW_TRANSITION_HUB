<template>
  <Dialog
    v-model="show"
    :options="{
      title: isEditing ? 'Chỉnh sửa Flow' : 'Tạo Flow mới',
      size: 'md'
    }"
  >
    <template #body-content>
      <div class="space-y-4">
        <!-- Flow Name Field -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Tên Flow <span class="text-red-500">*</span>
          </label>
          <FormControl
            v-model="form.title"
            type="text"
            placeholder="Nhập tên flow..."
            :disabled="loading"
            @input="clearError('title')"
          />
          <div v-if="errors.title" class="mt-1 text-sm text-red-600">
            {{ errors.title }}
          </div>
        </div>

        <!-- Status Field -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Trạng thái <span class="text-red-500">*</span>
          </label>
          <FormControl
            v-model="form.status"
            type="select"
            :options="statusOptions"
            placeholder="Chọn trạng thái..."
            :disabled="loading"
            @change="clearError('status')"
          />
          <div v-if="errors.status" class="mt-1 text-sm text-red-600">
            {{ errors.status }}
          </div>
        </div>

        <!-- Description Field (Optional) -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Mô tả
          </label>
          <FormControl
            v-model="form.description"
            type="textarea"
            placeholder="Nhập mô tả flow..."
            :disabled="loading"
            rows="3"
          />
        </div>

        <!-- Error Message -->
        <div v-if="generalError" class="p-3 bg-red-50 border border-red-200 rounded-md">
          <div class="flex">
            <FeatherIcon name="alert-circle" class="h-5 w-5 text-red-400" />
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">Có lỗi xảy ra</h3>
              <div class="mt-2 text-sm text-red-700">
                {{ generalError }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <template #actions>
      <div class="flex justify-end space-x-2">
        <Button
          variant="ghost"
          @click="handleCancel"
          :disabled="loading"
        >
          Hủy
        </Button>
        <Button
          variant="solid"
          @click="handleSubmit"
          :loading="loading"
        >
          {{ isEditing ? 'Cập nhật' : 'Tạo mới' }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { Dialog, FormControl, Button, FeatherIcon } from 'frappe-ui'
import { useMiraFlowStore } from '@/stores/miraFlow'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  flow: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'success'])

// Store
const flowStore = useMiraFlowStore()

// Reactive data
const loading = ref(false)
const errors = ref({})
const generalError = ref('')

// Form data
const form = ref({
  title: '',
  status: 'Draft',
  description: ''
})

// Status options
const statusOptions = [
  { label: 'Bản nháp', value: 'Draft' },
  { label: 'Đang hoạt động', value: 'Active' },
  { label: 'Tạm dừng', value: 'Paused' },
  { label: 'Đã lưu trữ', value: 'Archived' }
]

// Computed
const show = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const isEditing = computed(() => {
  return props.flow && props.flow.name
})

// Methods
const resetForm = () => {
  form.value = {
    title: '',
    status: 'Draft',
    description: ''
  }
  errors.value = {}
  generalError.value = ''
}

const loadFlowData = () => {
  if (props.flow) {
    form.value = {
      title: props.flow.title || '',
      status: props.flow.status || 'Draft',
      description: props.flow.description || ''
    }
  }
}

const validateForm = () => {
  errors.value = {}
  
  if (!form.value.title || form.value.title.trim().length === 0) {
    errors.value.title = 'Tên flow là bắt buộc'
  } else if (form.value.title.length > 200) {
    errors.value.title = 'Tên flow không được vượt quá 200 ký tự'
  }
  
  if (!form.value.status) {
    errors.value.status = 'Trạng thái là bắt buộc'
  }
  
  return Object.keys(errors.value).length === 0
}

const clearError = (field) => {
  if (errors.value[field]) {
    delete errors.value[field]
  }
  if (generalError.value) {
    generalError.value = ''
  }
}

const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }
  
  loading.value = true
  generalError.value = ''
  
  try {
    let result
    
    if (isEditing.value) {
      // Update existing flow
      result = await flowStore.updateFlow(props.flow.name, form.value)
    } else {
      // Create new flow
      result = await flowStore.createFlow(form.value)
    }
    
    if (result.success) {
      emit('success', result.data)
      show.value = false
      resetForm()
    } else {
      generalError.value = result.error || result.message || 'Có lỗi xảy ra khi lưu flow'
    }
  } catch (error) {
    console.error('Error submitting flow:', error)
    generalError.value = error.message || 'Có lỗi xảy ra khi lưu flow'
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  show.value = false
  resetForm()
}

// Watchers
watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    nextTick(() => {
      loadFlowData()
    })
  } else {
    resetForm()
  }
})

watch(() => props.flow, () => {
  if (props.modelValue) {
    loadFlowData()
  }
})
</script>

<style scoped>
/* Custom styles if needed */
</style>
