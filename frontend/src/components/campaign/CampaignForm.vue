<template>
  <Dialog
    v-model="dialog"
    :options="{
      title: isEdit ? 'Edit Campaign' : 'Create New Campaign',
      size: 'xl'
    }"
  >
    <template #body>
      <div class="p-6">
        <!-- Header -->
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" />
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-900">
              {{ isEdit ? 'Edit Campaign' : 'Create New Campaign' }}
            </h3>
            <p class="text-sm text-gray-500">
              {{ isEdit ? 'Update campaign information' : 'Create a new recruitment campaign' }}
            </p>
          </div>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- Campaign Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Campaign Name <span class="text-red-500">*</span>
            </label>
            <input
              v-model="form.campaign_name"
              type="text"
              placeholder="Enter campaign name"
              maxlength="200"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
            <div class="text-xs text-gray-500 mt-1">Maximum 200 characters</div>
          </div>

          <!-- Description -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
            <textarea
              v-model="form.description"
              rows="3"
              placeholder="Enter detailed campaign description..."
              maxlength="1000"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            ></textarea>
            <div class="text-xs text-gray-500 mt-1">Maximum 1000 characters</div>
          </div>

          <!-- Row 1: Status and Type -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
              <select
                v-model="form.status"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option
                  v-for="option in statusOptions"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.title }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Campaign Type</label>
              <select
                v-model="form.type"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option
                  v-for="option in typeOptions"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.title }}
                </option>
              </select>
            </div>
          </div>

          <!-- Row 2: Active Status and Owner -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Active Status</label>
              <select
                v-model="form.is_active"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option
                  v-for="option in activeOptions"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.title }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Owner</label>
              <select
                v-model="form.owner_id"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">-- Select Owner --</option>
                <option
                  v-for="user in users"
                  :key="user.value"
                  :value="user.value"
                >
                  {{ user.title }}
                </option>
              </select>
            </div>

          </div>

          <!-- Target Segment -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Target Segment</label>
            <select
              v-model="form.target_segment"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">-- Select Target Segment --</option>
              <option
                v-for="segment in talentSegments"
                :key="segment.value"
                :value="segment.value"
              >
                {{ segment.title }}
              </option>
            </select>
          </div>

          <!-- Row 3: Start Date and End Date -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
              <input
                v-model="form.start_date"
                type="date"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">End Date</label>
              <input
                v-model="form.end_date"
                type="date"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-3">
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
          <div v-if="success" class="bg-green-50 border border-green-200 rounded-lg p-3">
            <div class="flex">
              <svg class="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
              <div class="ml-3">
                <p class="text-sm text-green-800">{{ __('Operation successful!') }}</p>
              </div>
            </div>
          </div>

          <!-- Buttons -->
          <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
            <button
              type="button"
              @click="handleCancel"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              {{ __('Cancel') }}
            </button>
            <button
              type="submit"
              :disabled="loading"
              class="px-4 py-2 text-sm font-medium text-white bg-black border border-transparent rounded-lg hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              <span v-if="loading" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></span>
              <span>{{ isEdit ? __('Update') : __('Create') }}</span>
            </button>
          </div>
        </form>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { Dialog } from 'frappe-ui'
import { useCampaignForm, useCampaignCRUD } from '@/composables/useCampaign.js'

// Translation helper function


// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  campaign: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'success', 'cancel'])

// Computed
const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const isEdit = computed(() => !!props.campaign)

// Composables
const {
  form,
  users,
  talentSegments,
  loadingOptions,
  campaignNameRules,
  dateRules,
  endDateRules,
  typeOptions,
  statusOptions,
  activeOptions,
  loadOptions,
  validateForm,
  resetForm,
  setFormData
} = useCampaignForm()

const {
  loading,
  error,
  success,
  createCampaign,
  updateCampaign,
  resetState
} = useCampaignCRUD()

// Validate form
const validateFormData = () => {
  if (!form.value.campaign_name || form.value.campaign_name.trim().length === 0) {
    return __('Campaign name is required')
  }
  if (form.value.campaign_name.length > 200) {
    return __('Campaign name cannot exceed 200 characters')
  }

  if (form.value.start_date && form.value.end_date) {
    if (new Date(form.value.start_date) > new Date(form.value.end_date)) {
      return __('Start date cannot be after end date')
    }
  }

  return null
}

// Methods
const handleSubmit = async () => {
  const validationError = validateFormData()
  if (validationError) {
    // Set error in composable
    error.value = validationError
    return
  }

  let result = false
  
  try {
    if (isEdit.value) {
      result = await updateCampaign(props.campaign.name, form.value)
    } else {
      result = await createCampaign(form.value)
    }

    if (result) {
      emit('success', {
        action: isEdit.value ? 'update' : 'create',
        data: form.value
      })
      
      // Đóng dialog sau 1 giây để user thấy thông báo success
      setTimeout(() => {
        dialog.value = false
      }, 1000)
    }
      } catch (err) {
      error.value = __('An error occurred: ') + err.message
    }
}

const handleCancel = () => {
  resetState()
  emit('cancel')
  dialog.value = false
}

// Watch for campaign changes (edit mode)
watch(() => props.campaign, (newCampaign) => {
  if (newCampaign) {
    setFormData(newCampaign)
  } else {
    resetForm()
  }
}, { immediate: true })

// Watch dialog open/close
watch(dialog, (isOpen) => {
  if (isOpen) {
    resetState()
    loadOptions() // Load users and talent segments
    if (props.campaign) {
      setFormData(props.campaign)
    } else {
      resetForm()
    }
  }
})

// Load options on mount
onMounted(() => {
  loadOptions()
})

// Expose methods for parent component
defineExpose({
  resetForm,
  validateForm: validateFormData
})
</script> 