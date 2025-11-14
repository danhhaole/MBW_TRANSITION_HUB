<template>
  <div class="space-y-6 animate-fadeIn">
    <!-- Header -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-base font-semibold text-gray-900 mb-2">
        {{ __('Content & Channels') }}
      </h3>
      <p class="text-sm text-gray-600">
        {{ __('Create content and choose where to post your attraction campaign') }}
      </p>
    </div>

    <!-- Landing Page Selector (Section 2.1) -->
    <LandingPageSelector
      v-model:ladipage-url="localLadipageUrl"
      v-model:ladipage-id="localLadipageId"
      :campaign-id="props.name"
      :campaign-name="campaignName"
      :company-info="companyInfo"
      :job-info="jobInfo"
    />


    <!-- Channel Selection with Add Button -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-4">
        <h4 class="text-sm font-semibold text-gray-900">
          {{ __('Posting Channels') }}
        </h4>
        
        <!-- Add Channel Dropdown (only show if there are available channels) -->
        <Dropdown v-if="availableChannelOptions.length > 0" :options="availableChannelOptions">
          <template v-slot="{ open }">
            <Button variant="solid" size="sm" :theme="'gray'">
              <template #prefix>
                <FeatherIcon name="plus" class="h-4 w-4" />
              </template>
              {{ __('Add Channel') }}
              <template #suffix>
                <FeatherIcon
                  :name="open ? 'chevron-up' : 'chevron-down'"
                  class="h-4 w-4"
                />
              </template>
            </Button>
          </template>
        </Dropdown>
        
        <!-- All channels added message -->
        <div v-else class="text-xs text-gray-500 flex items-center">
          <FeatherIcon name="check-circle" class="h-4 w-4 text-green-600 mr-1" />
          {{ __('All channels added') }}
        </div>
      </div>

      <!-- Selected Channels List (Empty State) -->
      <div v-if="localSelectedChannels.length === 0" class="text-center py-8 border-2 border-dashed border-gray-200 rounded-lg">
        <FeatherIcon name="share-2" class="h-10 w-10 text-gray-400 mx-auto mb-3" />
        <p class="text-sm text-gray-600 mb-1">{{ __('No channels added yet') }}</p>
        <p class="text-xs text-gray-500">{{ __('Click "Add Channel" to start posting') }}</p>
      </div>

      <!-- No channel selected warning -->
      <div v-if="localSelectedChannels.length === 0 && showError" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
        <div class="flex items-start">
          <FeatherIcon name="alert-circle" class="h-4 w-4 text-red-600 mt-0.5 mr-2 flex-shrink-0" />
          <p class="text-sm text-red-800">
            {{ __('Please add at least one channel to continue') }}
          </p>
        </div>
      </div>
    </div>

    <!-- Channel Content Editors (Collapsible) -->
    <div class="space-y-4">
      <!-- Facebook Editor (Collapsible) -->
      <div v-if="isFacebookSelected" class="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 flex items-center justify-between border-b border-gray-200">
          <button
            @click="toggleEditor('facebook')"
            class="flex items-center flex-1 hover:opacity-80 transition-opacity"
          >
            <div class="w-10 h-10 rounded-lg bg-blue-500 text-white flex items-center justify-center mr-3">
              <FeatherIcon name="facebook" class="h-5 w-5" />
            </div>
            <div class="text-left flex-1">
              <h4 class="text-sm font-semibold text-gray-900">
                {{ __('Facebook Post') }}
              </h4>
              <p class="text-xs text-gray-500">
                {{ localFacebookContent.content ? __('Content added') : __('Click to add content') }}
              </p>
            </div>
            <FeatherIcon 
              :name="expandedEditors.facebook ? 'chevron-up' : 'chevron-down'" 
              class="h-5 w-5 text-gray-400 mr-3"
            />
          </button>
          <button
            @click="removeChannel('facebook')"
            class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
            :title="__('Remove channel')"
          >
            <FeatherIcon name="x" class="h-4 w-4" />
          </button>
        </div>
        
        <div v-show="expandedEditors.facebook" class="p-6 space-y-4">
          <!-- Schedule Time for Facebook -->
          <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <div class="flex items-center mb-3">
              <FeatherIcon name="clock" class="h-4 w-4 text-gray-600 mr-2" />
              <label class="text-sm font-medium text-gray-700">
                {{ __('Post Schedule Time') }}
              </label>
            </div>
            <FormControl
              type="datetime-local"
              :model-value="localFacebookContent.schedule_time"
              :placeholder="__('Leave empty to post immediately')"
              @update:model-value="updateFacebookContent('schedule_time', $event)"
            />
            <p class="text-xs text-gray-500 mt-1">
              {{ localFacebookContent.schedule_time ? __('Will post at scheduled time') : __('Will post immediately when campaign starts') }}
            </p>
          </div>

          <!-- Content Editor -->
          <FacebookContentEditor
            :content="localFacebookContent.content"
            :image="localFacebookContent.image"
            :page-id="localFacebookContent.page_id"
            :page-options="facebookPages"
            :show-page-selector="true"
            :show-link-input="false"
            :placeholder="__('Write your job post content here...')"
            @update:content="updateFacebookContent('content', $event)"
            @update:image="updateFacebookContent('image', $event)"
            @update:page-id="updateFacebookContent('page_id', $event)"
          />

          <!-- Test Share Job Posting Button -->
          <div class="mt-4 pt-4 border-t border-gray-200">
            <Button
              @click="testShareJobPosting"
              :loading="testingShare"
              variant="outline"
              size="sm"
              class="w-full"
            >
              <template #prefix>
                <FeatherIcon name="send" class="h-4 w-4" />
              </template>
              {{ __('Test Share Job to Facebook') }}
            </Button>
            <p class="text-xs text-gray-500 mt-2 text-center">
              {{ __('This will post the current content to your selected Facebook page') }}
            </p>
          </div>
        </div>
      </div>

      <!-- Zalo Editor (Collapsible) -->
      <div v-if="isZaloSelected" class="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 flex items-center justify-between border-b border-gray-200">
          <button
            @click="toggleEditor('zalo')"
            class="flex items-center flex-1 hover:opacity-80 transition-opacity"
          >
            <div class="w-10 h-10 rounded-lg bg-green-500 text-white flex items-center justify-center mr-3">
              <FeatherIcon name="message-circle" class="h-5 w-5" />
            </div>
            <div class="text-left flex-1">
              <h4 class="text-sm font-semibold text-gray-900">
                {{ __('Zalo Post') }}
              </h4>
              <p class="text-xs text-gray-500">
                {{ localZaloContent.content ? __('Content added') : __('Click to add content') }}
              </p>
            </div>
            <FeatherIcon 
              :name="expandedEditors.zalo ? 'chevron-up' : 'chevron-down'" 
              class="h-5 w-5 text-gray-400 mr-3"
            />
          </button>
          <button
            @click="removeChannel('zalo')"
            class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
            :title="__('Remove channel')"
          >
            <FeatherIcon name="x" class="h-4 w-4" />
          </button>
        </div>
        
        <div v-show="expandedEditors.zalo" class="p-6 space-y-4">
          <!-- Schedule Time for Zalo -->
          <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <div class="flex items-center mb-3">
              <FeatherIcon name="clock" class="h-4 w-4 text-gray-600 mr-2" />
              <label class="text-sm font-medium text-gray-700">
                {{ __('Post Schedule Time') }}
              </label>
            </div>
            <FormControl
              type="datetime-local"
              :model-value="localZaloContent.schedule_time"
              :placeholder="__('Leave empty to post immediately')"
              @update:model-value="updateZaloScheduleTime($event)"
            />
            <p class="text-xs text-gray-500 mt-1">
              {{ localZaloContent.schedule_time ? __('Will post at scheduled time') : __('Will post immediately when campaign starts') }}
            </p>
          </div>

          <!-- Content Editor -->
          <ZaloContentEditor
            :content="localZaloContent"
            @update:content="updateZaloContent($event)"
          />
        </div>
      </div>
      
      <!-- QR Code Editor (Collapsible) -->
      <div v-if="isQrSelected" class="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 flex items-center justify-between border-b border-gray-200">
          <button
            @click="toggleEditor('qr_code')"
            class="flex items-center flex-1 hover:opacity-80 transition-opacity"
          >
            <div class="w-10 h-10 rounded-lg bg-gray-500 text-white flex items-center justify-center mr-3">
              <FeatherIcon name="qr-code" class="h-5 w-5" />
            </div>
            <div class="text-left flex-1">
              <h4 class="text-sm font-semibold text-gray-900">
                {{ __('QR Code') }}
              </h4>
              <p class="text-xs text-gray-500">
                {{ localQrContent.qr_data ? __('QR Code generated') : __('Click to generate QR code') }}
              </p>
            </div>
            <FeatherIcon 
              :name="expandedEditors.qr_code ? 'chevron-up' : 'chevron-down'" 
              class="h-5 w-5 text-gray-400 mr-3"
            />
          </button>
          <button
            @click="removeChannel('qr_code')"
            class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
            :title="__('Remove channel')"
          >
            <FeatherIcon name="x" class="h-4 w-4" />
          </button>
        </div>
        
        <div v-show="expandedEditors.qr_code" class="p-6 space-y-4">
          <!-- Content Editor -->
          <QRCodeContentEditor
            :content="localQrContent"
            :landing-page-url="localPageData?.builder_page || localLadipageUrl"
            :campaign-id="props.name"
            @update:content="updateQrContent($event)"
          />
        </div>
      </div>
    </div>

    <!-- Channel Content Customizer -->
    <ChannelContentCustomizer
      :channels="localSelectedChannels"
      :campaign-name="campaignName"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { FeatherIcon, Button, Dropdown, FormControl, call } from 'frappe-ui'
