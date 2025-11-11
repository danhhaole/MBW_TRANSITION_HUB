<template>
  <div class="space-y-6 animate-fadeIn">
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-900">
          {{ __('Create Recruitment Message') }}
        </h3>
        <Badge theme="purple" variant="subtle">
          {{ selectedChannel || __('No Channel') }}
        </Badge>
      </div>

      <p class="text-gray-600 mb-6">
        {{ __('Create compelling content to attract the right candidates for your job opening.') }}
      </p>

      <!-- Message Type -->
      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-3">
          {{ __('Message Type') }}
        </label>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div
            class="border-2 rounded-lg p-4 cursor-pointer transition-all"
            :class="messageType === 'job_invitation' ? 'border-purple-500 bg-purple-50' : 'border-gray-200 hover:border-gray-300'"
            @click="messageType = 'job_invitation'"
          >
            <FeatherIcon 
              name="mail" 
              class="h-6 w-6 mb-2"
              :class="messageType === 'job_invitation' ? 'text-purple-600' : 'text-gray-400'"
            />
            <h4 class="text-sm font-semibold text-gray-900">
              {{ __('Job Invitation') }}
            </h4>
            <p class="text-xs text-gray-600 mt-1">
              {{ __('Invite candidates to apply') }}
            </p>
          </div>

          <div
            class="border-2 rounded-lg p-4 cursor-pointer transition-all"
            :class="messageType === 'job_alert' ? 'border-purple-500 bg-purple-50' : 'border-gray-200 hover:border-gray-300'"
            @click="messageType = 'job_alert'"
          >
            <FeatherIcon 
              name="bell" 
              class="h-6 w-6 mb-2"
              :class="messageType === 'job_alert' ? 'text-purple-600' : 'text-gray-400'"
            />
            <h4 class="text-sm font-semibold text-gray-900">
              {{ __('Job Alert') }}
            </h4>
            <p class="text-xs text-gray-600 mt-1">
              {{ __('Notify about new opportunity') }}
            </p>
          </div>
        </div>
      </div>

      <!-- Content Editor -->
      <div class="border-t border-gray-200 pt-6">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Message Title') }}
            </label>
            <FormControl
              v-model="messageTitle"
              type="text"
              :placeholder="__('e.g., Exciting Opportunity: Senior Frontend Developer')"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Message Content') }}
            </label>
            <div class="bg-gray-50 rounded-lg p-8 text-center border-2 border-dashed border-gray-300">
              <FeatherIcon name="file-text" class="h-12 w-12 text-gray-400 mx-auto mb-3" />
              <p class="text-gray-500 mb-2">
                {{ __('Recruitment message editor will be implemented here') }}
              </p>
              <p class="text-xs text-gray-400">
                {{ __('Include job details, requirements, and application instructions') }}
              </p>
            </div>
          </div>

          <!-- Include Job Details -->
          <div class="flex items-center space-x-2">
            <input
              id="include-job-details"
              type="checkbox"
              v-model="includeJobDetails"
              class="h-4 w-4 text-purple-600 border-gray-300 rounded"
            />
            <label for="include-job-details" class="text-sm text-gray-700">
              {{ __('Include full job description in message') }}
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FeatherIcon, Badge, FormControl } from 'frappe-ui'

defineProps({
  selectedChannel: String
})

const messageType = ref('job_invitation')
const messageTitle = ref('')
const includeJobDetails = ref(true)

const __ = (text) => text
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-in;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
