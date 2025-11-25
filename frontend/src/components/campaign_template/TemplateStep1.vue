<template>
  <div class="space-y-6">
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
      :campaign-tags="campaignTags"
      @update:campaign-tags="$emit('update:campaignTags', $event)"
    />

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
            {{ __('Configure template visibility and properties') }}
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Scope Type -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __('Template Scope') }}
          </label>
          <Select
            :model-value="scopeType"
            @update:model-value="$emit('update:scopeType', $event)"
            :options="scopeTypeOptions"
            :placeholder="__('Select scope type')"
          />
          <p class="text-xs text-gray-500 mt-1">
            {{ __('Who can see and use this template') }}
          </p>
        </div>

        <!-- Template Properties -->
        <div class="space-y-3">
          <label class="block text-sm font-medium text-gray-700">
            {{ __('Template Properties') }}
          </label>
          
          <!-- Is Default -->
          <div class="flex items-center">
            <input
              type="checkbox"
              :checked="isDefault"
              @change="$emit('update:isDefault', $event.target.checked)"
              class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <label class="ml-2 text-sm text-gray-700">
              {{ __('Default Template') }}
            </label>
          </div>
          <p class="text-xs text-gray-500 ml-6 -mt-2">
            {{ __('Use as default template for this campaign type') }}
          </p>

          <!-- Is Premium -->
          <div class="flex items-center">
            <input
              type="checkbox"
              :checked="isPremium"
              @change="$emit('update:isPremium', $event.target.checked)"
              class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <label class="ml-2 text-sm text-gray-700">
              {{ __('Premium Template') }}
            </label>
          </div>
          <p class="text-xs text-gray-500 ml-6 -mt-2">
            {{ __('Requires premium access to use') }}
          </p>

          <!-- Is Suggestion -->
          <div class="flex items-center">
            <input
              type="checkbox"
              :checked="isSuggestion"
              @change="$emit('update:isSuggestion', $event.target.checked)"
              class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <label class="ml-2 text-sm text-gray-700">
              {{ __('Suggested Template') }}
            </label>
          </div>
          <p class="text-xs text-gray-500 ml-6 -mt-2">
            {{ __('Show as suggested template to users') }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { FormControl, Select, FeatherIcon } from 'frappe-ui'
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
  showError: {
    type: Boolean,
    default: false
  }
})

defineEmits([
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
  'update:isSuggestion'
])

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
