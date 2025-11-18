<template>
  <div class="space-y-6 animate-fadeIn">
    <!-- Campaign Basic Information -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-base font-semibold text-gray-900 mb-4">
        {{ __('Recruitment Campaign Information') }}
      </h3>
      <CampaignBasicInfo
        :campaign-name="campaignName"
        :objective="objective"
        :show-error="showError"
        @update:campaign-name="$emit('update:campaignName', $event)"
        @update:objective="$emit('update:objective', $event)"
      />
    </div>

    <!-- Target Segment Selection -->
    <TargetSegmentSelector
      :title="__('Select Target Candidates')"
      :description="__('Choose candidate segments or define custom criteria for recruitment')"
      :config-data="configData"
      :conditions="conditions"
      :candidate-count="candidateCount"
      @update:config-data="$emit('update:configData', $event)"
      @update:conditions="$emit('update:conditions', $event)"
      @update:candidate-count="$emit('update:candidateCount', $event)"
      @validate="$emit('validate', $event)"
      @change="$emit('change', $event)"
    />

    <!-- Campaign Tags -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <div class="mb-4">
        <h3 class="text-base font-semibold text-gray-900">
          {{ __('Campaign Tags') }}
        </h3>
        <p class="text-sm text-gray-600 mt-1">
          {{ __('Add tags to categorize and organize this recruitment campaign') }}
        </p>
      </div>

      <CampaignTagPicker
        :campaign-id="campaignId"
        :model-value="campaignTags"
        @update:model-value="$emit('update:campaignTags', $event)"
      />
    </div>

    <!-- Campaign Schedule -->
    <CampaignSchedule
      :start-date="startDate"
      @update:start-date="$emit('update:startDate', $event)"
    />
  </div>
</template>

<script setup>
import CampaignBasicInfo from '../molecules/CampaignBasicInfo.vue'
import CampaignTagPicker from '../molecules/CampaignTagPicker.vue'
import TargetSegmentSelector from '../molecules/TargetSegmentSelector.vue'
import CampaignSchedule from '../molecules/CampaignSchedule.vue'

defineProps({
  campaignName: String,
  objective: String,
  campaignId: {
    type: String,
    default: ''
  },
  campaignTags: {
    type: Array,
    default: () => []
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
  showError: Boolean,
  startDate: String
})

defineEmits([
  'update:campaignName',
  'update:objective',
  'update:campaignTags',
  'update:configData',
  'update:conditions',
  'update:candidateCount',
  'validate',
  'change',
  'update:startDate'
])

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
