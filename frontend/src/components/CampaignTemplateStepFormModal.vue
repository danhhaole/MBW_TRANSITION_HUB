<template>
  <div v-if="show" class="fixed z-50 inset-0 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="handleClose"></div>
      
      <span class="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
      
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
        <form @submit.prevent="handleSubmit">
          <!-- Header -->
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                {{ isEdit ? __('Edit Template Step') : __('Add Template Step') }}
              </h3>
              <Button
                variant="ghost"
                size="sm"
                @click="handleClose"
              >
                <template #icon>
                  <FeatherIcon name="x" class="w-6 h-6" />
                </template>
              </Button>
            </div>
          </div>

          <!-- Form Content -->
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 max-h-96 overflow-y-auto">
            <div class="grid grid-cols-1 gap-6">
              <!-- Step Name -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Step Name') }}
                  <span class="text-red-500">*</span>
                </label>
                <TextInput
                  v-model="formData.campaign_step_name"
                  type="text"
                  :placeholder="__('Enter step name...')"
                  :disabled="loading"
                  class="w-full"
                />
                <div v-if="errors.campaign_step_name" class="mt-1 text-sm text-red-600">
                  {{ errors.campaign_step_name }}
                </div>
              </div>

              <div class="grid grid-cols-2 gap-4">
                <!-- Action Type -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __('Action Type') }}
                    <span class="text-red-500">*</span>
                  </label>
                  <FormControl
                    type="select"
                    v-model="formData.action_type"
                    :options="actionTypeOptions"
                    :disabled="loading"
                    class="w-full"
                  />
                  <div v-if="errors.action_type" class="mt-1 text-sm text-red-600">
                    {{ errors.action_type }}
                  </div>
                </div>

                <!-- Step Order -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __('Step Order') }}
                    <span class="text-red-500">*</span>
                  </label>
                  <TextInput
                    v-model.number="formData.step_order"
                    type="number"
                    min="1"
                    max="999"
                    :placeholder="__('Order...')"
                    :disabled="loading"
                    class="w-full"
                  />
                  <div v-if="errors.step_order" class="mt-1 text-sm text-red-600">
                    {{ errors.step_order }}
                  </div>
                </div>
              </div>

              <!-- Delay -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Delay (Days)') }}
                </label>
                <TextInput
                  v-model.number="formData.delay_in_days"
                  type="number"
                  min="0"
                  max="365"
                  :placeholder="__('0 for immediate execution')"
                  :disabled="loading"
                  class="w-full"
                />
                <p class="mt-1 text-sm text-gray-500">
                  {{ __('Number of days to wait before executing this step') }}
                </p>
                <div v-if="errors.delay_in_days" class="mt-1 text-sm text-red-600">
                  {{ errors.delay_in_days }}
                </div>
              </div>

              <!-- Template Content -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Template Content') }}
                </label>
                <textarea
                  v-model="formData.template_content"
                  rows="4"
                  :placeholder="__('Enter template content for this step...')"
                  :disabled="loading"
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
                <p class="mt-1 text-sm text-gray-500">
                  {{ __('Content template for emails, SMS, or other actions') }}
                </p>
                <div v-if="errors.template_content" class="mt-1 text-sm text-red-600">
                  {{ errors.template_content }}
                </div>
              </div>

              <!-- Action Config -->
              <div>
                <div class="flex items-center justify-between mb-2">
                  <label class="block text-sm font-medium text-gray-700">
                    {{ __('Action Configuration') }}
                  </label>
                  <Button
                    variant="ghost"
                    size="sm"
                    @click="showJsonHelp = !showJsonHelp"
                  >
                    {{ showJsonHelp ? __('Hide Help') : __('Show Help') }}
                  </Button>
                </div>
                
                <!-- JSON Help -->
                <div v-if="showJsonHelp" class="mb-3 p-3 bg-blue-50 border border-blue-200 rounded-md">
                  <div class="text-xs text-blue-800">
                    <p class="font-medium mb-2">{{ __('Configuration Examples:') }}</p>
                    <div class="space-y-1">
                      <p><strong>Email:</strong> {"subject": "Title", "from_email": "sender@example.com"}</p>
                      <p><strong>SMS:</strong> {"phone_field": "mobile", "sender_id": "Company"}</p>
                      <p><strong>Call:</strong> {"priority": "high", "assign_to": "user@example.com"}</p>
                      <p><strong>Task:</strong> {"title": "Follow up", "due_date": "+3 days"}</p>
                    </div>
                  </div>
                </div>

                <textarea
                  v-model="formData.action_config_string"
                  rows="3"
                  :placeholder="__('Enter JSON configuration...')"
                  :disabled="loading"
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm font-mono text-sm"
                />
                <p class="mt-1 text-sm text-gray-500">
                  {{ __('JSON configuration for the action (optional)') }}
                </p>
                <div v-if="errors.action_config" class="mt-1 text-sm text-red-600">
                  {{ errors.action_config }}
                </div>
              </div>
            </div>

            <!-- Error Message -->
            <div v-if="submitError" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <div class="flex">
                <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
                <div class="ml-3">
                  <h3 class="text-sm font-medium text-red-800">
                    {{ __('Error saving step') }}
                  </h3>
                  <div class="mt-1 text-sm text-red-700">
                    {{ submitError }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <Button
              type="submit"
              variant="solid"
              theme="gray"
              :loading="loading"
              :disabled="loading"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? __('Saving...') : (isEdit ? __('Update Step') : __('Add Step')) }}
            </Button>
            <Button
              variant="outline"
              theme="gray"
              @click="handleClose"
              :disabled="loading"
              class="sm:mr-3"
            >
              {{ __('Cancel') }}
            </Button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, nextTick } from 'vue'
