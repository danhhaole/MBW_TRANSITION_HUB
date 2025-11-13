<template>
  <div class="bg-white rounded-lg border border-gray-200 p-6">
    <div class="flex items-center justify-between mb-4">
      <div>
        <h3 class="text-base font-semibold text-gray-900">
          {{ __('Campaign Schedule') }}
        </h3>
        <p class="text-sm text-gray-600 mt-1">
          {{ __('When do you want to start this campaign?') }}
        </p>
      </div>
      <!-- Reset button (only show if has been set) -->
      <button
        v-if="hasBeenSet"
        @click="resetSelection"
        class="text-xs text-blue-600 hover:text-blue-700 font-medium"
      >
        {{ __('Change') }}
      </button>
    </div>

    <!-- Show selection cards when not in schedule mode -->
    <div v-if="!hasBeenSet" class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Start Now -->
      <div 
        class="border rounded-lg p-4 bg-white cursor-pointer transition-colors"
        :class="sendingStrategy === 'now' ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' : 'border-gray-200 hover:border-gray-300'"
        @click="selectStrategy('now')"
      >
        <div class="text-center">
          <div class="flex items-center justify-center w-12 h-12 rounded-full mx-auto mb-3"
               :class="sendingStrategy === 'now' ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'">
            <FeatherIcon name="zap" class="h-6 w-6" />
          </div>
          <h6 class="text-sm font-semibold mb-1"
              :class="sendingStrategy === 'now' ? 'text-blue-900' : 'text-gray-900'">
            {{ __("Start Now") }}
          </h6>
          <p class="text-xs text-gray-600">
            {{ __("Campaign starts immediately") }}
          </p>
        </div>
      </div>

     

      <!-- Schedule Start -->
      <div 
        class="border rounded-lg p-4 bg-white cursor-pointer transition-colors"
        :class="sendingStrategy === 'scheduled' ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' : 'border-gray-200 hover:border-gray-300'"
        @click="selectStrategy('scheduled')"
      >
        <div class="text-center">
          <div class="flex items-center justify-center w-12 h-12 rounded-full mx-auto mb-3"
               :class="sendingStrategy === 'scheduled' ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'">
            <FeatherIcon name="calendar" class="h-6 w-6" />
          </div>
          <h6 class="text-sm font-semibold mb-1"
              :class="sendingStrategy === 'scheduled' ? 'text-blue-900' : 'text-gray-900'">
            {{ __("Schedule Start") }}
          </h6>
          <p class="text-xs text-gray-600">
            {{ __("Choose specific time to start campaign") }}
          </p>
        </div>
      </div>
    </div>

    <!-- Show DateTimePicker for scheduled mode -->
    <div v-else-if="sendingStrategy === 'scheduled'">
      <DateTimePicker
        :model-value="startDate"
        @update:model-value="$emit('update:startDate', $event)"
        variant="subtle"
        :placeholder="__('Select date and time')"
        :label="__('Start Date & Time')"
      />
      <p class="text-xs text-gray-500 mt-2">
        {{ __("Campaign will automatically start at the scheduled time") }}
      </p>
    </div>

    <!-- Show confirmation for Send Now -->
    <div v-else-if="sendingStrategy === 'now' && startDate === 'SEND_NOW'" class="bg-green-50 border border-green-200 rounded-lg p-4">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
          <FeatherIcon name="zap" class="h-5 w-5 text-green-600" />
        </div>
        <div>
          <h4 class="text-sm font-semibold text-green-900">
            {{ __('Ready to Start Immediately') }}
          </h4>
          <p class="text-xs text-green-700 mt-1">
            {{ __('Campaign will start as soon as you click Continue') }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { FeatherIcon, DateTimePicker } from 'frappe-ui'
import moment from 'moment'

const props = defineProps({
  startDate: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:startDate'])

// Track if user has made a selection (only true if user actually selected something)
const hasBeenSet = ref(false)

// Initialize sendingStrategy - default to 'now' but don't auto-set
const sendingStrategy = ref('now')

// Select strategy and mark as set
const selectStrategy = (strategy) => {
  sendingStrategy.value = strategy
  
  if (strategy === 'now') {
    // Just mark strategy, don't set datetime yet
    // Will be set when user clicks Continue
    emit('update:startDate', 'SEND_NOW')
  } else {
    // Schedule mode - show datetime picker
    hasBeenSet.value = true
    emit('update:startDate', '')
  }
}

// Reset to show selection cards again
const resetSelection = () => {
  hasBeenSet.value = false
  sendingStrategy.value = 'now'
  // Clear the start date when resetting
  emit('update:startDate', '')
}

// If props.startDate exists (from editing existing campaign), mark as set


watch(() => props.startDate, () => {
  if (props.startDate && props.startDate !== 'SEND_NOW') {
    hasBeenSet.value = true
    sendingStrategy.value = 'scheduled'
  } else if (props.startDate === 'SEND_NOW') {
    hasBeenSet.value = false
    sendingStrategy.value = 'now'
  }
})
</script>
