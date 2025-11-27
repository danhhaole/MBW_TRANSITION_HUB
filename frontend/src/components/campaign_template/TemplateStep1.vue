<template>
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <!-- Left Column: Main Content (2/3) -->
    <div class="lg:col-span-2 space-y-6">
      <!-- Template Basic Info -->
      <div class="bg-white rounded-lg border border-gray-200 p-6">
        <div class="flex items-center mb-4">
          <div class="w-8 h-8 rounded-lg bg-blue-500 text-white flex items-center justify-center mr-3">
            <FeatherIcon name="file-text" class="h-4 w-4" />
          </div>
          <div>
            <h4 class="text-sm font-semibold text-gray-900">
              {{ __('Template Information') }}
            </h4>
            <p class="text-xs text-gray-500">
              {{ __('Basic information about your campaign template') }}
            </p>
          </div>
        </div>

        <div class="grid grid-cols-1 gap-6">
          <!-- Template Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Template Name') }}
              <span class="text-red-500">*</span>
            </label>
            <FormControl
              type="text"
              :value="templateName"
              @change="$emit('update:templateName', $event.target.value)"
              :placeholder="__('Enter template name')"
              :class="showError && !templateName ? 'border-red-300' : ''"
            />
            <p v-if="showError && !templateName" class="mt-1 text-sm text-red-600">
              {{ __('Template name is required') }}
            </p>
          </div>

          <!-- Template Description -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Template Description') }}
              <span class="text-red-500">*</span>
            </label>
            <FormControl
              type="textarea"
              :value="templateDescription"
              @change="$emit('update:templateDescription', $event.target.value)"
              :placeholder="__('Describe what this template is for, e.g., Vue Developer Recruitment Campaign...')"
              rows="3"
              :class="showError && !templateDescription ? 'border-red-300' : ''"
            />
            <p v-if="showError && !templateDescription" class="mt-1 text-sm text-red-600">
              {{ __('Template description is required') }}
            </p>
          </div>
        </div>
      </div>

      <!-- Campaign Basic Info (reuse existing component) -->
      <CampaignBasicInfo
        :campaign-name="campaignName"
        :description="description"
        :show-error="showError"
        @update:campaign-name="$emit('update:campaignName', $event)"
        @update:description="$emit('update:description', $event)"
      />

      <!-- Campaign Type Specific Fields -->
      <div v-if="campaignType === 'ATTRACTION'">
        <!-- Target Pool Selection -->
        <div class="bg-white rounded-lg border border-gray-200 p-6">
          <div class="mb-4">
            <h3 class="text-base font-semibold text-gray-900">
              {{ __('Target Pool') }}
            </h3>
            <p class="text-sm text-gray-600 mt-1">
              {{ __('Select a segment to save this campaign to (optional)') }}
            </p>
          </div>

          <Link
            :doctype="'Mira Segment'"
            :model-value="targetPool"
            :label="__('Segment')"
            :placeholder="__('Select or search segment...')"
            size="md"
            :searchfield="'title'"
            @update:model-value="$emit('update:targetPool', $event)"
          />

          <div v-if="!targetPool" class="mt-3 bg-blue-50 rounded-lg p-3 border border-blue-200">
            <div class="flex items-start">
              <FeatherIcon name="info" class="h-4 w-4 text-blue-600 mt-0.5 mr-2 flex-shrink-0" />
              <p class="text-xs text-blue-800">
                {{ __('If no segment is selected, the campaign will not be associated with any specific talent pool.') }}
              </p>
            </div>
          </div>

          <div v-else class="mt-3 bg-green-50 rounded-lg p-3 border border-green-200">
            <div class="flex items-start">
              <FeatherIcon name="check-circle" class="h-4 w-4 text-green-600 mt-0.5 mr-2 flex-shrink-0" />
              <p class="text-xs text-green-800">
                {{ __('Campaign will be saved to segment: ') }}<strong>{{ targetPool }}</strong>
              </p>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="campaignType === 'NURTURING' || campaignType === 'RECRUITMENT'">
        <!-- Target Segment Selector -->
        <TargetSegmentSelector
          :config-data="configData"
          :conditions="conditions"
          :candidate-count="candidateCount"
          :campaign-type="campaignType"
          @update:config-data="$emit('update:configData', $event)"
          @update:conditions="$emit('update:conditions', $event)"
          @update:candidate-count="$emit('update:candidateCount', $event)"
        />
      </div>

      <!-- Campaign Tags -->
      <CampaignTagPicker
        :campaign-id="templateId"
        :model-value="campaignTags"
        doctype="Mira Campaign Template"
        @update:model-value="$emit('update:campaignTags', $event)"
      />
    </div>

    <!-- Right Column: Template Settings (1/3) -->
    <div class="lg:col-span-1 space-y-6">
      <!-- Thumbnail Upload -->
      <div class="bg-white rounded-lg border border-gray-200 p-6">
        <div class="flex items-center mb-4">
          <div class="w-8 h-8 rounded-lg bg-pink-500 text-white flex items-center justify-center mr-3">
            <FeatherIcon name="image" class="h-4 w-4" />
          </div>
          <div>
            <h4 class="text-sm font-semibold text-gray-900">
              {{ __('Template Thumbnail') }}
            </h4>
            <p class="text-xs text-gray-500">
              {{ __('Upload a preview image') }}
            </p>
          </div>
        </div>

        <!-- Thumbnail Preview -->
        <div class="mb-4">
          <div 
            v-if="thumbnail"
            class="relative w-full aspect-video rounded-lg overflow-hidden border border-gray-200"
          >
            <img 
              :src="thumbnail" 
              alt="Template thumbnail"
              class="w-full h-full object-cover"
            />
            <button
              @click="$emit('update:thumbnail', '')"
              class="absolute top-2 right-2 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600 transition-colors"
              :title="__('Remove thumbnail')"
            >
              <FeatherIcon name="x" class="h-3 w-3" />
            </button>
          </div>
          <div 
            v-else
            class="w-full aspect-video rounded-lg border-2 border-dashed border-gray-300 flex flex-col items-center justify-center bg-gray-50 hover:bg-gray-100 transition-colors cursor-pointer"
            @click="triggerFileUpload"
          >
            <FeatherIcon name="upload-cloud" class="h-8 w-8 text-gray-400 mb-2" />
            <p class="text-sm text-gray-500">{{ __('Click to upload') }}</p>
            <p class="text-xs text-gray-400 mt-1">{{ __('PNG, JPG up to 2MB') }}</p>
          </div>
        </div>

        <!-- Hidden File Input -->
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          class="hidden"
          @change="handleFileUpload"
        />

        <!-- Upload Button -->
        <Button
          v-if="!thumbnail"
          variant="outline"
          class="w-full"
          @click="triggerFileUpload"
        >
          <template #prefix>
            <FeatherIcon name="upload" class="h-4 w-4" />
          </template>
          {{ __('Upload Image') }}
        </Button>
      </div>

      <!-- Template Settings -->
      <div class="bg-white rounded-lg border border-gray-200 p-6">
        <div class="flex items-center mb-4">
          <div class="w-8 h-8 rounded-lg bg-purple-500 text-white flex items-center justify-center mr-3">
            <FeatherIcon name="settings" class="h-4 w-4" />
          </div>
          <div>
            <h4 class="text-sm font-semibold text-gray-900">
              {{ __('Template Settings') }}
            </h4>
            <p class="text-xs text-gray-500">
              {{ __('Visibility and properties') }}
            </p>
          </div>
        </div>

        <div class="space-y-4">
          <!-- Template Properties -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-3">
              {{ __('Template Properties') }}
            </label>
            
            <!-- Is Premium -->
            <div class="flex items-start mb-3">
              <input
                type="checkbox"
                :checked="isPremium"
                @change="$emit('update:isPremium', $event.target.checked)"
                class="h-4 w-4 text-yellow-600 border-gray-300 rounded focus:ring-yellow-500 mt-0.5"
              />
              <div class="ml-2">
                <label class="text-sm text-gray-700">{{ __('Premium Template') }}</label>
                <p class="text-xs text-gray-500">{{ __('Requires premium access to use') }}</p>
              </div>
            </div>

            <!-- Is Suggestion -->
            <div class="flex items-start">
              <input
                type="checkbox"
                :checked="isSuggestion"
                @change="$emit('update:isSuggestion', $event.target.checked)"
                class="h-4 w-4 text-green-600 border-gray-300 rounded focus:ring-green-500 mt-0.5"
              />
              <div class="ml-2">
                <label class="text-sm text-gray-700">{{ __('Suggested Template') }}</label>
                <p class="text-xs text-gray-500">{{ __('Show as suggested to users') }}</p>
              </div>
            </div>
          </div>

          <!-- Info Box -->
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 mt-4">
            <div class="flex items-start">
              <FeatherIcon name="info" class="h-4 w-4 text-blue-600 mt-0.5 mr-2 flex-shrink-0" />
              <p class="text-xs text-blue-800">
                {{ __('This template will be publicly available to all users.') }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { FormControl, Select, FeatherIcon, Button, call } from 'frappe-ui'
import CampaignBasicInfo from '../campaign_new/molecules/CampaignBasicInfo.vue'
import TargetSegmentSelector from '../campaign_new/molecules/TargetSegmentSelector.vue'
import CampaignTagPicker from '../campaign_new/molecules/CampaignTagPicker.vue'
import Link from '@/components/Controls/Link.vue'

const props = defineProps({
  templateName: {
    type: String,
    default: ''
  },
  templateDescription: {
    type: String,
    default: ''
  },
  campaignType: {
    type: String,
    default: 'ATTRACTION'
  },
  campaignName: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  targetPool: {
    type: String,
    default: ''
  },
  configData: {
    type: Object,
    default: () => ({})
  },
  conditions: {
    type: Array,
    default: () => []
  },
  candidateCount: {
    type: Number,
    default: 0
  },
  campaignTags: {
    type: Array,
    default: () => []
  },
  templateId: {
    type: String,
    default: ''
  },
  scopeType: {
    type: String,
    default: 'PUBLIC'
  },
  isDefault: {
    type: Boolean,
    default: false
  },
  isPremium: {
    type: Boolean,
    default: false
  },
  isSuggestion: {
    type: Boolean,
    default: false
  },
  thumbnail: {
    type: String,
    default: ''
  },
  showError: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'update:templateName',
  'update:templateDescription',
  'update:campaignType', 
  'update:campaignName',
  'update:description',
  'update:targetPool',
  'update:configData',
  'update:conditions',
  'update:candidateCount',
  'update:campaignTags',
  'update:scopeType',
  'update:isDefault',
  'update:isPremium',
  'update:isSuggestion',
  'update:thumbnail'
])

// File upload refs
const fileInput = ref(null)
const uploading = ref(false)

// Trigger file input click
const triggerFileUpload = () => {
  fileInput.value?.click()
}

// Handle file upload
const handleFileUpload = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  // Validate file type
  if (!file.type.startsWith('image/')) {
    alert('Please select an image file')
    return
  }

  // Validate file size (2MB max)
  if (file.size > 2 * 1024 * 1024) {
    alert('File size must be less than 2MB')
    return
  }

  uploading.value = true
  
  try {
    // Create FormData for upload - don't attach to doctype when creating new
    const formData = new FormData()
    formData.append('file', file)
    formData.append('is_private', '0')
    formData.append('folder', 'Home/Attachments')
    // Don't set doctype/docname - upload as unattached file
    
    // Upload using Frappe's upload API
    const response = await fetch('/api/method/upload_file', {
      method: 'POST',
      body: formData,
      headers: {
        'X-Frappe-CSRF-Token': window.csrf_token || ''
      }
    })
    
    const result = await response.json()
    
    if (result.message?.file_url) {
      emit('update:thumbnail', result.message.file_url)
    } else {
      console.error('Upload failed:', result)
      alert('Failed to upload image')
    }
  } catch (error) {
    console.error('Upload error:', error)
    alert('Failed to upload image')
  } finally {
    uploading.value = false
    // Reset file input
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  }
}

const campaignTypeOptions = [
  { label: __('Attraction'), value: 'ATTRACTION' },
  { label: __('Nurturing'), value: 'NURTURING' },
  { label: __('Recruitment'), value: 'RECRUITMENT' }
]

const scopeTypeOptions = [
  { label: __('Public'), value: 'PUBLIC' },
  { label: __('Private'), value: 'PRIVATE' },
  { label: __('Organization'), value: 'ORGANIZATION' }
]
</script>
