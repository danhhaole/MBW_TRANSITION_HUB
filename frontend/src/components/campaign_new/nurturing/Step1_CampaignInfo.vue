<template>
  <div class="space-y-6 animate-fadeIn">
    <!-- Campaign Basic Information -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-base font-semibold text-gray-900 mb-4">
        {{ __('Nurturing Campaign Information') }}
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
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <TargetSegmentSelector
        :title="__('Select Audience to Nurture')"
        :description="__('Choose existing contacts or define custom conditions for nurturing')"
        :selection-mode="selectionMode"
        :config-data="configData"
        :conditions="conditions"
        :candidate-count="candidateCount"
        @update:selection-mode="$emit('update:selectionMode', $event)"
        @update:config-data="$emit('update:configData', $event)"
        @update:conditions="$emit('update:conditions', $event)"
        @validate="$emit('validate', $event)"
        @change="$emit('change', $event)"
      />
    </div>
  </div>
</template>

<script setup>
import CampaignBasicInfo from '../molecules/CampaignBasicInfo.vue'
import TargetSegmentSelector from '../molecules/TargetSegmentSelector.vue'

defineProps({
  campaignName: String,
  objective: String,
  selectionMode: {
    type: String,
    default: 'segment'
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
  showError: Boolean
})

defineEmits([
  'update:campaignName',
  'update:objective',
  'update:selectionMode',
  'update:configData',
  'update:conditions',
  'validate',
  'change'
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
