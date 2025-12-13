<template>
  <div class="space-y-4">
    <!-- QR Codes List -->
    <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
      <div class="flex items-center justify-between mb-3">
        <h4 class="text-sm font-medium text-gray-900">
          {{ __('QR Codes') }} ({{ qrCodesList.length }})
        </h4>
        <Button
          @click="showAddQRModal = true"
          variant="solid"
          size="sm"
        >
          <template #prefix>
            <FeatherIcon name="plus" class="h-3 w-3" />
          </template>
          {{ __('Add QR Code') }}
        </Button>
      </div>

      <!-- QR Codes Grid -->
      <div v-if="qrCodesList.length > 0" class="grid grid-cols-1 gap-3">
        <div
          v-for="qr in qrCodesList"
          :key="qr.name"
          class="bg-white border border-gray-200 rounded-lg p-3 hover:border-blue-300 transition-colors"
        >
          <div class="flex items-start gap-3">
            <!-- QR Image Thumbnail -->
            <div v-if="qr.qr_image" class="flex-shrink-0">
              <img
                :src="qr.qr_image"
                alt="QR Code"
                class="w-32 h-32 border border-gray-200 rounded"
              />
            </div>
            <div v-else class="flex-shrink-0 w-32 h-32 bg-gray-100 border border-gray-200 rounded flex items-center justify-center">
              <FeatherIcon name="image" class="h-6 w-6 text-gray-400" />
            </div>

            <!-- QR Info -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between">
                <div>
                  <h5 class="text-sm font-medium text-gray-900">
                    {{ qr.qr_name }}
                  </h5>
                  <p v-if="qr.description" class="text-xs text-gray-500 mt-0.5">
                    {{ qr.description }}
                  </p>
                </div>
                <div class="flex items-center gap-1">
                  <Button
                    v-if="qr.qr_image"
                    @click="downloadQRCode(qr)"
                    variant="ghost"
                    size="sm"
                    class="p-1"
                  >
                    <FeatherIcon name="download" class="h-3 w-3" />
                  </Button>
                  <Button
                    @click="editQRCode(qr)"
                    variant="ghost"
                    size="sm"
                    class="p-1"
                  >
                    <FeatherIcon name="edit" class="h-3 w-3" />
                  </Button>
                  <Button
                    @click="deleteQRCode(qr)"
                    variant="ghost"
                    size="sm"
                    class="p-1 text-red-600 hover:text-red-700"
                  >
                    <FeatherIcon name="trash-2" class="h-3 w-3" />
                  </Button>
                </div>
              </div>

              <!-- UTM Info -->
              <div class="grid grid-cols-2 gap-2 mt-2 text-xs">
                <div>
                  <label class="text-gray-500">Source</label>
                  <p class="text-gray-900">{{ qr.utm_source }}</p>
                </div>
                <div>
                  <label class="text-gray-500">Medium</label>
                  <p class="text-gray-900">{{ qr.utm_medium }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-6 border-2 border-dashed border-gray-200 rounded-lg">
        <FeatherIcon name="qr-code" class="h-10 w-10 text-gray-400 mx-auto mb-2" />
        <p class="text-sm text-gray-600 mb-1">{{ __('No QR codes yet') }}</p>
        <p class="text-xs text-gray-500">{{ __('Click "Add QR Code" to create one') }}</p>
      </div>
    </div>

    <!-- Add/Edit QR Modal -->
    <Dialog
      v-model="showAddQRModal"
      :options="{
        title: editingQR ? __('Edit QR Code') : __('Add QR Code'),
        size: 'xl'
      }"
    >
      <template #body-content>
        <div class="space-y-4">
          <!-- QR Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ __('QR Name') }} <span class="text-red-500">*</span>
            </label>
            <FormControl
              v-model="newQRData.qr_name"
              :placeholder="__('e.g., Facebook Post QR, Poster QR, Event QR')"
            />
          </div>

          <!-- Description -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ __('Description') }}
            </label>
            <FormControl
              type="textarea"
              v-model="newQRData.description"
              :placeholder="__('Describe the purpose of this QR code')"
              :rows="2"
            />
          </div>

          <!-- Purpose -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ __('Purpose') }}
            </label>
            <FormControl
              v-model="newQRData.purpose"
              :placeholder="__('e.g., Social Media, Print Material, Event')"
            />
          </div>

          <div class="grid grid-cols-1 gap-4">
            <!-- UTM Source -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ __('UTM Source') }} <span class="text-red-500">*</span>
              </label>
              <FormControl
                v-model="newQRData.utm_source"
                :placeholder="__('e.g., qr_code, poster, flyer')"
              />
            </div>

            <!-- UTM Medium -->
            <!-- <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ __('UTM Medium') }} <span class="text-red-500">*</span>
              </label>
              <FormControl
                v-model="newQRData.utm_medium"
                :placeholder="__('e.g., qr, print, offline')"
              />
            </div> -->
          </div>

          <!-- Preview if QR exists -->
          <div v-if="editingQR && editingQR.qr_image" class="border-t border-gray-200 pt-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Current QR Code') }}
            </label>
            <img
              :src="editingQR.qr_image"
              alt="QR Code"
              class="w-32 h-32 border border-gray-200 rounded"
            />
          </div>
        </div>
      </template>

      <template #actions>
        <Button
          @click="showAddQRModal = false"
          variant="ghost"
        >
          {{ __('Cancel') }}
        </Button>
        <Button
          @click="saveQRCode"
          variant="solid"
          :loading="savingQR"
        >
          {{ editingQR ? __('Update & Generate') : __('Create & Generate') }}
        </Button>
      </template>
    </Dialog>

    <!-- Old QR Code Preview (Hidden, kept for backward compatibility) -->
    <div v-if="false && qrData?.qr_image" class="bg-white border border-gray-200 rounded-lg p-4 flex-1">
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
import { ref, computed, watch, onMounted } from 'vue'
import { FeatherIcon, FormControl, Button, Dialog, call } from 'frappe-ui'
import { useCampaignQRStore } from '@/stores/campaignQR'
import { useToast } from '@/composables/useToast'

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

