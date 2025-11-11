<template>
  <div class="bg-white rounded-lg border border-gray-200 p-6">
    <div class="flex items-center mb-4">
      <div class="w-8 h-8 rounded-lg bg-purple-500 text-white flex items-center justify-center mr-3">
        <FeatherIcon name="link" class="h-4 w-4" />
      </div>
      <div>
        <h4 class="text-sm font-semibold text-gray-900">
          {{ __('2.1. Landing Page & CTA Link') }}
        </h4>
        <p class="text-xs text-gray-500">
          {{ __('Choose landing page and configure call-to-action') }}
        </p>
      </div>
    </div>

    <div class="space-y-4">
      <!-- Landing Page Selection -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Choose Landing Page') }}
          <span class="text-red-500">*</span>
        </label>
        <FormControl
          type="select"
          :model-value="landingPage"
          :options="landingPageOptions"
          :placeholder="__('Select a landing page...')"
          @update:model-value="$emit('update:landingPage', $event)"
        />
        <p class="text-xs text-gray-500 mt-1">
          {{ __('Ensure the form on the landing page is connected to sync Lead data to CRM') }}
        </p>
      </div>

      <!-- CTA Link Configuration -->
      <div v-if="landingPage" class="border border-gray-200 rounded-lg p-4 bg-gray-50">
        <div class="flex items-start mb-3">
          <FeatherIcon name="info" class="h-4 w-4 text-blue-600 mt-0.5 mr-2 flex-shrink-0" />
          <div class="text-xs text-gray-600">
            {{ __('The form on the landing page must be connected to automatically sync Lead data to the system') }}
          </div>
        </div>

        <!-- Preview Landing Page URL -->
        <div class="bg-white border border-gray-200 rounded p-3">
          <div class="flex items-center justify-between">
            <div class="flex-1 mr-3">
              <div class="text-xs text-gray-500 mb-1">{{ __('Landing Page URL') }}</div>
              <div class="text-sm text-gray-900 font-mono break-all">
                {{ getLandingPageUrl(landingPage) }}
              </div>
            </div>
            <button
              @click="copyToClipboard(getLandingPageUrl(landingPage))"
              class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded transition-colors"
              :title="__('Copy URL')"
            >
              <FeatherIcon name="copy" class="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      <!-- Form Structure Info -->
      <div v-if="landingPage" class="border-l-4 border-yellow-400 bg-yellow-50 p-4 rounded">
        <div class="flex items-start">
          <FeatherIcon name="alert-triangle" class="h-5 w-5 text-yellow-600 mt-0.5 mr-3 flex-shrink-0" />
          <div>
            <h5 class="text-sm font-semibold text-yellow-900 mb-1">
              {{ __('Form Structure Requirements') }}
            </h5>
            <p class="text-xs text-yellow-800">
              {{ __('Ensure the form on the landing page is properly connected to sync data to CRM. Contact your administrator if you need help setting this up.') }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { FeatherIcon, FormControl } from 'frappe-ui'
import { 
  getLandingPageOptions, 
  getLandingPageUrl as getPageUrl,
  isFormConnected 
} from '@/data/mockLandingPages'

const props = defineProps({
  landingPage: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:landingPage'])

// Landing page options from mock data
const landingPageOptions = computed(() => getLandingPageOptions())

// Get landing page URL
const getLandingPageUrl = (pageId) => {
  return getPageUrl(pageId)
}

// Copy to clipboard
const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    // Could add toast notification here
    console.log('✅ Copied to clipboard:', text)
  })
}
</script>

<style scoped>
/* Add any custom styles here */
</style>
