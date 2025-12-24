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

  localContent.value = { ...localContent.value, ...content }
  emit('update:content', localContent.value)
}

watch(() => props.content, (newContent) => {
  isUpdatingFromProps.value = true
  localContent.value = { ...localContent.value, ...newContent }
  setTimeout(() => {
    isUpdatingFromProps.value = false
  }, 0)
}, { deep: true })

// Handle saved event from EmailEditor
const handleSaved = (content) => {
  localContent.value = { ...localContent.value, ...content }
  emit('saved', localContent.value)
}
</script>

<style scoped>
.email-content-editor {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
