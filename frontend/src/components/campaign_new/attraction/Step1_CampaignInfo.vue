<template>
  <div class="space-y-6 animate-fadeIn">
    <!-- Campaign Basic Information -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-base font-semibold text-gray-900 mb-4">
        {{ __('Campaign Information') }}
      </h3>
      <CampaignBasicInfo
        :campaign-name="campaignName"
        :objective="objective"
        :show-error="showError"
        @update:campaign-name="$emit('update:campaignName', $event)"
        @update:objective="$emit('update:description', $event)"
      />
    </div>

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
</template>

<script setup>
import CampaignBasicInfo from '../molecules/CampaignBasicInfo.vue'
import Link from '@/components/Controls/Link.vue'
import { FeatherIcon } from 'frappe-ui'

defineProps({
  campaignName: {
    type: String,
    default: ''
  },
  objective: {
    type: String,
    default: ''
  },
  targetPool: {
    type: String,
    default: ''
  },
  showError: {
    type: Boolean,
    default: false
  },
  description: {
    type: String,
    default: ''
  }
})

defineEmits(['update:campaignName', 'update:objective', 'update:targetPool', 'update:description'])

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