import FacebookContentEditor from '../molecules/FacebookContentEditor.vue'
import ZaloContentEditor from '../molecules/ZaloContentEditor.vue'
import QRCodeContentEditor from '../molecules/QRCodeContentEditor.vue'
import LandingPageSelector from '../molecules/LandingPageSelector.vue'
import ChannelContentCustomizer from '../molecules/ChannelContentCustomizer.vue'
import { getAvailableChannels } from '@/data/mockChannels'
import { useToast } from '@/composables/useToast'

const toast = useToast()

const props = defineProps({
  selectedChannels: {
    type: Array,
    default: () => []
  },
  name: {
    type: String,
    default: ''
  },
  facebookContent: {
    type: Object,
    default: () => ({
      content: '',
      image: null,
      page_id: null
    })
  },
  zaloContent: {
    type: Object,
    default: () => ({
      content: '',
      image: null
    })
  },
  qrContent: {
    type: Object,
    default: () => ({
      utm_campaign: '',
      utm_source: 'qr_code',
      utm_medium: 'qr',
      qr_data: null
    })
  },
  landingPage: {
    type: String,
    default: ''
  },
  pageData: {
    type: Object,
    default: null
  },
  ladipageUrl: {
    type: String,
    default: ''
  },
  ladipageId: {
    type: String,
    default: ''
  },
  campaignId: {
    type: String,
    default: ''
  },
  campaignName: {
    type: String,
    default: ''
  },
  companyInfo: {
    type: Object,
    default: () => ({})
  },
  jobInfo: {
    type: Object,
    default: () => ({})
  },
  showError: {
    type: Boolean,
    default: false
  }
})

