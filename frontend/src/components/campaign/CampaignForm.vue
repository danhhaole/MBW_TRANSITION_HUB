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
              {{ isEdit ? __('Edit Campaign') : __('Create New Campaign') }}
            </h3>
            <p class="text-sm text-gray-500">
              {{ isEdit ? __('Update campaign information') : __('Create a new recruitment campaign') }}
            </p>
          </div>
        </div>

        <!-- Form -->
        <div class="space-y-4">
          <!-- Campaign Name -->
          <FormControl
            v-model="form.campaign_name"
            type="text"
            :label="__('Campaign Name')"
            :placeholder="__('Enter campaign name')"
            :maxlength="200"
            :required="true"
            :help="__('Maximum 200 characters')"
          />

          <!-- Description -->
          <FormControl
            v-model="form.description"
            type="textarea"
            :label="__('Description')"
            :placeholder="__('Enter detailed campaign description...')"
            :rows="3"
            :maxlength="1000"
            :help="__('Maximum 1000 characters')"
          />

          <!-- Row 1: Status and Type -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormControl
              v-model="form.status"
              type="select"
              :label="__('Status')"
              :options="statusOptions"
            />
            <FormControl
              v-model="form.type"
              type="select"
              :label="__('Campaign Type')"
              :options="typeOptions"
            />
          </div>

          <!-- Row 2: Active Status and Owner -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormControl
              v-model="form.is_active"
              type="select"
              :label="__('Active Status')"
              :options="activeOptions"
            />
            <FormControl
              v-model="form.owner_id"
              type="select"
              :label="__('Owner')"
              :options="[{ label: __('Select Owner'), value: '' }, ...users]"
            />
          </div>

          <!-- Target Segment -->
          <FormControl
            v-model="form.target_segment"
            type="select"
            :label="__('Target Segment')"
            :options="[{ label: __('Select Target Segment'), value: '' }, ...talentSegments]"
          />

          <!-- Job Opening
          <FormControl
            v-model="form.job_opening"
            type="select"
            :label="__('Job Opening')"
            :options="[{ label: __('Select Job Opening'), value: '' }, ...jobOpenings]"
            :help="__('Select a job to attach this campaign to')"
          /> -->
          <!-- Row 3: Start Date and End Date -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormControl
              v-model="form.start_date"
              type="datetime"
              :label="__('Start Date')"
            />
            <FormControl
              v-model="form.end_date"
              type="datetime"
              :label="__('End Date')"
            />
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
            <Button
              variant="outline"
              theme="gray"
              @click="handleCancel"
            >
              {{ __('Cancel') }}
            </Button>
            <Button
              variant="solid"
              theme="gray"
              :loading="loading"
              @click="handleSubmit"
            >
              {{ isEdit ? __('Update') : __('Create') }}
            </Button>
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { Dialog, FormControl, Button } from 'frappe-ui'
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
  setFormData,
  // jobOpenings
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