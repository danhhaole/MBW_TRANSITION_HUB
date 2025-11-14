<template>
  <div class=" flex gap-2">
    <!-- QR Code Preview -->
    <div v-if="qrData?.qr_image" class="bg-white border border-gray-200 rounded-lg p-4 flex-1">
      <div class="flex items-start gap-4">
        <!-- QR Code Image -->
        <div class="flex-shrink-0">
          <img 
            :src="qrData.qr_image" 
            alt="QR Code" 
            class="w-32 h-32 border border-gray-200 rounded"
          />
        </div>
        
        <!-- QR Code Info -->
        <div class="flex-1 min-w-0">
          <h4 class="text-sm font-medium text-gray-900 mb-2">
            {{ __('QR Code Generated') }}
          </h4>
          
          <div class="space-y-2">
            <div>
              <label class="text-xs text-gray-500">{{ __('Target URL') }}</label>
              <p class="text-xs text-gray-900 font-mono break-all">
                {{ qrData.url }}
              </p>
            </div>
            
            <div class="grid grid-cols-2 gap-2 text-xs">
              <div>
                <label class="text-gray-500">UTM Source</label>
                <p class="text-gray-900">{{ qrData.utm_params?.utm_source }}</p>
              </div>
              <div>
                <label class="text-gray-500">UTM Medium</label>
                <p class="text-gray-900">{{ qrData.utm_params?.utm_medium }}</p>
              </div>
            </div>
          </div>
          
          <!-- Actions -->
          <div class="flex gap-2 mt-3">
            <Button
              @click="downloadQR"
              variant="ghost"
              size="sm"
            >
              <template #prefix>
                <FeatherIcon name="download" class="h-3 w-3" />
              </template>
              {{ __('Download') }}
            </Button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- QR Code Configuration -->
    <div class="bg-gray-50 border border-gray-200 rounded-lg p-4 flex-1">
      <h4 class="text-sm font-medium text-gray-900 mb-3">
        {{ __('QR Code Settings') }}
      </h4>
      
      <div class="space-y-3">
        <!-- UTM Campaign (readonly) -->
        <div>
          <label class="block text-xs font-medium text-gray-700 mb-1">
            {{ __('UTM Campaign') }}
          </label>
          <FormControl
            :model-value="campaignId"
            :placeholder="__('Campaign ID will be used automatically')"
            disabled
          />
          <p class="text-xs text-gray-500 mt-1">
            {{ __('Automatically set to current campaign ID') }}
          </p>
        </div>
        
        <!-- UTM Source -->
        <div>
          <label class="block text-xs font-medium text-gray-700 mb-1">
            {{ __('UTM Source') }}
          </label>
          <FormControl
            :model-value="localContent.utm_source"
            @update:model-value="updateUtmSource"
            :placeholder="__('e.g., qr_code, poster, flyer')"
          />
        </div>
        
        <!-- UTM Medium -->
        <div>
          <label class="block text-xs font-medium text-gray-700 mb-1">
            {{ __('UTM Medium') }}
          </label>
          <FormControl
            :model-value="localContent.utm_medium"
            @update:model-value="updateUtmMedium"
            :placeholder="__('e.g., qr, print, offline')"
          />
        </div>
      </div>
      
      <!-- Generate Button -->
      <div class="mt-4">
        <Button
          @click="generateQR"
          variant="solid"
          size="sm"
          :loading="generating"
          :disabled="!landingPageUrl"
        >
          <template #prefix>
            <FeatherIcon name="qr-code" class="h-3 w-3" />
          </template>
          {{ qrData ? __('Regenerate QR Code') : __('Generate QR Code') }}
        </Button>
        
        <p v-if="!landingPageUrl" class="text-xs text-red-600 mt-1">
          {{ __('Please create a landing page first') }}
        </p>
      </div>
    </div>
    
    <!-- Error Display -->
    <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-3">
      <div class="flex items-start">
        <FeatherIcon name="alert-circle" class="h-4 w-4 text-red-600 mt-0.5 mr-2" />
        <div>
          <p class="text-sm font-medium text-red-900">
            {{ __('Error generating QR code') }}
          </p>
          <p class="text-xs text-red-700">
            {{ error }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { FeatherIcon, FormControl, Button, call } from 'frappe-ui'

const props = defineProps({
  content: {
    type: Object,
    default: () => ({
      utm_campaign: '',
      utm_source: 'qr_code',
      utm_medium: 'qr',
      qr_data: null
    })
  },
  landingPageUrl: {
    type: String,
    default: ''
  },
  campaignId: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:content'])

// State
const generating = ref(false)
const error = ref(null)

// Local content
const localContent = computed({
  get: () => props.content,
  set: (value) => emit('update:content', value)
})

// QR Data from content
const qrData = computed(() => localContent.value.qr_data)

// Generate QR Code
const generateQR = async () => {
  if (!props.landingPageUrl || !props.campaignId) {
    error.value = 'Missing landing page URL or campaign ID'
    return
  }
  
  generating.value = true
  error.value = null
  
  try {
    const response = await call('mbw_mira.api.create_landing_page_qrcode', {
      landing_page_url: props.landingPageUrl,
      campaign_id: props.campaignId,
      utm_source: localContent.value.utm_source,
      utm_medium: localContent.value.utm_medium,
      utm_campaign: props.campaignId
    })
    
    if (response?.status === 'success' && response?.data) {
      // Update content with QR data
      localContent.value = {
        ...localContent.value,
        qr_data: response.data
      }
      console.log('✅ QR Code generated:', response.data)
    } else {
      error.value = 'Failed to generate QR code'
    }
  } catch (err) {
    error.value = err.message || 'Failed to generate QR code'
    console.error('❌ Error generating QR code:', err)
  } finally {
    generating.value = false
  }
}

// Regenerate QR Code
const regenerateQR = () => {
  generateQR()
}

// Download QR Code
const downloadQR = () => {
  if (!qrData.value?.qr_image) return
  
  // Create download link
  const link = document.createElement('a')
  link.href = qrData.value.qr_image
  link.download = `qr-code-${props.campaignId || 'campaign'}.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// Update UTM parameters
const updateUtmSource = (value) => {
  localContent.value = {
    ...localContent.value,
    utm_source: value
  }
}

const updateUtmMedium = (value) => {
  localContent.value = {
    ...localContent.value,
    utm_medium: value
  }
}

// Update content when local changes
const updateContent = () => {
  emit('update:content', localContent.value)
}

// Watch landing page URL changes
watch(() => props.landingPageUrl, (newUrl) => {
  if (newUrl && !qrData.value) {
    // Auto-generate QR when landing page is available
    setTimeout(() => {
      generateQR()
    }, 500)
  }
})
</script>

<style scoped>
/* Add any custom styles here */
</style>
