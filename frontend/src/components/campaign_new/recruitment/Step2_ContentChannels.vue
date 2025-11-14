<!-- Recruitment Content & Channels - Similar to Attraction but with Email -->
<template>
  <div class="space-y-6 animate-fadeIn">
    <!-- Header -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-base font-semibold text-gray-900 mb-2">
        {{ __('Content & Channels') }}
      </h3>
      <p class="text-sm text-gray-600">
        {{ __('Create content for recruitment campaign across multiple channels') }}
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
      <!-- Email Editor (Collapsible) -->
      <div v-if="isEmailSelected" class="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 flex items-center justify-between border-b border-gray-200">
          <button
            @click="toggleEditor('email')"
            class="flex items-center flex-1 hover:opacity-80 transition-opacity"
          >
            <div class="w-10 h-10 rounded-lg bg-red-500 text-white flex items-center justify-center mr-3">
              <FeatherIcon name="mail" class="h-5 w-5" />
            </div>
            <div class="text-left flex-1">
              <h4 class="text-sm font-semibold text-gray-900">
                {{ __('Email Campaign') }}
              </h4>
              <p class="text-xs text-gray-500">
                {{ localEmailContent.subject ? __('Content added') : __('Click to add content') }}
              </p>
            </div>
            <FeatherIcon 
              :name="expandedEditors.email ? 'chevron-up' : 'chevron-down'" 
              class="h-5 w-5 text-gray-400 mr-3"
            />
          </button>
          <button
            @click="removeChannel('email')"
            class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
            :title="__('Remove channel')"
          >
            <FeatherIcon name="x" class="h-4 w-4" />
          </button>
        </div>
        <div v-if="expandedEditors.email" class="p-6 space-y-4">
          <!-- Schedule Time for Email -->
          <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <div class="flex items-center mb-3">
              <FeatherIcon name="clock" class="h-4 w-4 text-gray-600 mr-2" />
              <label class="text-sm font-medium text-gray-700">
                {{ __('Email Send Time') }}
              </label>
            </div>
            <FormControl
              type="datetime-local"
              :model-value="localEmailContent.schedule_time"
              :placeholder="__('Leave empty to send immediately')"
              @update:model-value="updateEmailScheduleTime($event)"
            />
            <p class="text-xs text-gray-500 mt-1">
              {{ localEmailContent.schedule_time ? __('Will send at scheduled time') : __('Will send immediately when campaign starts') }}
            </p>
          </div>

          <!-- Content Editor -->
          <EmailContentEditor
            :content="localEmailContent"
            @update:content="updateEmailContent"
          />
        </div>
      </div>

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
        <div v-if="expandedEditors.facebook" class="p-6 space-y-4">
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
            :campaign-name="campaignName"
            :image="localFacebookContent.image"
            :page-id="localFacebookContent.page_id"
            :page-options="facebookPages"
            :show-page-selector="true"
            :show-link-input="false"
            @update:content="updateFacebookContent('content', $event)"
            @update:image="updateFacebookContent('image', $event)"
            @update:page-id="updateFacebookContent('page_id', $event)"
          />
        </div>
      </div>

      <!-- Zalo Editor (Collapsible) -->
      <div v-if="isZaloSelected" class="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 flex items-center justify-between border-b border-gray-200">
          <button
            @click="toggleEditor('zalo')"
            class="flex items-center flex-1 hover:opacity-80 transition-opacity"
          >
            <div class="w-10 h-10 rounded-lg bg-blue-600 text-white flex items-center justify-center mr-3">
              <FeatherIcon name="message-square" class="h-5 w-5" />
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
        <div v-if="expandedEditors.zalo" class="p-6 space-y-4">
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
            :campaign-name="campaignName"
            :oa-options="zaloAccounts"
            :show-oa-selector="true"
            @update:content="updateZaloContent"
            @update:oa-id="updateZaloOaId"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { FeatherIcon, Button, Dropdown, FormControl, call } from 'frappe-ui'
import EmailContentEditor from '../molecules/EmailContentEditor.vue'
import FacebookContentEditor from '../molecules/FacebookContentEditor.vue'
import ZaloContentEditor from '../molecules/ZaloContentEditor.vue'
import LandingPageSelector from '../molecules/LandingPageSelector.vue'

