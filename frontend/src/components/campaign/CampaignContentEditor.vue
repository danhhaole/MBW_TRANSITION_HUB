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
      
      <!-- Zalo Editor (for both ZNS and ZALO_CARE) -->
      <ZaloEditor 
        v-else-if="interaction_type === 'ZALO_ZNS' || interaction_type === 'ZALO_CARE'" 
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
import ZaloEditor from './content-editors/ZaloEditor.vue'
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
  
  // Zalo fields (using blocks structure)
  blocks: [],
  image_url: '',
  
  // Common fields
  success_action: '',
  failure_action: '',
  
  ...props.modelValue
})

// Additional actions state
const additionalActions = ref(props.modelValue.additional_actions || {})

// Translation helper
const __ = (text) => text

// Flag to prevent recursive updates
const isUpdating = ref(false)

// Debounce timer for content updates
let contentUpdateTimer = null

// Handle content updates from child components
const handleContentUpdate = (updatedContent) => {
  console.log('📝 CampaignContentEditor received update:', updatedContent)
  
  // Prevent recursive updates
  if (isUpdating.value) {
    console.log('⏭️ Skipping handleContentUpdate - already updating')
    return
  }
  
  // Set flag immediately
  isUpdating.value = true
  
  // Update local content immediately for responsive UI
  content.value = { ...content.value, ...updatedContent }
  console.log('📝 Updated content.value:', content.value)
  
  // Clear previous timer
  if (contentUpdateTimer) {
    clearTimeout(contentUpdateTimer)
  }
  
  // Debounce emit to avoid too many updates during typing
  contentUpdateTimer = setTimeout(() => {
    console.log('📤 Emitting update:modelValue:', content.value)
    emit('update:modelValue', content.value)
  }, 500) // Wait 500ms after user stops typing
  
  // Reset flag after debounce period + buffer
  setTimeout(() => {
    isUpdating.value = false
  }, 700) // 500ms debounce + 200ms buffer
}

// Handle save action
const handleSave = () => {
  console.log('💾 Saving content:', content.value)
  
  // Clear any pending debounce timers
  if (contentUpdateTimer) {
    clearTimeout(contentUpdateTimer)
    contentUpdateTimer = null
  }
  
  // Emit immediately when saving
  emit('update:modelValue', content.value)
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
  // Prevent recursive updates
  if (isUpdating.value) {
    console.log('⏭️ Skipping handleAdditionalActionsUpdate - already updating')
    return
  }
  
  // Set flag immediately
  isUpdating.value = true
  
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
    emit('update:modelValue', updatedContent)
  }, 500) // Wait 500ms after changes
  
  // Reset flag after debounce period + buffer
  setTimeout(() => {
    isUpdating.value = false
  }, 700) // 500ms debounce + 200ms buffer
}
</script>

<style scoped>
.campaign-content-editor {
  width: 100%;
}
</style>
