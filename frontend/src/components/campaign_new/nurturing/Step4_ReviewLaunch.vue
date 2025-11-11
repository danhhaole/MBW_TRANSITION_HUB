<template>
  <div class="space-y-6 animate-fadeIn">
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">
        {{ __('Review & Launch Nurturing Campaign') }}
      </h3>

      <p class="text-gray-600 mb-6">
        {{ __('Review your nurturing campaign before launching.') }}
      </p>

      <!-- Campaign Summary -->
      <div class="space-y-4">
        <div class="bg-green-50 rounded-lg p-4 border border-green-200">
          <h4 class="text-sm font-semibold text-green-900 mb-3">
            {{ __('Campaign Overview') }}
          </h4>
          <dl class="space-y-2">
            <div class="flex justify-between text-sm">
              <dt class="text-green-700">{{ __('Campaign Name:') }}</dt>
              <dd class="font-medium text-green-900">{{ campaignName || '-' }}</dd>
            </div>
            <div class="flex justify-between text-sm">
              <dt class="text-green-700">{{ __('Type:') }}</dt>
              <dd class="font-medium text-green-900">{{ __('Nurturing') }}</dd>
            </div>
            <div class="flex justify-between text-sm">
              <dt class="text-green-700">{{ __('Channel:') }}</dt>
              <dd class="font-medium text-green-900">{{ selectedChannel || '-' }}</dd>
            </div>
          </dl>
        </div>
      </div>

      <!-- Launch Settings -->
      <div class="mt-6 border-t border-gray-200 pt-6">
        <h4 class="text-sm font-semibold text-gray-900 mb-4">
          {{ __('Launch Settings') }}
        </h4>
        <div class="bg-gray-50 rounded-lg p-4">
          <p class="text-sm text-gray-600">
            {{ __('Launch settings will be implemented here') }}
          </p>
        </div>
      </div>

      <!-- Confirmation -->
      <div class="mt-6 bg-green-50 rounded-lg p-4 border border-green-200">
        <div class="flex items-start">
          <FeatherIcon name="check-circle" class="h-5 w-5 text-green-600 mt-0.5 mr-3" />
          <div>
            <h5 class="text-sm font-semibold text-green-900 mb-1">
              {{ __('Ready to Start Nurturing?') }}
            </h5>
            <p class="text-sm text-green-800">
              {{ __('Your nurturing campaign will help build stronger relationships with your audience.') }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { FeatherIcon } from 'frappe-ui'

defineProps({
  campaignName: String,
  selectedChannel: String
})

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