const props = defineProps({
  selectedChannels: {
    type: Array,
    default: () => []
  },
  emailContent: {
    type: Object,
    default: () => ({ subject: '', body: '' })
  },
  facebookContent: {
    type: Object,
    default: () => ({ content: '', image: null, page_id: null })
  },
  zaloContent: {
    type: Object,
    default: () => ({ content: '', image: null })
  },
  campaignName: {
    type: String,
    default: ''
  },
  name: {
    type: String,
    default: ''
  },
  ladipageUrl: {
    type: String,
    default: ''
  },
  ladipageId: {
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

const emit = defineEmits([
  'update:selectedChannels',
  'update:emailContent',
  'update:facebookContent',
  'update:zaloContent',
  'update:ladipageUrl',
  'update:ladipageId'
])

// Local computed properties for two-way binding
const localSelectedChannels = computed({
  get: () => props.selectedChannels,
  set: (value) => emit('update:selectedChannels', value)
})

const localEmailContent = computed({
  get: () => props.emailContent,
  set: (value) => emit('update:emailContent', value)
})

const localFacebookContent = computed({
  get: () => props.facebookContent,
  set: (value) => emit('update:facebookContent', value)
})

const localZaloContent = computed({
  get: () => props.zaloContent,
  set: (value) => emit('update:zaloContent', value)
})

const localLadipageUrl = computed({
  get: () => props.ladipageUrl,
  set: (value) => emit('update:ladipageUrl', value)
})

const localLadipageId = computed({
  get: () => props.ladipageId,
  set: (value) => emit('update:ladipageId', value)
})

// Editor expansion state
const expandedEditors = ref({
  email: true,
  facebook: true,
  zalo: true
})

// Facebook pages from Mira External Connection
const facebookPages = ref([])
const loadingPages = ref(false)

// Zalo OA accounts from Mira External Connection
const zaloAccounts = ref([])
const loadingZaloAccounts = ref(false)

// Channel options - Include Email for recruitment
const allChannelOptions = [
  {
    label: __('Email'),
    value: 'email',
    icon: 'mail',
    onClick: () => addChannel('email')
  },
  {
    label: __('Facebook'),
    value: 'facebook',
    icon: 'facebook',
    onClick: () => addChannel('facebook')
  },
  {
    label: __('Zalo'),
    value: 'zalo',
    icon: 'message-square',
    onClick: () => addChannel('zalo')
  }
]

// Available channel options (not yet selected)
const availableChannelOptions = computed(() => {
  return allChannelOptions.filter(option => 
    !localSelectedChannels.value.includes(option.value)
  )
})

// Channel selection helpers
const isEmailSelected = computed(() => localSelectedChannels.value.includes('email'))
const isFacebookSelected = computed(() => localSelectedChannels.value.includes('facebook'))
const isZaloSelected = computed(() => localSelectedChannels.value.includes('zalo'))

// Channel management
const addChannel = (channelType) => {
  if (!localSelectedChannels.value.includes(channelType)) {
    localSelectedChannels.value = [...localSelectedChannels.value, channelType]
    // Auto-expand the editor when adding
    expandedEditors.value[channelType] = true
  }
}

const removeChannel = (channelType) => {
  localSelectedChannels.value = localSelectedChannels.value.filter(ch => ch !== channelType)
  expandedEditors.value[channelType] = false
}

const toggleEditor = (channelType) => {
  expandedEditors.value[channelType] = !expandedEditors.value[channelType]
}

// Content update handlers
const updateEmailContent = (content) => {
  localEmailContent.value = content
}

const updateEmailScheduleTime = (scheduleTime) => {
  localEmailContent.value = {
    ...localEmailContent.value,
    schedule_time: scheduleTime
  }
}

const updateFacebookContent = (field, value) => {
  localFacebookContent.value = {
    ...localFacebookContent.value,
    [field]: value
  }
}

const updateZaloContent = (content) => {
  localZaloContent.value = content
}

const updateZaloOaId = (oaId) => {
  localZaloContent.value = {
    ...localZaloContent.value,
    oa_id: oaId
  }
}

const updateZaloScheduleTime = (scheduleTime) => {
  localZaloContent.value = {
    ...localZaloContent.value,
    schedule_time: scheduleTime
  }
}

// Load Facebook pages
const loadFacebookPages = async () => {
  try {
    loadingPages.value = true
    const result = await call('mbw_mira.api.external_connection.get_facebook_pages')
    
    if (result.success && result.data) {
      facebookPages.value = result.data.map(page => ({
        label: page.page_name,
        value: page.page_id
      }))
      console.log('✅ Loaded Facebook pages:', facebookPages.value)
    }
  } catch (error) {
    console.error('❌ Error loading Facebook pages:', error)
  } finally {
    loadingPages.value = false
  }
}

// Load Zalo OA accounts
const loadZaloAccounts = async () => {
  try {
    loadingZaloAccounts.value = true
    const result = await call('mbw_mira.api.external_connection.get_zalo_accounts')
    
    if (result.success && result.data) {
      zaloAccounts.value = result.data.map(account => ({
        label: account.oa_name,
        value: account.oa_id,
        oa_id: account.oa_id
      }))
      console.log('✅ Loaded Zalo OA accounts:', zaloAccounts.value)
    }
  } catch (error) {
    console.error('❌ Error loading Zalo accounts:', error)
  } finally {
    loadingZaloAccounts.value = false
  }
}

// Load pages and accounts on mount
onMounted(() => {
  loadFacebookPages()
  loadZaloAccounts()
})

</script>

<style scoped>
/* Add any custom styles here */
</style>
