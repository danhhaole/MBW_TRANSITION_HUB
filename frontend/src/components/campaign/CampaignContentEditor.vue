<template>
  <div class="campaign-content-editor">
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
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import EmailEditor from './content-editors/EmailEditor.vue'
import ZaloZnsEditor from './content-editors/ZaloZnsEditor.vue'
import ZaloCareEditor from './content-editors/ZaloCareEditor.vue'
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

// Translation helper
const __ = (text) => text

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  content.value = { ...content.value, ...newValue }
}, { deep: true })

// Handle content updates from child components
const handleContentUpdate = (updatedContent) => {
  content.value = { ...content.value, ...updatedContent }
  emit('update:modelValue', content.value)
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
</script>

<style scoped>
.campaign-content-editor {
  @apply w-full;
}
</style>
