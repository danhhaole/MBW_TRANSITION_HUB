<template>
  <div class="conditions-builder">
    <!-- Header -->
    <div class="mb-4">
      <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
      <p v-if="description" class="text-sm text-gray-600 mt-1">{{ description }}</p>
    </div>

    <!-- Conditions Section -->
    <div class="space-y-4">
      <CFConditions
        v-if="localConditions.length > 0"
        :conditions="localConditions"
        :level="0"
        :disableAddCondition="hasErrors"
        :doctype="doctype"
      />
      
      <!-- Empty State - Add First Condition -->
      <div
        v-if="localConditions.length === 0"
        class="flex p-4 items-center cursor-pointer justify-center gap-2 text-sm border border-gray-300 text-gray-600 rounded-md hover:bg-gray-50 transition-colors"
        @click="addFirstCondition"
      >
        <FeatherIcon name="plus" class="h-4" />
        {{ __('Add a condition') }}
      </div>

      <!-- Add Condition Button (when conditions exist) -->
      <div class="flex items-center justify-between mt-2" v-if="localConditions.length > 0">
        <Dropdown v-slot="{ open }" :options="dropdownOptions">
          <Button
            :disabled="hasErrors"
            :icon-right="open ? 'chevron-up' : 'chevron-down'"
            :label="__('Add condition')"
          />
        </Dropdown>
      </div>
    </div>

    <!-- Preview Section (Optional) -->
    <div v-if="showPreview && localConditions.length > 0" class="mt-6 p-4 bg-gray-50 rounded-md border border-gray-200">
      <div class="flex items-center justify-between mb-2">
        <span class="text-sm font-medium text-gray-700">{{ __('Condition Preview') }}</span>
        <Button
          variant="ghost"
          size="sm"
          icon="copy"
          @click="copyConditionsJSON"
          :label="__('Copy JSON')"
        />
      </div>
      <pre class="text-xs text-gray-600 overflow-x-auto">{{ JSON.stringify(localConditions, null, 2) }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, provide } from 'vue'
import { Button, Dropdown, FeatherIcon } from 'frappe-ui'
import { validateConditions } from '@/utils'
import { useToast } from '@/composables/useToast'
import CFConditions from './CFConditions.vue'

const props = defineProps({
  // Initial conditions value
  modelValue: {
    type: Array,
    default: () => []
  },
  // DocType for field filtering
  doctype: {
    type: String,
    required: true
  },
  // Custom fields to use instead of fetching from doctype
  customFields: {
    type: Array,
    default: null
  },
  // Title for the conditions section
  title: {
    type: String,
    default: 'Assignment condition'
  },
  // Description text
  description: {
    type: String,
    default: ''
  },
  // Show JSON preview
  showPreview: {
    type: Boolean,
    default: false
  },
  // Validate on change
  validateOnChange: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'validate', 'change'])

const { showSuccess, showError } = useToast()

// Local state
const localConditions = ref([...props.modelValue])
const errorMessage = ref('')

// Computed
const hasErrors = computed(() => {
  if (!props.validateOnChange) return false
  return errorMessage.value !== ''
})

// Get conjunction (and/or)
const getConjunction = () => {
  let conjunction = 'and'
  localConditions.value.forEach((condition) => {
    if (typeof condition === 'string') {
      conjunction = condition
    }
  })
  return conjunction
}

// Dropdown options for adding conditions
const dropdownOptions = computed(() => {
  return [
    {
      label: __('Add condition'),
      onClick: () => {
        addCondition()
      },
    },
    {
      label: __('Add condition group'),
      onClick: () => {
        const conjunction = getConjunction()
        localConditions.value.push(conjunction, [[]])
        validateAndEmit()
      },
    },
  ]
})

// Add first condition
const addFirstCondition = () => {
  localConditions.value.push(['', '', ''])
  validateAndEmit()
}

// Add condition
const addCondition = () => {
  const isValid = validateConditions(localConditions.value)

  if (!isValid && localConditions.value.length > 0) {
    errorMessage.value = __('Please complete existing conditions before adding new ones')
    return
  }
  
  errorMessage.value = ''
  const conjunction = getConjunction()
  localConditions.value.push(conjunction, ['', '', ''])
  validateAndEmit()
}

// Validate and emit
const validateAndEmit = () => {
  if (props.validateOnChange) {
    const isValid = validateConditions(localConditions.value)
    
    if (!isValid && localConditions.value.length > 0) {
      errorMessage.value = __('Conditions are invalid or incomplete')
    } else {
      errorMessage.value = ''
    }
    
    emit('validate', {
      isValid,
      conditions: localConditions.value,
      error: errorMessage.value
    })
  }
  
  emit('update:modelValue', localConditions.value)
  emit('change', localConditions.value)
}

// Validate assignment rule (provided to child components)
const validateAssignmentRule = () => {
  validateAndEmit()
}

// Copy conditions JSON to clipboard
const copyConditionsJSON = () => {
  const json = JSON.stringify(localConditions.value, null, 2)
  navigator.clipboard.writeText(json).then(() => {
    showSuccess(__('Conditions JSON copied to clipboard'))
  }).catch(() => {
    showError(__('Failed to copy to clipboard'))
  })
}

// Clear all conditions
const clearConditions = () => {
  localConditions.value = []
  errorMessage.value = ''
  validateAndEmit()
}

// Set conditions programmatically
const setConditions = (conditions) => {
  localConditions.value = [...conditions]
  validateAndEmit()
}

// Get current conditions
const getConditions = () => {
  return [...localConditions.value]
}

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  if (JSON.stringify(newValue) !== JSON.stringify(localConditions.value)) {
    localConditions.value = [...newValue]
  }
}, { deep: true })

// Watch local conditions for validation
watch(localConditions, () => {
  validateAndEmit()
}, { deep: true })

// Provide validation function and custom fields to child components
provide('validateAssignmentRule', validateAssignmentRule)
provide('customFields', props.customFields)

// Expose methods for parent component
defineExpose({
  clearConditions,
  setConditions,
  getConditions,
  validate: validateAndEmit
})
</script>

<style scoped>
.conditions-builder {
  width: 100%;
}
</style>
