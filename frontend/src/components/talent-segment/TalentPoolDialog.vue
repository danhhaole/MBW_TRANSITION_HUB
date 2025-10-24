<template>
  <Dialog v-model="isOpen" :options="dialogOptions">
    <template #body-title>
      <div class="bg-white">
        <div class="mb-5 flex items-center justify-between">
          <div>
            <h3 class="text-2xl font-semibold leading-6 text-gray-900">
              {{ segment ? __('Edit Talent Pool') : __('Create Talent Pool') }}
            </h3>
          </div>
        </div>
      </div>
    </template>
    
    <template #body-content>
      <div class="bg-white">
        <div class="max-h-[70vh] overflow-y-auto px-1">
          <div class="space-y-6">
            <!-- Title -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Pool Name') }} <span class="text-red-500">*</span>
              </label>
              <input 
                v-model="formData.title" 
                type="text" 
                :placeholder="__('Enter pool name...')"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                :class="{ 'border-red-500': errors.title }" 
                maxlength="100"
              />
              <p v-if="errors.title" class="mt-1 text-sm text-red-600">{{ errors.title }}</p>
            </div>

            <!-- Description -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Description') }}
              </label>
              <textarea 
                v-model="formData.description" 
                rows="3"
                :placeholder="__('Detailed description of this pool...')"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                maxlength="500" 
              />
            </div>

            <!-- Type and Owner -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Pool Type') }} <span class="text-red-500">*</span>
                </label>
                <select 
                  v-model="formData.type"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  <option value="">{{ __('Select pool type') }}</option>
                  <option value="STATIC">{{ __('Static') }}</option>
                  <option value="DYNAMIC">{{ __('Dynamic') }}</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Manager') }}
                </label>
                <select 
                  v-model="formData.owner_id"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  <option value="">{{ __('Select manager') }}</option>
                  <option v-for="user in userOptions" :key="user.name" :value="user.name">
                    {{ user.full_name }}
                  </option>
                </select>
              </div>
            </div>

            <!-- Filter Conditions Section -->
            <div class="border-t pt-6">
              <div class="mb-4">
                <h4 class="text-lg font-medium text-gray-900 mb-2">
                  {{ __('Filter Conditions') }}
                </h4>
                <p class="text-sm text-gray-600">
                  {{ __('Define conditions to automatically filter talents for this pool') }}
                </p>
              </div>

              <ConditionsBuilder
                ref="conditionsBuilderRef"
                v-model="formData.conditions"
                doctype="Mira Talent"
                :custom-fields="talentPoolFields"
                :title="''"
                :description="''"
                :show-preview="false"
                :validate-on-change="true"
                @validate="handleConditionsValidate"
              />
            </div>
          </div>
        </div>
      </div>
    </template>
    
    <template #actions>
      <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
        <Button variant="outline" theme="gray" @click="handleCancel">
          {{ __('Cancel') }}
        </Button>
        <Button 
          variant="solid" 
          theme="gray" 
          @click="handleSubmit"
          :loading="loading"
          :disabled="!isFormValid"
        >
          {{ segment ? __('Update') : __('Create') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { Dialog, Button, FeatherIcon } from 'frappe-ui'
import { useToast } from '@/composables/useToast'
import { call } from 'frappe-ui'
import ConditionsBuilder from '@/components/ConditionsFilter/ConditionsBuilder.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  segment: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'success', 'cancel'])

const { showSuccess, showError } = useToast()

// Local state
const loading = ref(false)
const errors = ref({})
const userOptions = ref([])
const conditionsValid = ref(true)
const conditionsBuilderRef = ref(null)

// Form data
const formData = ref({
  title: '',
  description: '',
  type: 'DYNAMIC',
  owner_id: '',
  conditions: []
})

// Custom fields for Talent Pool filtering - Advanced Conditions
const talentPoolFields = [
  { label: 'Full Name', fieldname: 'full_name', fieldtype: 'Data', value: 'full_name' },
  { label: 'Email', fieldname: 'email', fieldtype: 'Data', value: 'email' },
  { label: 'Phone', fieldname: 'phone', fieldtype: 'Data', value: 'phone' },
  { label: 'Skills', fieldname: 'skills', fieldtype: 'Small Text', value: 'skills' },
  { label: 'Tags', fieldname: 'tags', fieldtype: 'Small Text', value: 'tags' },
  { label: 'Source', fieldname: 'source', fieldtype: 'Data', value: 'source' },
  { label: 'Status', fieldname: 'status', fieldtype: 'Select', options: 'Active\nInactive\nBlacklisted', value: 'status' },
  { label: 'Gender', fieldname: 'gender', fieldtype: 'Select', options: 'Male\nFemale\nOther', value: 'gender' },
  { label: 'Experience Years', fieldname: 'experience_years', fieldtype: 'Int', value: 'experience_years' },
  { label: 'Education Level', fieldname: 'education_level', fieldtype: 'Select', options: 'High School\nBachelor\nMaster\nPhD', value: 'education_level' },
  { label: 'Current Position', fieldname: 'current_position', fieldtype: 'Data', value: 'current_position' },
  { label: 'Expected Salary', fieldname: 'expected_salary', fieldtype: 'Currency', value: 'expected_salary' },
  { label: 'Rating', fieldname: 'rating', fieldtype: 'Rating', value: 'rating' },
  { label: 'City', fieldname: 'city', fieldtype: 'Data', value: 'city' },
  { label: 'Last Interaction Date', fieldname: 'last_interaction_date', fieldtype: 'Date', value: 'last_interaction_date' },
  { label: 'Created On', fieldname: 'creation', fieldtype: 'Datetime', value: 'creation' },
  { label: 'Modified On', fieldname: 'modified', fieldtype: 'Datetime', value: 'modified' },
]

// Computed
const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const dialogOptions = computed(() => ({
  size: '4xl',
  title: props.segment ? __('Edit Talent Pool') : __('Create Talent Pool')
}))

const isFormValid = computed(() => {
  return formData.value.title && 
         formData.value.type && 
         conditionsValid.value
})

// Methods
const loadUserOptions = async () => {
  try {
    const result = await call('frappe.client.get_list', {
      doctype: 'User',
      fields: ['name', 'full_name', 'email'],
      filters: { enabled: 1 },
      limit_page_length: 100
    })
    
    if (result && result.length) {
      userOptions.value = result
    }
  } catch (error) {
    console.error('Error loading users:', error)
  }
}

const handleConditionsValidate = (validation) => {
  conditionsValid.value = validation.isValid
}

const resetForm = () => {
  formData.value = {
    title: '',
    description: '',
    type: 'DYNAMIC',
    owner_id: '',
    conditions: []
  }
  errors.value = {}
  conditionsValid.value = true
}

const loadSegmentData = () => {
  if (props.segment) {
    formData.value = {
      title: props.segment.title || '',
      description: props.segment.description || '',
      type: props.segment.type || 'DYNAMIC',
      owner_id: props.segment.owner_id || '',
      conditions: props.segment.criteria || []
    }
    
    // Parse conditions if exists
    try {
      if (props.segment.criteria) {
        formData.value.conditions = JSON.parse(props.segment.criteria)
      }
    } catch (error) {
      console.error('Error parsing segment conditions:', error)
    }
  } else {
    resetForm()
  }
}

const handleSubmit = async () => {
  errors.value = {}
  
  // Validate
  if (!formData.value.title) {
    errors.value.title = __('Pool name is required')
    return
  }
  
  if (!conditionsValid.value) {
    showError(__('Please fix the conditions before saving'))
    return
  }

  loading.value = true
  
  try {
    const data = {
      title: formData.value.title,
      description: formData.value.description,
      type: formData.value.type,
      owner_id: formData.value.owner_id,
      criteria: JSON.stringify(formData.value.conditions)
    }

    if (props.segment) {
      // Update existing
      await call('frappe.client.set_value', {
        doctype: 'Mira Segment',
        name: props.segment.name,
        fieldname: data
      })
      showSuccess(__('Talent pool updated successfully'))
    } else {
      // Create new
      await call('frappe.client.insert', {
        doc: {
          doctype: 'Mira Segment',
          ...data
        }
      })
      showSuccess(__('Talent pool created successfully'))
    }
    
    emit('success')
    isOpen.value = false
  } catch (error) {
    console.error('Error saving talent pool:', error)
    showError(error.message || __('Failed to save talent pool'))
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  emit('cancel')
  isOpen.value = false
}

// Watchers
watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    loadSegmentData()
    loadUserOptions()
  }
})

watch(() => props.segment, () => {
  if (props.modelValue) {
    loadSegmentData()
  }
})

// Lifecycle
onMounted(() => {
  if (props.modelValue) {
    loadSegmentData()
    loadUserOptions()
  }
})
</script>

<style scoped>
/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
