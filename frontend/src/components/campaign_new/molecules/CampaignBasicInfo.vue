<template>
  <div class="space-y-6">
    <!-- Campaign Name -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">
        {{ __('Campaign Name') }} <span class="text-red-500">*</span>
      </label>
      <FormControl
        v-model="localCampaignName"
        type="text"
        :placeholder="__('Example: React Candidate Nurturing Q4/2024')"
        size="md"
      />
      <p v-if="!localCampaignName && showError" class="mt-1 text-sm text-red-600">
        {{ __('Campaign name is required') }}
      </p>
    </div>

    <!-- Campaign Objective -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">
        {{ __('Campaign Objective') }}
      </label>
      <FormControl
        v-model="localObjective"
        type="textarea"
        :placeholder="__('Describe what you want to achieve with this campaign...')"
        :rows="4"
        size="md"
      />
      <div class="flex justify-between mt-1">
        <p class="text-xs text-gray-500 ml-auto">
          {{ localObjective?.length || 0 }}/500
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { FormControl } from 'frappe-ui'

const props = defineProps({
  campaignName: {
    type: String,
    default: ''
  },
  objective: {
    type: String,
    default: ''
  },
  showError: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:campaignName', 'update:objective'])

const localCampaignName = computed({
  get: () => props.campaignName,
  set: (value) => emit('update:campaignName', value)
})

const localObjective = computed({
  get: () => props.objective,
  set: (value) => {
    console.log('[CampaignBasicInfo] update objective (localObjective):', value)
    emit('update:objective', value)
  }
})

watch(
  () => props.objective,
  (val) => {
    console.log('[CampaignBasicInfo] props.objective changed:', val)
  }
)

</script>
