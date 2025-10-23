<template>
  <div class="campaign-content-editor space-y-6">
    <!-- Content Editors -->
    <div>
      <!-- Email Editor -->
      <EmailEditor 
        v-if="interaction_type === 'EMAIL'" 
        :content="content"
        :readonly="readonly"
        @update:content="handleContentUpdate"
        @save="handleSave"
        @preview="handlePreview"
      />
      
      <!-- Zalo ZNS Editor -->
      <ZaloZnsEditor 
        v-else-if="interaction_type === 'ZALO_ZNS'" 
        :content="content"
        :readonly="readonly"
        @update:content="handleContentUpdate"
        @save="handleSave"
        @preview="handlePreview"
      />
      
      <!-- Zalo Care Editor -->
      <ZaloCareEditor 
        v-else-if="interaction_type === 'ZALO_CARE'" 
        :content="content"
        :readonly="readonly"
        @update:content="handleContentUpdate"
        @save="handleSave"
        @preview="handlePreview"
      />
      
      <!-- Fallback for unknown interaction type -->
      <div v-else class="text-center py-8">
        <div class="text-gray-500">
          <FeatherIcon name="alert-circle" class="h-12 w-12 mx-auto mb-4" />
          <h3 class="text-lg font-medium mb-2">{{ __("Unknown Interaction Type") }}</h3>
          <p>{{ __("Please select a valid interaction method first") }}</p>
        </div>
      </div>
    </div>

    <!-- Additional Actions -->
    <AdditionalActions
      v-if="interaction_type && interaction_type !== 'UNKNOWN'"
      :interaction-type="interaction_type"
      v-model="additionalActions"
      @update:modelValue="handleAdditionalActionsUpdate"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import EmailEditor from './content-editors/EmailEditor.vue'
import ZaloZnsEditor from './content-editors/ZaloEditor.vue'
import ZaloCareEditor from './content-editors/ZaloCareEditor.vue'
import AdditionalActions from './AdditionalActions.vue'
import { FeatherIcon } from 'frappe-ui'

// Props
const props = defineProps({
  interaction_type: {
    type: String,
    required: true,
    validator: (value) => ['EMAIL', 'ZALO_ZNS', 'ZALO_CARE'].includes(value)
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

// Emits
const emit = defineEmits(['update:modelValue', 'save', 'preview'])

// Local content state
const content = ref({
  // Email fields
  email_subject: '',
  email_content: '',
  attachments: [],
  
  // Zalo fields
  message_content: '',
  image_url: '',
  action_buttons: [],
  
  // Common fields
  success_action: '',
  failure_action: '',
  
  ...props.modelValue
})

// Additional actions state
const additionalActions = ref(props.modelValue.additional_actions || {})

// Translation helper
const __ = (text) => text

// Track if we're updating from emit to prevent loop
const isUpdatingFromEmit = ref(false)

// Watch for external changes
watch(() => props.modelValue, (newValue, oldValue) => {
  // Skip if we just emitted an update
  if (isUpdatingFromEmit.value) {
    return
  }
  
  // Deep equality check to avoid unnecessary updates
  const newValueStr = JSON.stringify(newValue)
  const oldValueStr = JSON.stringify(oldValue)
  if (newValueStr === oldValueStr) {
    return
  }
  
  content.value = { ...content.value, ...newValue }
}, { deep: true })

// Debounce timer for content updates
let contentUpdateTimer = null

// Handle content updates from child components
const handleContentUpdate = (updatedContent) => {
  // Update local content immediately for responsive UI
  content.value = { ...content.value, ...updatedContent }
  
  // Clear previous timer
  if (contentUpdateTimer) {
    clearTimeout(contentUpdateTimer)
  }
  
  // Debounce emit to avoid too many updates during typing
  contentUpdateTimer = setTimeout(() => {
    isUpdatingFromEmit.value = true
    emit('update:modelValue', content.value)
    // Reset flag after a short delay
    setTimeout(() => {
      isUpdatingFromEmit.value = false
    }, 100)
  }, 500) // Wait 500ms after user stops typing
}

// Handle save action
const handleSave = () => {
  console.log('💾 Saving content:', content.value)
  emit('save', content.value)
}

// Handle preview action
const handlePreview = () => {
  console.log('👁️ Previewing content:', content.value)
  emit('preview', content.value)
}

// Debounce timer for additional actions updates
let additionalActionsTimer = null

// Handle additional actions update
const handleAdditionalActionsUpdate = (actions) => {
  // Update local state immediately
  additionalActions.value = actions
  const updatedContent = { 
    ...content.value, 
    additional_actions: actions 
  }
  content.value = updatedContent
  
  // Clear previous timer
  if (additionalActionsTimer) {
    clearTimeout(additionalActionsTimer)
  }
  
  // Debounce emit to avoid rapid updates
  additionalActionsTimer = setTimeout(() => {
    isUpdatingFromEmit.value = true
    emit('update:modelValue', updatedContent)
    // Reset flag after a short delay
    setTimeout(() => {
      isUpdatingFromEmit.value = false
    }, 100)
  }, 500) // Wait 500ms after changes
}
</script>

<style scoped>
.campaign-content-editor {
  width: 100%;
}
</style>