console.log('✅ Props:', props)

const emit = defineEmits([
  'update:selectedChannels',
  'update:facebookContent',
  'update:zaloContent',
  'update:qrContent',
  'update:landingPage',
  'update:pageData',
  'update:ladipageUrl',
  'update:ladipageId'
])

// Local state
const localSelectedChannels = computed({
  get: () => props.selectedChannels,
  set: (value) => emit('update:selectedChannels', value)
})

const localFacebookContent = computed({
  get: () => props.facebookContent,
  set: (value) => emit('update:facebookContent', value)
})

const localZaloContent = computed({
  get: () => props.zaloContent,
  set: (value) => emit('update:zaloContent', value)
})

const localQrContent = computed({
  get: () => props.qrContent,
  set: (value) => emit('update:qrContent', value)
})

const localLandingPage = computed({
  get: () => props.landingPage,
  set: (value) => emit('update:landingPage', value)
})

const localPageData = computed({
  get: () => props.pageData,
  set: (value) => emit('update:pageData', value)
})

const localLadipageUrl = computed({
  get: () => props.ladipageUrl,
  set: (value) => emit('update:ladipageUrl', value)
})

const localLadipageId = computed({
  get: () => props.ladipageId,
  set: (value) => emit('update:ladipageId', value)
})

// Computed
const isFacebookSelected = computed(() => localSelectedChannels.value.includes('facebook'))
const isZaloSelected = computed(() => localSelectedChannels.value.includes('zalo'))
const isQrSelected = computed(() => localSelectedChannels.value.includes('qr_code'))

