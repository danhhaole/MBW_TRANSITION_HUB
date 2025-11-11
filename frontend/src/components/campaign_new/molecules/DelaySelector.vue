<template>
  <div class="space-y-2">
    <label v-if="label" class="block text-xs font-medium text-gray-700">
      {{ label }}
      <span v-if="!optional" class="text-red-500">*</span>
      <span v-else class="text-gray-500 text-xs">({{ __('Optional') }})</span>
    </label>
    
    <div class="flex items-center space-x-2">
      <!-- Number Input -->
      <FormControl
        type="number"
        :modelValue="delayValue"
        @update:modelValue="updateDelayValue"
        :placeholder="placeholder || '0'"
        size="sm"
        min="0"
        class="flex-1"
      />
      
      <!-- Unit Selector -->
      <FormControl
        type="select"
        :modelValue="delayUnit"
        @update:modelValue="updateDelayUnit"
        :options="unitOptions"
        size="sm"
        class="w-32"
      />
    </div>
    
    <!-- Display calculated minutes -->
    <p v-if="totalMinutes > 0" class="text-xs text-gray-500">
      {{ __('Total delay:') }} {{ formatDelay(totalMinutes) }}
    </p>
    <p v-else class="text-xs text-gray-500">
      {{ __('No delay - will execute immediately') }}
    </p>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { FormControl } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: Number,
    default: 0 // Total minutes
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  optional: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue'])

// Unit options
const unitOptions = [
  { label: __('Minutes'), value: 'minutes' },
  { label: __('Hours'), value: 'hours' },
  { label: __('Days'), value: 'days' },
  { label: __('Weeks'), value: 'weeks' }
]

// Local state
const delayValue = ref(0)
const delayUnit = ref('minutes')

// Calculate total minutes
const totalMinutes = computed(() => {
  const value = delayValue.value || 0
  const multipliers = {
    'minutes': 1,
    'hours': 60,
    'days': 1440, // 24 * 60
    'weeks': 10080 // 7 * 24 * 60
  }
  return value * (multipliers[delayUnit.value] || 1)
})

// Initialize from modelValue
const initializeFromMinutes = (minutes) => {
  if (!minutes || minutes === 0) {
    delayValue.value = 0
    delayUnit.value = 'minutes'
    return
  }
  
  // Try to find the best unit
  if (minutes % 10080 === 0) {
    // Weeks
    delayValue.value = minutes / 10080
    delayUnit.value = 'weeks'
  } else if (minutes % 1440 === 0) {
    // Days
    delayValue.value = minutes / 1440
    delayUnit.value = 'days'
  } else if (minutes % 60 === 0) {
    // Hours
    delayValue.value = minutes / 60
    delayUnit.value = 'hours'
  } else {
    // Minutes
    delayValue.value = minutes
    delayUnit.value = 'minutes'
  }
}

// Watch for external changes
watch(() => props.modelValue, (newVal) => {
  if (newVal !== totalMinutes.value) {
    initializeFromMinutes(newVal)
  }
}, { immediate: true })

// Emit changes
watch(totalMinutes, (newVal) => {
  emit('update:modelValue', newVal)
})

// Update handlers
const updateDelayValue = (value) => {
  delayValue.value = parseInt(value) || 0
}

const updateDelayUnit = (value) => {
  delayUnit.value = value
}

// Format delay for display
const formatDelay = (minutes) => {
  if (minutes === 0) return __('Immediate')
  
  const weeks = Math.floor(minutes / 10080)
  const days = Math.floor((minutes % 10080) / 1440)
  const hours = Math.floor((minutes % 1440) / 60)
  const mins = minutes % 60
  
  const parts = []
  if (weeks > 0) parts.push(`${weeks} ${weeks === 1 ? __('week') : __('weeks')}`)
  if (days > 0) parts.push(`${days} ${days === 1 ? __('day') : __('days')}`)
  if (hours > 0) parts.push(`${hours} ${hours === 1 ? __('hour') : __('hours')}`)
  if (mins > 0) parts.push(`${mins} ${mins === 1 ? __('minute') : __('minutes')}`)
  
  return parts.join(', ')
}
</script>

<style scoped>
/* Add any custom styles here */
</style>
