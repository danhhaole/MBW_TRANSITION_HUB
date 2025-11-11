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

    <!-- Show selection cards only on first time or after reset -->
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

    <!-- Show DateTimePicker after selection -->
    <div v-else>
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
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { FeatherIcon, DateTimePicker } from 'frappe-ui'
import moment from 'moment'

const props = defineProps({
  startDate: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:startDate'])

// Track if user has made a selection
const hasBeenSet = ref(!!props.startDate)

// Initialize sendingStrategy based on existing start_date
const sendingStrategy = ref(props.startDate ? 'scheduled' : 'now')

// Select strategy and mark as set
const selectStrategy = (strategy) => {
  sendingStrategy.value = strategy
  hasBeenSet.value = true
  
  if (strategy === 'now') {
    // Set to current datetime
    const formattedNow = moment().format('YYYY-MM-DD HH:mm:ss')
    emit('update:startDate', formattedNow)
  } else {
    // Clear for user to select custom date
    emit('update:startDate', '')
  }
}

// Reset to show selection cards again
const resetSelection = () => {
  hasBeenSet.value = false
  sendingStrategy.value = 'now'
}

// Set default start_date if not exists (only on first load)
if (!props.startDate) {
  const formattedNow = moment().format('YYYY-MM-DD HH:mm:ss')
  emit('update:startDate', formattedNow)
}
</script>