// Expanded editors state
const expandedEditors = ref({
  facebook: false,
  zalo: false,
  qr_code: false
})

// Available channels for dropdown (from mock data)
const availableChannels = getAvailableChannels()

// Facebook pages from Mira External Connection
const facebookPages = ref([])
const loadingPages = ref(false)
const testingShare = ref(false)

// Load Facebook pages
const loadFacebookPages = async () => {
  try {
    loadingPages.value = true
    const result = await call('mbw_mira.api.external_connection.get_facebook_pages')
    
    if (result.success && result.data) {
      facebookPages.value = result.data.map(page => ({
        label: page.page_name,
        value: page.page_id,
        connection_id: page.connection_name // Use connection_name as connection_id
      }))
      console.log('✅ Loaded Facebook pages:', facebookPages.value)
    }
  } catch (error) {
    console.error('❌ Error loading Facebook pages:', error)
  } finally {
    loadingPages.value = false
  }
}

// Dropdown options - only show channels that are not already selected
const availableChannelOptions = computed(() => {
  return availableChannels
    .filter(channel => !localSelectedChannels.value.includes(channel.id))
    .map(channel => ({
      label: channel.label,
      icon: channel.icon,
      onClick: () => addChannel(channel.id)
    }))
})

// Load pages on mount
onMounted(() => {
  loadFacebookPages()
})

// Methods
const addChannel = (channelId) => {
  if (!localSelectedChannels.value.includes(channelId)) {
    localSelectedChannels.value = [...localSelectedChannels.value, channelId]
    // Auto-expand editor when added
    expandedEditors.value[channelId] = true
  }
}

const removeChannel = (channelId) => {
  localSelectedChannels.value = localSelectedChannels.value.filter(id => id !== channelId)
  // Collapse editor when removed
  expandedEditors.value[channelId] = false
}

const toggleEditor = (channel) => {
  expandedEditors.value[channel] = !expandedEditors.value[channel]
}

const updateFacebookContent = (field, value) => {
  localFacebookContent.value = {
    ...localFacebookContent.value,
    [field]: value
  }
}

const updateZaloContent = (value) => {
  localZaloContent.value = {
    ...localZaloContent.value,
    ...value
  }
}

const updateZaloScheduleTime = (value) => {
  localZaloContent.value = {
    ...localZaloContent.value,
    schedule_time: value
  }
}

const updateQrContent = (value) => {
  localQrContent.value = {
    ...localQrContent.value,
    ...value
  }
}

// Test share job posting to Facebook
const testShareJobPosting = async () => {
  if (!localFacebookContent.value.page_id) {
    toast.error(__('Please select a Facebook page first'))
    return
  }

  if (!localFacebookContent.value.content) {
    toast.error(__('Please add content to your Facebook post'))
    return
  }

  testingShare.value = true
  
  
  try {
    // Find the connection ID for the selected Facebook page
    const selectedPage = facebookPages.value.find(page => page.value === localFacebookContent.value.page_id)
    console.log('Selected Facebook page:', selectedPage)
    if (!selectedPage) {
      throw new Error('Selected Facebook page not found')
    }

    if (!selectedPage.connection_id) {
      throw new Error('Facebook page connection ID not found. Please reconnect your Facebook account.')
    }

    const result = await call('mbw_mira.api.external_connections.share_job_posting', {
      connection_id: selectedPage.connection_id,
      job_id: props.campaignId || 'test_job_id',
      message: localFacebookContent.value.content,
      schedule_type: 'now',
      image_url: localFacebookContent.value.image || '',
      campaign_id: props.campaignId,
      ladipage_url: props.ladipageUrl,
    })

    if (result.status === 'success') {
      toast.success(__('Job posted to Facebook successfully!'))
      console.log('✅ Facebook post result:', result)
    } else {
      throw new Error(result.message || 'Failed to post to Facebook')
    }
  } catch (error) {
    console.error('❌ Error sharing job to Facebook:', error)
    toast.error(error.message || __('Failed to share job to Facebook'))
  } finally {
    testingShare.value = false
  }
}

const updateLandingPage = (value) => {
  localLandingPage.value = value
}
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