import { Button, TextInput, FormControl, FeatherIcon } from 'frappe-ui'
import { useCampaignTemplateStepStore } from '@/stores/campaignTemplateStep.js'
import { useToast } from '@/composables/useToast.js'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  templateName: {
    type: String,
    required: true
  },
  step: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'saved'])

// Toast
const { showSuccess, showError } = useToast()

// Store
const campaignTemplateStepStore = useCampaignTemplateStepStore()

// Computed
const show = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const isEdit = computed(() => !!props.step)

// Reactive data
const loading = ref(false)
const submitError = ref('')
const showJsonHelp = ref(false)
const errors = reactive({})

const formData = reactive({
  campaign_step_name: '',
  action_type: '',
  step_order: 1,
  delay_in_days: 0,
  template_content: '',
  action_config_string: ''
})

// Action type options
const actionTypeOptions = [
  { label: __('Select action type...'), value: '', disabled: true },
  { label: __('Send Email'), value: 'SEND_EMAIL' },
  { label: __('Send SMS'), value: 'SEND_SMS' },
  { label: __('Manual Call'), value: 'MANUAL_CALL' },
  { label: __('Manual Task'), value: 'MANUAL_TASK' }
]

// Methods
const resetForm = () => {
  formData.campaign_step_name = ''
  formData.action_type = ''
  formData.step_order = 1
  formData.delay_in_days = 0
  formData.template_content = ''
  formData.action_config_string = ''
  
  // Clear errors
  Object.keys(errors).forEach(key => {
    delete errors[key]
  })
  
  submitError.value = ''
  showJsonHelp.value = false
}

const setFormData = (step) => {
  if (step) {
    formData.campaign_step_name = step.campaign_step_name || ''
    formData.action_type = step.action_type || ''
    formData.step_order = step.step_order || 1
    formData.delay_in_days = step.delay_in_days || 0
    formData.template_content = step.template_content || ''
    
    // Handle JSON config
    if (step.action_config) {
      if (typeof step.action_config === 'object') {
        formData.action_config_string = JSON.stringify(step.action_config, null, 2)
      } else {
        formData.action_config_string = step.action_config
      }
    } else {
      formData.action_config_string = ''
    }
  }
}