// Composables
const qrStore = useCampaignQRStore()
const toast = useToast()

// State
const generating = ref(false)
const error = ref(null)
const qrCodesList = ref([])
const showAddQRModal = ref(false)
const editingQR = ref(null)
const savingQR = ref(false)
const newQRData = ref({
  qr_name: '',
  description: '',
  purpose: '',
  utm_source: 'qr_code',
  utm_medium: 'qr'
})

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

// Load QR codes on mount
onMounted(async () => {
  if (props.campaignId) {
    await loadQRCodes()
  }
})

// Load QR codes for campaign
const loadQRCodes = async () => {
  if (!props.campaignId) return
  
  const result = await qrStore.fetchQRCodesByCampaign(props.campaignId)
  if (result.success) {
    qrCodesList.value = result.data || []
  }
}

// Reset modal data
const resetModalData = () => {
  newQRData.value = {
    qr_name: '',
    description: '',
    purpose: '',
    utm_source: 'qr_code',
    utm_medium: 'qr'
  }
  editingQR.value = null
}

// Edit QR Code
const editQRCode = (qr) => {
  editingQR.value = qr
  newQRData.value = {
    qr_name: qr.qr_name,
    description: qr.description || '',
    purpose: qr.purpose || '',
    utm_source: qr.utm_source,
    utm_medium: qr.utm_medium
  }
  showAddQRModal.value = true
}

// Save QR Code (Create or Update)
const saveQRCode = async () => {
  // Validation
  if (!newQRData.value.qr_name || !newQRData.value.utm_source || !newQRData.value.utm_medium) {
    toast.error(__('Please fill in all required fields'))
    return
  }

  if (!props.landingPageUrl) {
    toast.error(__('Please create a landing page first'))
    return
  }

  savingQR.value = true
  
  try {
    let result
    
    if (editingQR.value) {
      // Update existing QR
      result = await qrStore.updateQRCode(editingQR.value.name, {
        qr_name: newQRData.value.qr_name,
        description: newQRData.value.description,
        purpose: newQRData.value.purpose,
        utm_source: newQRData.value.utm_source,
        utm_medium: newQRData.value.utm_medium,
        landing_page_url: props.landingPageUrl
      })
    } else {
      // Create new QR
      result = await qrStore.createQRCode({
        campaign_id: props.campaignId,
        qr_name: newQRData.value.qr_name,
        description: newQRData.value.description,
        purpose: newQRData.value.purpose,
        utm_source: newQRData.value.utm_source,
        utm_medium: newQRData.value.utm_medium,
        utm_campaign: props.campaignId,
        landing_page_url: props.landingPageUrl
      })
    }

    if (result.success) {
      // Generate QR code
      const qrId = editingQR.value ? editingQR.value.name : result.data.name
      const generateResult = await qrStore.generateQRCode(qrId, props.landingPageUrl, {
        utm_campaign: props.campaignId,
        utm_source: newQRData.value.utm_source,
        utm_medium: newQRData.value.utm_medium
      })

      if (generateResult.success) {
        toast.success(editingQR.value ? __('QR Code updated successfully') : __('QR Code created successfully'))
        showAddQRModal.value = false
        resetModalData()
        await loadQRCodes()
      } else {
        toast.error(__('QR Code saved but failed to generate image'))
      }
    } else {
      toast.error(result.error || __('Failed to save QR Code'))
    }
  } catch (err) {
    console.error('Error saving QR code:', err)
    toast.error(__('An error occurred while saving QR Code'))
  } finally {
    savingQR.value = false
  }
}

// Delete QR Code
const deleteQRCode = async (qr) => {
  if (!confirm(__('Are you sure you want to delete this QR code?'))) {
    return
  }

  const result = await qrStore.deleteQRCode(qr.name)
  if (result.success) {
    toast.success(__('QR Code deleted successfully'))
    await loadQRCodes()
  } else {
    toast.error(result.error || __('Failed to delete QR Code'))
  }
}

// Download QR Code
const downloadQRCode = (qr) => {
  if (!qr.qr_image) return
  
  const link = document.createElement('a')
  link.href = qr.qr_image
  link.download = `qr-code-${qr.qr_name.replace(/\s+/g, '-').toLowerCase()}.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// Watch modal close
watch(showAddQRModal, (newVal) => {
  if (!newVal) {
    resetModalData()
  }
})

// Watch landing page URL changes
watch(() => props.landingPageUrl, (newUrl) => {
  if (newUrl && !qrData.value) {
    // Auto-generate QR when landing page is available
    setTimeout(() => {
      generateQR()
    }, 500)
  }
})

// Watch campaign ID changes
watch(() => props.campaignId, (newId) => {
  if (newId) {
    loadQRCodes()
  }
})
</script>

<style scoped>
/* Add any custom styles here */
</style>
