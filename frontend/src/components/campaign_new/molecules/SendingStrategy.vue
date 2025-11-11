<template>
  <div class="bg-gray-50 rounded-lg p-6">
    <h5 class="text-md font-medium text-gray-900 mb-4">
      {{ title || __("Sending Strategy") }}
    </h5>
    <p class="text-sm text-gray-600 mb-4">
      {{ description || __("When do you want to send this campaign?") }}
    </p>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Send Now -->
      <div 
        class="border rounded-lg p-4 bg-white cursor-pointer transition-colors"
        :class="localStrategy === 'now' ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' : 'border-gray-200 hover:border-gray-300'"
        @click="localStrategy = 'now'"
      >
        <div class="text-center">
          <div class="flex items-center justify-center w-12 h-12 rounded-full mx-auto mb-3"
               :class="localStrategy === 'now' ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'">
            <FeatherIcon name="send" class="h-6 w-6" />
          </div>
          <h6 class="text-sm font-semibold mb-1"
              :class="localStrategy === 'now' ? 'text-blue-900' : 'text-gray-900'">
            {{ __("Send Now") }}
          </h6>
          <p class="text-xs text-gray-600">
            {{ __("Send campaign immediately") }}
          </p>
        </div>
      </div>

      <!-- Schedule Send -->
      <div 
        class="border rounded-lg p-4 bg-white cursor-pointer transition-colors"
        :class="localStrategy === 'scheduled' ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' : 'border-gray-200 hover:border-gray-300'"
        @click="localStrategy = 'scheduled'"
      >
        <div class="text-center">
          <div class="flex items-center justify-center w-12 h-12 rounded-full mx-auto mb-3"
               :class="localStrategy === 'scheduled' ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'">
            <FeatherIcon name="calendar" class="h-6 w-6" />
          </div>
          <h6 class="text-sm font-semibold mb-1"
              :class="localStrategy === 'scheduled' ? 'text-blue-900' : 'text-gray-900'">
            {{ __("Schedule Send") }}
          </h6>
          <p class="text-xs text-gray-600">
            {{ __("Choose specific time to send campaign") }}
          </p>
        </div>
      </div>
    </div>

    <!-- Schedule Date/Time Input -->
    <div v-if="localStrategy === 'scheduled'" class="mt-4">
      <label class="block text-sm font-medium text-gray-700 mb-2">
        {{ __("Schedule Date & Time") }}
      </label>
      <FormControl
        v-model="localScheduledDate"
        type="datetime-local"
        size="md"
      />
      <p class="text-xs text-gray-500 mt-2">
        {{ __("Campaign will be sent at the specified date and time") }}
      </p>
    </div>

    <!-- Send Now Info -->
    <div v-else class="mt-4 bg-blue-50 rounded-lg p-3 border border-blue-200">
      <div class="flex items-start">
        <FeatherIcon name="info" class="h-4 w-4 text-blue-600 mt-0.5 mr-2 flex-shrink-0" />
        <p class="text-xs text-blue-800">
          {{ __("Campaign will be sent immediately after activation") }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { FeatherIcon, FormControl } from 'frappe-ui'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  strategy: {
    type: String,
    default: 'now' // 'now' or 'scheduled'
  },
  scheduledDate: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:strategy', 'update:scheduledDate'])

// Local state
const localStrategy = computed({
  get: () => props.strategy,
  set: (value) => {
    emit('update:strategy', value)
    // Clear scheduled date if switching to 'now'
    if (value === 'now') {
      emit('update:scheduledDate', '')
    }
  }
})

const localScheduledDate = computed({
  get: () => props.scheduledDate,
  set: (value) => emit('update:scheduledDate', value)
})

// Translation helper
const __ = (text) => text
</script>

<style scoped>
/* Add any custom styles here */
</style>