const validateForm = () => {
  // Clear previous errors
  Object.keys(errors).forEach(key => {
    delete errors[key]
  })

  let isValid = true

  // Required fields
  if (!formData.campaign_step_name || !formData.campaign_step_name.trim()) {
    errors.campaign_step_name = __('Step name is required')
    isValid = false
  } else if (formData.campaign_step_name.length > 150) {
    errors.campaign_step_name = __('Step name must be less than 150 characters')
    isValid = false
  }

  if (!formData.action_type || !formData.action_type.trim()) {
    errors.action_type = __('Action type is required')
    isValid = false
  }

  if (!formData.step_order || formData.step_order < 1 || formData.step_order > 999) {
    errors.step_order = __('Step order must be between 1 and 999')
    isValid = false
  }

  if (formData.delay_in_days < 0 || formData.delay_in_days > 365) {
    errors.delay_in_days = __('Delay must be between 0 and 365 days')
    isValid = false
  }

  // Validate JSON config if provided
  if (formData.action_config_string && formData.action_config_string.trim()) {
    try {
      JSON.parse(formData.action_config_string)
    } catch (e) {
      errors.action_config = __('Invalid JSON format')
      isValid = false
    }
  }

  return isValid
}

const handleSubmit = async () => {
  console.log('Step Modal handleSubmit called!', {
    isEdit: isEdit.value,
    formData: { ...formData }
  })
  
  if (!validateForm()) {
    return
  }

  loading.value = true
  submitError.value = ''

  try {
    const data = {
      template: props.templateName,
      campaign_step_name: formData.campaign_step_name.trim(),
      action_type: formData.action_type,
      step_order: formData.step_order,
      delay_in_days: formData.delay_in_days,
      template_content: formData.template_content ? formData.template_content.trim() : '',
    }

    // Handle action config
    if (formData.action_config_string && formData.action_config_string.trim()) {
      try {
        data.action_config = JSON.parse(formData.action_config_string)
      } catch (e) {
        data.action_config = formData.action_config_string
      }
    }

    let result

    if (isEdit.value) {
      // Update existing step
      result = await campaignTemplateStepStore.updateStep(props.step.name, data)
    } else {
      // Create new step
      result = await campaignTemplateStepStore.createStep(data)
    }

    if (result.success) {
      showSuccess(result.message || (isEdit.value ? __('Step updated successfully') : __('Step added successfully')))

      // Close modal and emit saved event
      show.value = false
      emit('saved', result.data)
    } else {
      // Handle validation errors from server
      if (result.error.includes('campaign_step_name')) {
        errors.campaign_step_name = result.error
      } else if (result.error.includes('action_type')) {
        errors.action_type = result.error
      } else if (result.error.includes('step_order')) {
        errors.step_order = result.error
      } else {
        submitError.value = result.error
      }
    }
  } catch (err) {
    console.error('Error submitting form:', err)
    submitError.value = __('An error occurred while saving step')
  } finally {
    loading.value = false
  }
}

const handleClose = () => {
  if (!loading.value) {
    show.value = false
  }
}

// Auto-assign step order khi tạo mới
const getNextStepOrder = async () => {
  if (!isEdit.value && props.templateName) {
    try {
      const nextOrder = await campaignTemplateStepStore.getNextStepOrderForTemplate(props.templateName)
      formData.step_order = nextOrder
    } catch (error) {
      console.error('Error getting next step order:', error)
      formData.step_order = 1
    }
  }
}

// Watchers
watch(
  () => props.modelValue,
  async (newValue) => {
    if (newValue) {
      // Reset form when opening
      resetForm()
      
      // Debug log
      console.log('Step Modal opened:', {
        isEdit: isEdit.value,
        step: props.step,
        templateName: props.templateName
      })
      
      // Set form data if editing
      if (props.step) {
        nextTick(() => {
          setFormData(props.step)
        })
      } else {
        // Auto-assign step order for new steps
        await getNextStepOrder()
      }
    }
  },
  { immediate: true }
)

watch(
  () => props.step,
  (newStep) => {
    if (newStep && props.modelValue) {
      setFormData(newStep)
    }
  }
)
</script>

<style scoped>
/* Add any component-specific styles here */
</style> 