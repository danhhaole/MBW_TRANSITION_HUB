<template>
  <div class="bg-gray-50 rounded-lg p-4">
    <!-- Add Tag Configuration -->
    <div v-if="actionType === 'add_tag'" class="space-y-3">
      <label class="block text-sm font-medium text-gray-700">
        {{ __("Tag to Add") }}
      </label>
      <div class="flex space-x-2">
        <input
          :value="actionData.tag_name || ''"
          @input="updateData({ tag_name: $event.target.value })"
          type="text"
          :placeholder="__('Enter tag name (e.g., Webinar MBWN DMS 2110)')"
          class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
        <Button variant="outline" size="sm">
          <FeatherIcon name="plus" class="h-4 w-4 mr-1" />
          {{ __("Create") }}
        </Button>
      </div>
      <p class="text-xs text-gray-500">
        {{ __("This tag will be added to the candidate's profile and category") }}
      </p>
    </div>

    <!-- Remove Tag Configuration -->
    <div v-else-if="actionType === 'remove_tag'" class="space-y-3">
      <label class="block text-sm font-medium text-gray-700">
        {{ __("Tag to Remove") }}
      </label>
      <select
        :value="actionData.tag_id || ''"
        @change="updateData({ tag_id: $event.target.value })"
        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      >
        <option value="">{{ __("Select tag to remove...") }}</option>
        <option v-for="tag in availableTags" :key="tag.id" :value="tag.id">
          {{ tag.name }}
        </option>
      </select>
      <p class="text-xs text-gray-500">
        {{ __("This tag will be removed from the candidate's profile") }}
      </p>
    </div>

    <!-- Unsubscribe Configuration -->
    <div v-else-if="actionType === 'unsubscribe'" class="space-y-3">
      <div class="flex items-center space-x-2">
        <FeatherIcon name="mail-x" class="h-5 w-5 text-red-500" />
        <span class="text-sm font-medium text-gray-900">
          {{ __("Unsubscribe from emails") }}
        </span>
      </div>
      <p class="text-xs text-gray-500">
        {{ __("The candidate will be marked as unsubscribed and will not receive future emails") }}
      </p>
      
      <div class="flex items-center space-x-2">
        <input
          :checked="actionData.send_confirmation || false"
          @change="updateData({ send_confirmation: $event.target.checked })"
          type="checkbox"
          class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
        />
        <label class="text-sm text-gray-700">
          {{ __("Send unsubscribe confirmation email") }}
        </label>
      </div>
    </div>

    <!-- Next Scenario Configuration -->
    <div v-else-if="actionType === 'next_scenario'" class="space-y-3">
      <label class="block text-sm font-medium text-gray-700">
        {{ __("Select Scenario") }}
      </label>
      <select
        :value="actionData.scenario_id || ''"
        @change="updateData({ scenario_id: $event.target.value })"
        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      >
        <option value="">{{ __("Select scenario to execute...") }}</option>
        <option v-for="scenario in availableScenarios" :key="scenario.id" :value="scenario.id">
          {{ scenario.name }}
        </option>
      </select>
      
      <div class="space-y-2">
        <label class="block text-sm font-medium text-gray-700">
          {{ __("Delay before execution") }}
        </label>
        <div class="flex space-x-2">
          <input
            :value="actionData.delay_value || 0"
            @input="updateData({ delay_value: parseInt($event.target.value) || 0 })"
            type="number"
            min="0"
            class="w-20 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
          <select
            :value="actionData.delay_unit || 'minutes'"
            @change="updateData({ delay_unit: $event.target.value })"
            class="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option value="minutes">{{ __("Minutes") }}</option>
            <option value="hours">{{ __("Hours") }}</option>
            <option value="days">{{ __("Days") }}</option>
          </select>
        </div>
      </div>
      
      <p class="text-xs text-gray-500">
        {{ __("The selected scenario will be executed after the specified delay") }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Button, FeatherIcon } from 'frappe-ui'

// Props
const props = defineProps({
  actionType: {
    type: String,
    required: true
  },
  actionData: {
    type: Object,
    default: () => ({})
  }
})

// Emits
const emit = defineEmits(['update:data'])

// Translation helper
const __ = (text) => text

// Mock data - these should come from props or API calls
const availableTags = ref([
  { id: '1', name: 'Webinar MBWN DMS 2110' },
  { id: '2', name: 'Interested in React' },
  { id: '3', name: 'Senior Developer' },
  { id: '4', name: 'Remote Worker' }
])

const availableScenarios = ref([
  { id: '1', name: 'Follow-up Email Sequence' },
  { id: '2', name: 'Interview Invitation' },
  { id: '3', name: 'Technical Assessment' },
  { id: '4', name: 'Rejection Email' }
])

// Methods
const updateData = (newData) => {
  const updatedData = { ...props.actionData, ...newData }
  emit('update:data', updatedData)
}
</script>
