<template>
  <div class="email-content-editor">
        <EmailEditor
      :content="localContent"
      :readonly="readonly"
      @update:content="handleContentUpdate"
      @saved="handleSaved"
    >
      <template #actions>
        <slot name="actions"></slot>
      </template>
    </EmailEditor>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import EmailEditor from '@/components/campaign/content-editors/EmailEditor.vue'

const props = defineProps({
  content: {
    type: Object,
    default: () => ({
      email_subject: '',
      email_content: '',        // Legacy field
      block_content: '',        // EmailBuilder format
      template_content: '',     // HTML format
      mjml_content: '',         // MJML format
      css_content: '',          // CSS content for styling
      attachments: [],
      sender_account: null
    })
  },
  readonly: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:content', 'saved'])

const localContent = ref({
  email_subject: '',
  email_content: '',        // Legacy field
  block_content: '',        // EmailBuilder format
  template_content: '',     // HTML format
  mjml_content: '',         // MJML format
  css_content: '',          // CSS content for styling
  attachments: [],
  sender_account: null,
  ...props.content
})


// Flag to prevent recursive updates
const isUpdatingFromProps = ref(false)

const handleContentUpdate = (content) => {
  if (isUpdatingFromProps.value) {
    return
  }

  // IMPORTANT: Merge all fields to ensure block_content, template_content, css_content are preserved
  localContent.value = { 
    ...localContent.value, 
    ...content,
    // Explicitly ensure all fields are updated
    block_content: content.block_content !== undefined ? content.block_content : localContent.value.block_content,
    template_content: content.template_content !== undefined ? content.template_content : localContent.value.template_content,
    css_content: content.css_content !== undefined ? content.css_content : localContent.value.css_content,
    mjml_content: content.mjml_content !== undefined ? content.mjml_content : localContent.value.mjml_content
  }
  
  console.log('📤 [EmailContentEditor] Forwarding update:content to parent')
  console.log('   block_content exists:', !!localContent.value.block_content)
  console.log('   block_content length:', localContent.value.block_content?.length || 0)
  console.log('   template_content exists:', !!localContent.value.template_content)
  console.log('   template_content length:', localContent.value.template_content?.length || 0)
  console.log('   css_content exists:', !!localContent.value.css_content)
  console.log('   css_content length:', localContent.value.css_content?.length || 0)
  
  emit('update:content', { ...localContent.value })
}

watch(() => props.content, (newContent) => {
  if (!newContent) return
  
  isUpdatingFromProps.value = true
  
  // IMPORTANT: Merge all fields to ensure block_content, template_content, css_content are preserved
  localContent.value = { 
    ...localContent.value, 
    ...newContent,
    // Explicitly ensure all fields are updated from props
    block_content: newContent.block_content !== undefined ? newContent.block_content : localContent.value.block_content,
    template_content: newContent.template_content !== undefined ? newContent.template_content : localContent.value.template_content,
    css_content: newContent.css_content !== undefined ? newContent.css_content : localContent.value.css_content,
    mjml_content: newContent.mjml_content !== undefined ? newContent.mjml_content : localContent.value.mjml_content
  }
  
  console.log('🔄 [EmailContentEditor] Props content updated')
  console.log('   block_content exists:', !!localContent.value.block_content)
  console.log('   template_content exists:', !!localContent.value.template_content)
  console.log('   css_content exists:', !!localContent.value.css_content)
  
  setTimeout(() => {
    isUpdatingFromProps.value = false
  }, 0)
}, { deep: true })

// Handle saved event from EmailEditor
const handleSaved = (content) => {
  console.log('💾 [EmailContentEditor] Received saved event from EmailEditor')
  console.log('   content keys:', Object.keys(content || {}))
  console.log('   template_content length:', content?.template_content?.length || 0)
  console.log('   template_content preview:', content?.template_content?.substring(0, 200) + '...')
  console.log('   block_content length:', content?.block_content?.length || 0)
  console.log('   css_content length:', content?.css_content?.length || 0)
  
  // IMPORTANT: Update localContent with ALL fields from saved content
  // Force trigger reactivity by creating new object reference
  // This ensures preview in EmailEditor will show the latest saved content
  localContent.value = { 
    ...localContent.value, 
    ...content,
    // Explicitly ensure all fields are updated
    block_content: content.block_content !== undefined ? content.block_content : localContent.value.block_content,
    template_content: content.template_content !== undefined ? content.template_content : localContent.value.template_content,
    css_content: content.css_content !== undefined ? content.css_content : localContent.value.css_content,
    mjml_content: content.mjml_content !== undefined ? content.mjml_content : localContent.value.mjml_content
  }
  
  console.log('✅ [EmailContentEditor] Updated localContent after save')
  console.log('   template_content length:', localContent.value.template_content?.length || 0)
  console.log('   template_content preview:', localContent.value.template_content?.substring(0, 200) + '...')
  console.log('   localContent object reference changed:', true)
  
  // IMPORTANT: Emit update:content FIRST to trigger EmailEditor's watch(props.content)
  // This will update preview in EmailEditor immediately
  const contentToEmit = { ...localContent.value }
  emit('update:content', contentToEmit)
  console.log('📤 [EmailContentEditor] Emitted update:content to parent (will trigger EmailEditor watch)')
  
  // Then emit saved event to parent (Step2_ContentChannels)
  emit('saved', { ...localContent.value })
  console.log('📤 [EmailContentEditor] Emitted saved event to parent')
}
</script>

<style scoped>
.email-content-editor {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
