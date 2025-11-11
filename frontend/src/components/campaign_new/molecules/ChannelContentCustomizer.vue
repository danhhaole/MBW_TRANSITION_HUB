<template>
  <div class="bg-white rounded-lg border border-gray-200 p-6">
    <div class="flex items-center mb-4">
      <div class="w-8 h-8 rounded-lg bg-indigo-500 text-white flex items-center justify-center mr-3">
        <FeatherIcon name="settings" class="h-4 w-4" />
      </div>
      <div>
        <h4 class="text-sm font-semibold text-gray-900">
          {{ __('2.2. Channel-Specific Content Customization') }}
        </h4>
        <p class="text-xs text-gray-500">
          {{ __('Customize content and tracking for each channel') }}
        </p>
      </div>
    </div>

    <!-- Channel Customization Table -->
    <div class="border border-gray-200 rounded-lg overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider w-24">
              {{ __('Channel') }}
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
              {{ __('Content Presentation') }}
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
              {{ __('Tracking Features') }}
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
              {{ __('UTM Tracking') }}
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <!-- Facebook Row -->
          <tr v-if="channels.includes('facebook')" class="hover:bg-gray-50">
            <td class="px-4 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="w-8 h-8 rounded-lg bg-blue-500 text-white flex items-center justify-center mr-2">
                  <FeatherIcon name="facebook" class="h-4 w-4" />
                </div>
                <span class="text-sm font-medium text-gray-900">Facebook</span>
              </div>
            </td>
            <td class="px-4 py-4">
              <div class="text-xs text-gray-600 space-y-1">
                <div><strong>{{ __('Presentation') }}:</strong> Text Area, Image/Video, View More button</div>
              </div>
            </td>
            <td class="px-4 py-4">
              <div class="text-xs text-gray-600 space-y-1">
                <div><strong>{{ __('Track Link') }}:</strong> {{ __('Auto-track URL clicks from selected Landing Page') }}</div>
              </div>
            </td>
            <td class="px-4 py-4">
              <div class="space-y-1">
                <div class="text-xs">
                  <code class="bg-gray-100 px-2 py-0.5 rounded text-gray-800">utm_source: facebook</code>
                </div>
                <div class="text-xs">
                  <code class="bg-gray-100 px-2 py-0.5 rounded text-gray-800">utm_campaign: {{ campaignName || '(Campaign Name)' }}</code>
                </div>
                <div class="text-xs">
                  <code class="bg-gray-100 px-2 py-0.5 rounded text-gray-800">utm_tag: (Tags)</code>
                </div>
              </div>
            </td>
          </tr>

          <!-- Zalo Row -->
          <tr v-if="channels.includes('zalo')" class="hover:bg-gray-50">
            <td class="px-4 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="w-8 h-8 rounded-lg bg-green-500 text-white flex items-center justify-center mr-2">
                  <FeatherIcon name="message-circle" class="h-4 w-4" />
                </div>
                <span class="text-sm font-medium text-gray-900">Zalo</span>
              </div>
            </td>
            <td class="px-4 py-4">
              <div class="text-xs text-gray-600 space-y-1">
                <div><strong>{{ __('Presentation') }}:</strong> Text Area, Image (no video), View More button</div>
              </div>
            </td>
            <td class="px-4 py-4">
              <div class="text-xs text-gray-600 space-y-1">
                <div><strong>{{ __('Track Link') }}:</strong> {{ __('Auto-track URL clicks from selected Landing Page') }}</div>
              </div>
            </td>
            <td class="px-4 py-4">
              <div class="space-y-1">
                <div class="text-xs">
                  <code class="bg-gray-100 px-2 py-0.5 rounded text-gray-800">utm_source: zalo</code>
                </div>
                <div class="text-xs">
                  <code class="bg-gray-100 px-2 py-0.5 rounded text-gray-800">utm_campaign: {{ campaignName || '(Campaign Name)' }}</code>
                </div>
                <div class="text-xs">
                  <code class="bg-gray-100 px-2 py-0.5 rounded text-gray-800">utm_tag: (Tags)</code>
                </div>
              </div>
            </td>
          </tr>

          <!-- Other Channels (Placeholder) -->
          <tr v-if="channels.length === 0">
            <td colspan="4" class="px-4 py-8 text-center text-sm text-gray-500">
              {{ __('No channels selected. Please add channels above to see customization options.') }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- UTM Tracking Info -->
    <div class="mt-4 border-l-4 border-blue-400 bg-blue-50 p-4 rounded">
      <div class="flex items-start">
        <FeatherIcon name="info" class="h-5 w-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0" />
        <div>
          <h5 class="text-sm font-semibold text-blue-900 mb-1">
            {{ __('About UTM Tracking') }}
          </h5>
          <p class="text-xs text-blue-800">
            {{ __('UTM parameters are automatically added to track the source and effectiveness of each channel. This helps you analyze which channels bring the best results.') }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { FeatherIcon } from 'frappe-ui'

const props = defineProps({
  channels: {
    type: Array,
    default: () => []
  },
  campaignName: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
/* Custom table styles */
table {
  font-size: 0.875rem;
}

code {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.75rem;
}
</style>
