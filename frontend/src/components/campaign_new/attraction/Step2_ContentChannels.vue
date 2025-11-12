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
      :landing-page="localLandingPage"
      @update:landing-page="updateLandingPage"
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
import LandingPageSelector from '../molecules/LandingPageSelector.vue'
import ChannelContentCustomizer from '../molecules/ChannelContentCustomizer.vue'
import { getAvailableChannels } from '@/data/mockChannels'

const props = defineProps({
  selectedChannels: {
    type: Array,
    default: () => []
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
  landingPage: {
    type: String,
    default: ''
  },
  campaignName: {
    type: String,
    default: ''
  },
  showError: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'update:selectedChannels',
  'update:facebookContent',
  'update:zaloContent',
  'update:landingPage'
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

const localLandingPage = computed({
  get: () => props.landingPage,
  set: (value) => emit('update:landingPage', value)
})

// Computed
const isFacebookSelected = computed(() => localSelectedChannels.value.includes('facebook'))
const isZaloSelected = computed(() => localSelectedChannels.value.includes('zalo'))

// Expanded editors state
const expandedEditors = ref({
  facebook: false,
  zalo: false
})

// Available channels for dropdown (from mock data)
const availableChannels = getAvailableChannels()

// Facebook pages from Mira External Connection
const facebookPages = ref([])
const loadingPages = ref(false)

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
