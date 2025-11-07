<template>
  <div class="space-y-4">
    <div class="text-center mb-6">
      <h4 class="text-lg font-medium text-gray-900 mb-2">
        {{ __("Design Content") }}
      </h4>
      <p class="text-sm text-gray-600">
        {{ __("Create the content for your campaign based on the selected interaction method") }}
      </p>
    </div>

    <!-- Show warning if no interaction method selected -->
    <div v-if="!interactionMethod" class="text-center py-12">
      <FeatherIcon name="alert-triangle" class="h-8 w-8 text-yellow-600 mx-auto mb-2" />
      <h4 class="text-lg font-medium text-yellow-900 mb-2">
        {{ __("No interaction method selected") }}
      </h4>
      <p class="text-yellow-700">
        {{ __("Please go back to Step 1 to select an interaction method") }}
      </p>
    </div>

    <!-- Content Editor -->
    <CampaignContentEditor
      v-else
      :interaction_type="interactionMethod"
      :model-value="modelValue"
      :readonly="readonly"
      @update:model-value="$emit('update:model-value', $event)"
      @save="$emit('save', $event)"
      @preview="$emit('preview', $event)"
    />
  </div>
</template>

<script setup>
import { FeatherIcon } from 'frappe-ui'
import CampaignContentEditor from './CampaignContentEditor.vue'

const props = defineProps({
  interactionMethod: {
    type: String,
    default: ''
  },
  modelValue: {
    type: Object,
    default: () => ({})
  },
  readonly: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:model-value', 'save', 'preview'])
</script>
