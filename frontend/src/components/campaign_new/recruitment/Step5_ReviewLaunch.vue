<template>
  <div class="space-y-6 animate-fadeIn">
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">
        {{ __('Review & Launch Recruitment Campaign') }}
      </h3>

      <p class="text-gray-600 mb-6">
        {{ __('Review your recruitment campaign details before launching.') }}
      </p>

      <!-- Campaign Summary -->
      <div class="space-y-4">
        <!-- Campaign Info -->
        <div class="bg-purple-50 rounded-lg p-4 border border-purple-200">
          <h4 class="text-sm font-semibold text-purple-900 mb-3">
            {{ __('Campaign Overview') }}
          </h4>
          <dl class="space-y-2">
            <div class="flex justify-between text-sm">
              <dt class="text-purple-700">{{ __('Campaign Name:') }}</dt>
              <dd class="font-medium text-purple-900">{{ campaignName || '-' }}</dd>
            </div>
            <div class="flex justify-between text-sm">
              <dt class="text-purple-700">{{ __('Type:') }}</dt>
              <dd class="font-medium text-purple-900">{{ __('Recruitment') }}</dd>
            </div>
            <div class="flex justify-between text-sm">
              <dt class="text-purple-700">{{ __('Channel:') }}</dt>
              <dd class="font-medium text-purple-900">{{ selectedChannel || '-' }}</dd>
            </div>
          </dl>
        </div>

        <!-- Job Opening Info -->
        <div class="bg-gray-50 rounded-lg p-4">
          <h4 class="text-sm font-semibold text-gray-900 mb-3">
            {{ __('Job Opening') }}
          </h4>
          <div class="flex items-center">
            <FeatherIcon name="briefcase" class="h-5 w-5 text-gray-400 mr-2" />
            <span class="text-sm text-gray-600">
              {{ __('No job opening selected') }}
            </span>
          </div>
        </div>

        <!-- Target Candidates -->
        <div class="bg-gray-50 rounded-lg p-4">
          <h4 class="text-sm font-semibold text-gray-900 mb-3">
            {{ __('Target Candidates') }}
          </h4>
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-600">{{ __('Potential Candidates:') }}</span>
            <span class="text-lg font-bold text-purple-600">0</span>
          </div>
        </div>
      </div>

      <!-- Application Tracking -->
      <div class="mt-6 border-t border-gray-200 pt-6">
        <h4 class="text-sm font-semibold text-gray-900 mb-4">
          {{ __('Application Tracking') }}
        </h4>
        <div class="space-y-3">
          <div class="flex items-center space-x-2">
            <input
              id="track-applications"
              type="checkbox"
              v-model="trackApplications"
              class="h-4 w-4 text-purple-600 border-gray-300 rounded"
            />
            <label for="track-applications" class="text-sm text-gray-700">
              {{ __('Track applications from this campaign') }}
            </label>
          </div>

          <div class="flex items-center space-x-2">
            <input
              id="auto-response"
              type="checkbox"
              v-model="autoResponse"
              class="h-4 w-4 text-purple-600 border-gray-300 rounded"
            />
            <label for="auto-response" class="text-sm text-gray-700">
              {{ __('Send automatic response to applicants') }}
            </label>
          </div>
        </div>
      </div>

      <!-- Launch Confirmation -->
      <div class="mt-6 bg-purple-50 rounded-lg p-4 border border-purple-200">
        <div class="flex items-start">
          <FeatherIcon name="users" class="h-5 w-5 text-purple-600 mt-0.5 mr-3" />
          <div>
            <h5 class="text-sm font-semibold text-purple-900 mb-1">
              {{ __('Ready to Start Recruiting?') }}
            </h5>
            <p class="text-sm text-purple-800">
              {{ __('Your recruitment campaign will reach potential candidates and help you find the perfect fit for your team.') }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FeatherIcon } from 'frappe-ui'

defineProps({
  campaignName: String,
  selectedChannel: String
})

const trackApplications = ref(true)
const autoResponse = ref(true)

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
