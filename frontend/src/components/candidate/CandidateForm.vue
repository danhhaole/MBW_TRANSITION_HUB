<template>
  <form @submit.prevent="$emit('submit', formData)" class="space-y-6">
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
            :error="errors?.full_name"
            required
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __('Email') }} <span class="text-red-500">*</span>
          </label>
          <FormControl
            type="email"
            v-model="formData.email"
            :placeholder="__('Enter email address')"
            :error="errors?.email"
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
            :error="errors?.phone"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Vị trí hiện tại
          </label>
          <FormControl
            type="text"
            v-model="formData.current_position"
            placeholder="VD: Senior Software Engineer"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Địa điểm
          </label>
          <FormControl
            type="text"
            v-model="formData.location"
            placeholder="VD: Ho Chi Minh City"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Năm kinh nghiệm
          </label>
          <FormControl
            type="number"
            v-model="formData.experience_years"
            placeholder="Nhập số năm kinh nghiệm"
            :min="0"
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
            <FormControl
              type="text"
              v-model="newSkill"
              placeholder="Nhập kỹ năng và nhấn Enter"
              @keyup.enter="addSkill"
            />
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
            Ghi chú
          </label>
          <FormControl
            type="textarea"
            v-model="formData.notes"
            placeholder="Ghi chú về ứng viên..."
            :rows="4"
          />
        </div>
      </div>
    </div>

    <!-- Form Actions -->
    <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
              <Button
          variant="outline"
          type="button"
          @click="$emit('cancel')"
          :disabled="loading"
        >
          {{ __('Cancel') }}
        </Button>
        <Button
          type="submit"
          variant="solid"
          :loading="loading"
          :disabled="!isFormValid"
        >
          {{ isEdit ? __('Update') : __('Create') }}
        </Button>
    </div>
  </form>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { FormControl, Button } from 'frappe-ui'

// Translation helper function


// Props
const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      full_name: '',
      email: '',
      phone: '',
      current_position: '',
      location: '',
      experience_years: '',
      source: '',
      status: 'Active',
      skills: [],
      notes: ''
    })
  },
  sourceOptions: {
    type: Array,
    default: () => [
 
    ]
  },
  statusOptions: {
    type: Array,
    default: () => [
      { label: 'Active', value: 'Active' },
      { label: 'Inactive', value: 'Inactive' }
    ]
  },
  errors: {
    type: Object,
    default: () => ({})
  },
  loading: {
    type: Boolean,
    default: false
  },
  isEdit: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits([
  'update:modelValue',
  'submit',
  'cancel'
])

// Refs
const newSkill = ref('')

// Form data
const formData = ref({ ...props.modelValue })

// Computed
const isFormValid = computed(() => {
  const hasName = !!formData.value.full_name?.trim()
  const hasEmail = !!formData.value.email?.trim()
  const hasNoErrors = Object.keys(props.errors).length === 0
  
  return hasName && hasEmail && hasNoErrors
})

// Methods
const addSkill = () => {
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

// Watchers
watch(() => props.modelValue, (newValue) => {
  formData.value = { ...newValue }
}, { deep: true })

watch(formData, (newValue) => {
  emit('update:modelValue', newValue)
}, { deep: true })
</script>

<style scoped>
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