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

  // IMPORTANT: Merge all fields to preserve ALL fields including email_subject and attachments
  localContent.value = { 
    ...localContent.value, 
    ...content
  }
  
  console.log('📤 [EmailContentEditor] Forwarding update:content to parent')
  console.log('   email_subject:', localContent.value.email_subject)
  console.log('   email_subject type:', typeof localContent.value.email_subject)
  console.log('   email_subject length:', localContent.value.email_subject?.length || 0)
  console.log('   attachments count:', localContent.value.attachments?.length || 0)
  console.log('   block_content exists:', !!localContent.value.block_content)
  console.log('   template_content exists:', !!localContent.value.template_content)
  console.log('   css_content exists:', !!localContent.value.css_content)
  
  emit('update:content', { ...localContent.value })
}

watch(() => props.content, (newContent) => {
  if (!newContent) return
  
  isUpdatingFromProps.value = true
  
  console.log('🔄 [EmailContentEditor] Props content updated')
  console.log('   newContent.email_subject:', newContent?.email_subject)
  console.log('   newContent.email_subject type:', typeof newContent?.email_subject)
  console.log('   newContent.email_subject length:', newContent?.email_subject?.length || 0)
  console.log('   current localContent.email_subject:', localContent.value.email_subject)
  
  // IMPORTANT: Preserve email_subject if newContent.email_subject is empty string or undefined
  // This prevents overwriting user input when props are updated from parent
  // Only preserve if current localContent has a non-empty email_subject AND newContent doesn't have a valid one
  const currentEmailSubject = localContent.value.email_subject || ''
  const newEmailSubject = newContent.email_subject || ''
  const shouldPreserveEmailSubject = currentEmailSubject.trim() !== '' && newEmailSubject.trim() === ''
  const preservedEmailSubject = shouldPreserveEmailSubject 
    ? currentEmailSubject
    : newEmailSubject
  
  // IMPORTANT: Merge all fields to preserve ALL fields including email_subject and attachments
  localContent.value = { 
    ...localContent.value, 
    ...newContent,
    // IMPORTANT: Preserve email_subject if newContent doesn't have a valid value
    email_subject: preservedEmailSubject
  }
  
  console.log('✅ [EmailContentEditor] Updated localContent from props')
  console.log('   preserved email_subject:', localContent.value.email_subject)
  console.log('   email_subject preserved:', shouldPreserveEmailSubject)
  console.log('   attachments count:', localContent.value.attachments?.length || 0)
  console.log('   block_content exists:', !!localContent.value.block_content)
  console.log('   template_content exists:', !!localContent.value.template_content)
  console.log('   css_content exists:', !!localContent.value.css_content)
  
  setTimeout(() => {
    isUpdatingFromProps.value = false
  }, 0)
}, { deep: true })

// Handle saved event from EmailEditor
const handleSaved = (content) => {
  console.log('💾 [EmailContentEditor] ========== RECEIVED saved event from EmailEditor ==========')
  console.log('   content keys:', Object.keys(content || {}))
  console.log('   email_subject:', content?.email_subject)
  console.log('   email_subject type:', typeof content?.email_subject)
  console.log('   email_subject length:', content?.email_subject?.length || 0)
  console.log('   email_subject value:', JSON.stringify(content?.email_subject))
  console.log('   attachments count:', content?.attachments?.length || 0)
  console.log('   attachments:', content?.attachments)
  console.log('   template_content length:', content?.template_content?.length || 0)
  console.log('   block_content length:', content?.block_content?.length || 0)
  console.log('   css_content length:', content?.css_content?.length || 0)
  console.log('   Full content:', JSON.stringify(content, null, 2))
  
  // IMPORTANT: Update localContent with ALL fields from saved content (like nurturing campaign)
  // Simply merge - preserve ALL fields including email_subject and attachments
  localContent.value = { 
    ...localContent.value, 
    ...content
  }
  
  console.log('✅ [EmailContentEditor] Updated localContent after save')
  console.log('   localContent.email_subject:', localContent.value.email_subject)
  console.log('   localContent.email_subject type:', typeof localContent.value.email_subject)
  console.log('   localContent.attachments count:', localContent.value.attachments?.length || 0)
  console.log('   template_content length:', localContent.value.template_content?.length || 0)
  
  // IMPORTANT: Emit update:content FIRST to trigger EmailEditor's watch(props.content)
  // This will update preview in EmailEditor immediately
  const contentToEmit = { ...localContent.value }
  emit('update:content', contentToEmit)
  console.log('📤 [EmailContentEditor] Emitted update:content to parent')
  console.log('   contentToEmit.email_subject:', contentToEmit.email_subject)
  console.log('   contentToEmit.attachments count:', contentToEmit.attachments?.length || 0)
  
  // Then emit saved event to parent (Step2_ContentChannels) with ALL fields
  emit('saved', { ...localContent.value })
  console.log('📤 [EmailContentEditor] Emitted saved event to parent')
  console.log('   saved content.email_subject:', localContent.value.email_subject)
  console.log('   saved content.attachments count:', localContent.value.attachments?.length || 0)
  console.log('💾 [EmailContentEditor] ========== END saved event ==========')
}
</script>

<style scoped>
.email-content-editor {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
